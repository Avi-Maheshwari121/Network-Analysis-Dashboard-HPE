import aiohttp
import asyncio
from ipaddress import ip_address
import shared_state
import time

# Rate limiting
last_api_call_time = 0
min_time_between_calls = 0.023  # ~45 requests per minute (API limit)

def is_public_ip(ip_str):
    """Check if an IP address is public (not private/reserved)"""
    try:
        ip_obj = ip_address(ip_str)
        return not (ip_obj.is_private or ip_obj.is_loopback or 
                   ip_obj.is_link_local or ip_obj.is_multicast or
                   ip_obj.is_reserved)
    except ValueError:
        return False

async def fetch_geolocation(session, ip):
    """Fetch geolocation data for a single IP from ip-api.com"""
    global last_api_call_time
    
    # Rate limiting - ensure we don't exceed 45 requests/minute
    current_time = time.time()
    time_since_last = current_time - last_api_call_time
    if time_since_last < min_time_between_calls:
        await asyncio.sleep(min_time_between_calls - time_since_last)
    
    try:
        # Use JSON format for easier parsing
        url = f"http://ip-api.com/json/{ip}?fields=status,lat,lon,city,country,query"
        
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as response:
            last_api_call_time = time.time()
            
            if response.status == 429:  # Rate limited
                print(f"Rate limited by ip-api.com, skipping {ip}")
                return None
            
            if response.status == 200:
                data = await response.json()
                
                if data.get("status") == "success":
                    geo_data = {
                        "ip": data.get("query", ip),
                        "latitude": data.get("lat"),
                        "longitude": data.get("lon"),
                        "city": data.get("city", "Unknown"),
                        "country": data.get("country", "Unknown")
                    }
                    return geo_data
                else:
                    print(f"Failed geolocation lookup for {ip}: {data}")
                    return None
                    
    except asyncio.TimeoutError:
        print(f"Timeout fetching geolocation for {ip}")
    except Exception as e:
        print(f"Error fetching geolocation for {ip}: {e}")
    
    return None


async def process_geolocation_batch(ips_to_query):
    """Process a batch of IPs for geolocation lookup"""
    if not ips_to_query:
        return
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for ip in ips_to_query:
            tasks.append(fetch_geolocation(session, ip))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if result and isinstance(result, dict):
                ip = result["ip"]
                shared_state.new_geolocations.append(result)

def extract_ips_from_packets(packets_data):
    """Extract unique public IPs from packet data"""
    public_ips = set()
    
    for packet in packets_data:
        source = packet.get("source", "N/A")
        destination = packet.get("destination", "N/A")
        
        for ip in [source, destination]:
            if ip != "N/A" and is_public_ip(ip):
                # Check if not in device IPs and not already queried
                if (ip not in shared_state.ip_address and 
                    ip not in shared_state.queried_public_ips):
                    public_ips.add(ip)
    
    return public_ips

async def geolocation_loop():
    """Background task that processes geolocation requests every 2 seconds"""
    while True:
        await asyncio.sleep(2.0)  # Check every 2 seconds
        
        if not shared_state.capture_active:
            continue
        
        # Extract public IPs from recent packets
        if shared_state.all_packets_history:
            new_public_ips = extract_ips_from_packets(shared_state.all_packets_history)
            
            if new_public_ips:
                # Mark these IPs as queried
                shared_state.queried_public_ips.update(new_public_ips)
                
                # Process the batch
                await process_geolocation_batch(list(new_public_ips))
