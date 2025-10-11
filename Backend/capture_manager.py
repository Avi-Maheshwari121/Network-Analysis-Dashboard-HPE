import subprocess
import time
from datetime import datetime
import shared_state
import re
import psutil
import socket


# Map IP protocol numbers to names -> Global Object
protocol_map = {
    "6": "tcp",      # TCP
    "17": "udp",     # UDP
    "1": "icmp",     # ICMP
    "2": "igmp",     # IGMP
    "47": "gre",     # GRE
    "50": "esp",     # ESP
    "51": "ah"       # Authentication Header
}


def get_device_ips():
    """Get all IPv4 and IPv6 addresses from all network interfaces."""
    device_ips = []
    
    try:
        all_addrs = psutil.net_if_addrs()
        
        for iface_name, addrs in all_addrs.items():
            for addr in addrs:
                if addr.family == socket.AF_INET:  # IPv4
                    device_ips.append(addr.address)
                elif addr.family == socket.AF_INET6:  # IPv6
                    ip6_without_zone = addr.address.split('%')[0]  # strip %zone
                    device_ips.append(ip6_without_zone)
        
        # Remove duplicates
        device_ips = list(set(device_ips))
                
    except Exception as e:
        print(f"Error getting device IPs: {e}")
    
    return device_ips



def get_network_interfaces():
    """Get a list of available network interfaces using tshark."""
    try:
        # Execute tshark -D to list interfaces
        proc = subprocess.run(
            ["tshark", "-D"],
            capture_output=True,
            text=True,
            check=True
        )
        # Parse the output to get both ID and descriptive name
        interfaces = []
        output = proc.stdout.strip()
        lines = output.split('\n')
        for line in lines:
            match = re.search(r'^\d+\.\s+(.+?)(?:\s+\((.+)\))?$', line)
            if match:
                interface_id = match.group(1).strip()
                descriptive_name = match.group(2).strip() if match.group(2) else interface_id
                interfaces.append({"id": interface_id, "name": descriptive_name})
        return interfaces
    except Exception as e:
        print(f"Error getting network interfaces: {e}")
        # Provide a default list if tshark command fails
        return [{"id": "Wi-Fi", "name": "Wi-Fi (Default)"}, {"id": "Ethernet", "name": "Ethernet (Default)"}]
    


# Starts Tshark Subprocess
def start_tshark(interface = "Wi-Fi"):
    if shared_state.tshark_proc is not None:
        return False, "Tshark already running"
    
    try:
        tshark_cmd = [
            "tshark",
            "-i", interface,
            "-T", "fields",
            "-e", "frame.number",
            "-e", "frame.time_epoch",
            "-e", "ip.src",
            "-e", "ip.dst",
            "-e", "frame.len", # bytes
            "-e", "_ws.col.Protocol", # Gives highest level protocol
            "-e", "_ws.col.Info",
            "-e", "tcp.stream",
            "-e", "udp.stream",
            "-e", "tcp.analysis.ack_rtt",
            "-e", "tcp.analysis.retransmission",
            "-e", "tcp.analysis.fast_retransmission",
            "-e", "tcp.analysis.spurious_retransmission",
            "-e", "rtp.ssrc",
            "-e", "rtp.seq",
            "-e", "ip.proto", # 15
            "-e", "ipv6.src", # 16
            "-e", "ipv6.dst", # 17
            "-e", "rtp.timestamp",  # 18 - NEW: RTP timestamp for jitter
            "-e", "rtp.p_type",     # 19 - NEW: RTP payload type
            "-e", "ipv6.nxt", # 20
            "-E", "separator=|",
            "-E", "occurrence=f",
            "-E", "header=n",
            "-E", "quote=n"
        ]
        
        shared_state.tshark_proc = subprocess.Popen(
            tshark_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True, # All fields are initially string
            bufsize=1 # Line Buffered Output
        )
        
        shared_state.capture_active = True
        print("Tshark started successfully")
        return True, "Tshark started successfully"
    except Exception as e:
        print(f"Error starting tshark: {e}")
        return False, f"Error starting tshark: {e}"


def stop_tshark():
    """Stop tshark packet capture process"""
    if shared_state.tshark_proc:
        try:
            shared_state.tshark_proc.terminate()
            shared_state.tshark_proc.wait(timeout = 5)
        except subprocess.TimeoutExpired:
            shared_state.tshark_proc.kill() # Forcefully kills tshark after timeout
            shared_state.tshark_proc.wait()
        finally:
            shared_state.tshark_proc = None
            shared_state.capture_active = False

            # Reset all shared state data
            shared_state.streams = {}
            shared_state.all_packets_history = []
            shared_state.session_metrics_history = [] # <-- UPDATED: Reset session history
            shared_state.lost_packets_total = 0
            shared_state.expected_packets_total = 0
            shared_state.protocol_distribution = {
                "TCP": 0,
                "UDP": 0,
                "RTP": 0,
                "TLSV": 0,
                "QUIC": 0,
                "DNS": 0,
                "Others": 0
            }
            
            shared_state.metrics_state.update({
                "inbound_throughput": 0.0,
                "outbound_throughput": 0.0,
                "latency": 0.0,
                "jitter": 0.0,
                "packet_loss_count": 0,
                "packet_loss_percent": 0.0,
                "status": "stopped",
                "last_update": None,
                "protocol_distribution": shared_state.protocol_distribution,
                "streamCount": 0,
                "totalPackets": 0
            })
            
            print("Tshark stopped")
        return True, "Tshark stopped successfully"
    else:
        return False, "Tshark was not running"
    

# Parse packet once and store only needed fields for display
# T.C: O(1) for 1 packet
def parse_and_store_packet(parts):
    try:
        frame_number = parts[0] or "N/A"
        timestamp = parts[1] or "N/A"

        source_ip = parts[2] or parts[16] or "N/A"  # ip.src or ipv6.src
        dest_ip = parts[3] or parts[17] or "N/A"    # ip.dst or ipv6.dst

        length = parts[4] or "0"
        protocols = parts[5] or "N/A"
        info = parts[6] or "N/A"

        # Format timestamp for display (do this once during storage)
        if timestamp != "N/A":
            try:
                ts_float = float(timestamp)
                formatted_time = datetime.fromtimestamp(ts_float).strftime("%H:%M:%S.%f")[:-3]
            except:
                formatted_time = timestamp
        else:
            formatted_time = "N/A"

        packet_data = {
            "no": frame_number,
            "time": formatted_time,
            "source": source_ip,
            "destination": dest_ip,
            "protocol": protocols,
            "length": length,
            "info": info[:100] + "..." if len(info) > 100 else info # Truncate info
        }
        return packet_data
    except Exception as e:
        # Return minimal data on error
        return {
            "no": "N/A",
            "time": "N/A",
            "source": "N/A",
            "destination": "N/A",
            "protocol": "N/A",
            "length": "0",
            "info": "N/A"
        }


def capture_packets(duration):
    """Capture packets for specified duration"""
    if not shared_state.tshark_proc or not shared_state.capture_active:
        return

    # Clear streams for current batch
    shared_state.streams = {}

    # Cleared all_packets_history also
    shared_state.all_packets_history = []
    
    start = time.time()
    new_packets_count = 0
    
    while time.time() - start < duration and shared_state.capture_active:
        try:
            # Check if process is still alive
            if shared_state.tshark_proc.poll() is not None:
                print("Tshark process terminated unexpectedly")
                break
            
            line = shared_state.tshark_proc.stdout.readline()
            if not line:
                break

            # Split line into fields using pipe separator
            parts = line.strip().split("|")
           
            # Parse and store formatted packet for display (EFFICIENT)
            formatted_packet = parse_and_store_packet(parts)
            if formatted_packet:
                shared_state.all_packets_history.append(formatted_packet)
                new_packets_count += 1

            # Group by stream for metrics calculation
            ip_proto = parts[15]  or "N/A"
            proto = parts[5] or "N/A"   # Text protocol field
            tcp_stream = parts[7] or "N/A"
            udp_stream = parts[8] or "N/A"
            rtp_ssrc = parts[13] or "N/A"
            proto_temp = parts[20] or "N/A"

            # Get protocol name from number
            proto_name = protocol_map.get(ip_proto, None)
            proto_temp = protocol_map.get(proto_temp, None)

            # Stream classification with numeric protocol mapping
            if (proto_name == "tcp" or proto == "tcp" or proto_temp == "tcp") and tcp_stream != "N/A":
                key = ("tcp", tcp_stream)
            elif proto_name == "udp" and udp_stream != "N/A":
                key = ("udp", udp_stream)
            elif "RTP" in proto.upper() and rtp_ssrc != "N/A":  # RTP uses text field
                key = ("rtp", rtp_ssrc)
            else:
                key = ("other", "misc")

            # Add packet to stream group
            if key not in shared_state.streams:
                shared_state.streams[key] = []
            shared_state.streams[key].append(parts)

        except Exception as e:
            print(f"Error reading packet: {e}")
            break


def clear_all_packets():
    """Clear all stored packets"""
    shared_state.streams = {}
    shared_state.all_packets_history = []
    print("All packets cleared")


def get_formatted_packets(display_count):
    """Get formatted packets for display - FAST! No re-parsing needed"""
    return shared_state.all_packets_history[-display_count:]  # Direct slice - O(1) operation!


def is_capture_active():
    """Check if capture is currently active"""
    return shared_state.capture_active


def get_streams():
    """Get current streams for metrics calculation"""
    return shared_state.streams