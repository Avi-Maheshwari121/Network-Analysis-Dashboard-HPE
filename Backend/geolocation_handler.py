"""
Geolocation handler for resolving public IP addresses to
geographic location and reverse DNS information.
"""

import asyncio
import socket
import time
from ipaddress import ip_address

import aiohttp

import shared_state
from static_geolocation_db import STATIC_GEOLOCATION_DB

# Rate limiting
LAST_API_CALL_TIME = 0
MIN_TIME_BETWEEN_CALLS = 0.023  # ~45 requests per minute (API limit)

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
    """Fetch geolocation and rDNS data for a single IP"""
    global LAST_API_CALL_TIME
    hostname = None

    # Get rDNS hostname
    try:
        loop = asyncio.get_running_loop()
        dns_lookup_task = loop.run_in_executor(None, socket.gethostbyaddr, ip)
        hostname_tuple = await asyncio.wait_for(dns_lookup_task, timeout=1.5)
        hostname = hostname_tuple[0]
    except (asyncio.TimeoutError, socket.herror):
        hostname = None
    except OSError as exc:
        print(f"Error during rDNS lookup for {ip}: {exc}")
        hostname = None

    # CHECK STATIC DATABASE FIRST and if not found here
    # then only make API Call
    if ip in STATIC_GEOLOCATION_DB:
        static_data = STATIC_GEOLOCATION_DB[ip]
        geo_data = {
            "ip": ip,
            "latitude": static_data['lat'],
            "longitude": static_data['long'],
            "city": static_data['city'],
            "country": static_data['country'],
            "hostname": hostname,
        }
        return geo_data

    try:
        current_time = time.time()
        time_since_last = current_time - LAST_API_CALL_TIME
        if time_since_last < MIN_TIME_BETWEEN_CALLS:
            await asyncio.sleep(MIN_TIME_BETWEEN_CALLS - time_since_last)

        url = f"http://ip-api.com/json/{ip}?fields=status,lat,lon,city,country,query"
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as response:
            LAST_API_CALL_TIME = time.time()
            if response.status == 200:
                data = await response.json()
                if data.get("status") == "success":
                    geo_data = {
                        "ip": data.get("query", ip),
                        "latitude": data.get("lat"),
                        "longitude": data.get("lon"),
                        "city": data.get("city", "Unknown"),
                        "country": data.get("country", "Unknown"),
                        "hostname": hostname
                    }
                    return geo_data
    except (aiohttp.ClientError, asyncio.TimeoutError, ValueError) as exc:
        print(f"Geolocation fetch failed for {ip}: {exc}")

    return None

async def process_geolocation_batch(ips_to_query):
    """Process a batch of IPs for geolocation lookup"""
    if not ips_to_query:
        return

    async with aiohttp.ClientSession() as session:
        # We process sequentially to respect rate limits
        for ip in ips_to_query:
            result = await fetch_geolocation(session, ip)

            if result and isinstance(result, dict):
                # Add passively captured DNS name if it exists
                if ip in shared_state.ip_to_dns:
                    result["dns_name"] = shared_state.ip_to_dns[ip]

                # Add application info if it exists
                if ip in shared_state.ip_stats:
                    stats = shared_state.ip_stats[ip]
                    result["app_info"] = stats.get("app_info")

                # Now, append the fully formed result
                shared_state.new_geolocations.append(result)

def extract_ips_from_packets(_packets_data):
    """Extract unique public IPs from raw packet data"""
    public_ips = set()
    all_raw_packets = []
    if shared_state.streams:
        for packet_list in shared_state.streams.values():
            all_raw_packets.extend(packet_list)

    for parts in all_raw_packets:
        try:
            source = parts[2] or parts[16]
            destination = parts[3] or parts[17]
            for ip in [source, destination]:
                if ip and ip != "N/A" and is_public_ip(ip):
                    if (ip not in shared_state.ip_address and
                        ip not in shared_state.queried_public_ips):
                        public_ips.add(ip)
        except (IndexError, TypeError):
            continue
    return public_ips

async def geolocation_loop():
    """Background task that processes geolocation requests every 2 seconds"""
    while True:
        await asyncio.sleep(2.0)
        if not shared_state.capture_active:
            continue
        if shared_state.streams:
            new_public_ips = extract_ips_from_packets(None)
            if new_public_ips:
                shared_state.queried_public_ips.update(new_public_ips)
                await process_geolocation_batch(list(new_public_ips))
