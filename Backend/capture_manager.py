"""Packet capture and session management logic."""

import re
import socket
import asyncio
import subprocess
import time
from datetime import datetime
import psutil
import shared_state
import app_detector


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
    ipv4_list = []
    ipv6_list = []

    try:
        all_addrs = psutil.net_if_addrs()

        for _iface_name, addrs in all_addrs.items():
            for addr in addrs:
                if addr.family == socket.AF_INET:  # IPv4
                    device_ips.append(addr.address)
                    ipv4_list.append(addr.address)
                elif addr.family == socket.AF_INET6:  # IPv6
                    ip6_without_zone = addr.address.split('%')[0]  # strip %zone
                    device_ips.append(ip6_without_zone)
                    ipv6_list.append(ip6_without_zone)

        # Remove duplicates
        device_ips = list(set(device_ips))
        ipv4_list = list(set(ipv4_list))
        ipv6_list = list(set(ipv6_list))

        shared_state.ip_address = device_ips
        shared_state.ipv4_ips = ipv4_list
        shared_state.ipv6_ips = ipv6_list
    except (psutil.Error, OSError) as e:
        print(f"Error getting device IPs: {e}")


def get_network_interfaces():
    """Get a list of available network interfaces using tshark."""
    try:
        proc = subprocess.run(
            ["tshark", "-D"],
            capture_output=True,
            text=True,
            check=True
        )
        interfaces = []
        output = proc.stdout.strip()
        lines = output.split('\n')

        for line in lines:
            match = re.match(r'^(\d+)\.\s+(.+?)(?:\s+\((.+?)\))?$', line)
            if match:
                interface_num = match.group(1)
                full_interface_path = match.group(2).strip()
                descriptive_name = match.group(3).strip() if match.group(3) else full_interface_path

                interfaces.append({
                    "id": interface_num,
                    "name": descriptive_name,
                    "full_path": full_interface_path
                })

        print(f"Found {len(interfaces)} network interfaces")
        return interfaces
    except (FileNotFoundError, subprocess.CalledProcessError, OSError) as e:
        print(f"Error getting network interfaces: {e}")
        return [{"id": "1", "name": "Default Interface"}]



async def start_tshark(interface = "1"):
    """Start tshark with the specified interface (number or name)"""

    if shared_state.tshark_proc is not None:
        return False, "Tshark already running"

    try:
        print(f"Starting tshark on interface: {interface}")

        tshark_cmd = [
            "tshark",
            "-i", str(interface),
            "-T", "fields",
            "-l",
            "-e", "frame.number",
            "-e", "frame.time_epoch",
            "-e", "ip.src",
            "-e", "ip.dst",
            "-e", "frame.len",
            "-e", "_ws.col.Protocol",
            "-e", "_ws.col.Info",
            "-e", "tcp.stream",
            "-e", "udp.stream",
            "-e", "tcp.analysis.ack_rtt",
            "-e", "tcp.analysis.retransmission",
            "-e", "tcp.analysis.fast_retransmission",
            "-e", "tcp.analysis.spurious_retransmission",
            "-e", "rtp.ssrc",
            "-e", "rtp.seq",
            "-e", "ip.proto",
            "-e", "ipv6.src",
            "-e", "ipv6.dst",
            "-e", "rtp.timestamp",
            "-e", "rtp.p_type",
            "-e", "ipv6.nxt",
            "-e", "tcp.len",
            "-e", "udp.length",
            "-e", "tcp.srcport",
            "-e", "tcp.dstport",
            "-e", "udp.srcport",
            "-e", "udp.dstport",
            "-e", "dns.qry.name",
            "-e", "dns.a",
            "-e", "dns.aaaa",
            "-e", "tls.handshake.extensions_server_name",
            "-e", "gquic.tag.sni",
            "-E", "separator=|",
            "-E", "occurrence=f",
            "-E", "header=n",
            "-E", "quote=n"
        ]

        # Create async subprocess
        shared_state.tshark_proc = await asyncio.create_subprocess_exec(
            *tshark_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        # Wait a bit and check if process started
        await asyncio.sleep(0.2)

        if shared_state.tshark_proc.returncode is not None:
            try:
                stderr_output = await asyncio.wait_for(
                    shared_state.tshark_proc.stderr.read(),
                    timeout = 1.5
                )
                error_msg = stderr_output.decode()
                print(f"Tshark failed to start: {error_msg}")
            except (asyncio.TimeoutError, asyncio.CancelledError, UnicodeDecodeError) as e:
                error_msg = e
            shared_state.tshark_proc = None
            return False, f"Failed to start tshark on interface {interface}: {error_msg}"

        shared_state.capture_active = True
        print(f"Tshark started successfully on interface {interface}")
        return True, f"Tshark started on interface {interface}"

    except FileNotFoundError:
        print("Tshark not found. Please install Wireshark/tshark.")
        return False, "Tshark not found. Please install Wireshark."
    except (OSError, RuntimeError) as e:
        print(f"Error starting tshark: {e}")
        if shared_state.tshark_proc:
            shared_state.tshark_proc = None
        return False, f"Error starting tshark: {e}"


def reset_shared_state():
    """Reset all shared capture-related state variables."""
    shared_state.tshark_proc = None
    shared_state.capture_active = False
    shared_state.session_start_time = None

    shared_state.streams = {}
    shared_state.all_packets_history = []

    shared_state.tcp_expected_packets_total = 0
    shared_state.tcp_lost_packets_total = 0
    shared_state.rtp_expected_packets_total = 0
    shared_state.rtp_lost_packets_total = 0

    shared_state.packets_Per_Second = 0

    shared_state.protocol_distribution = {
        "TCP": 0,
        "UDP": 0,
        "RTP": 0,
        "TLS": 0,
        "QUIC": 0,
        "DNS": 0,
        "IGMP": 0,
        "Others": 0
    }

    shared_state.metrics_state.update({
        "inbound_throughput": 0.0,
        "outbound_throughput": 0.0,
        "inbound_goodput": 0.0,
        "outbound_goodput": 0.0,
        "status": "stopped",
        "last_update": None,
        "protocol_distribution": shared_state.protocol_distribution,
        "streamCount": 0,
        "totalPackets": 0,
        "packets_per_second": 0,
        "inbound_throughput_peak": 0.0,
        "inbound_throughput_avg": 0.0,
        "outbound_throughput_peak": 0.0,
        "outbound_throughput_avg": 0.0,
        "inbound_goodput_peak": 0.0,
        "inbound_goodput_avg": 0.0,
        "outbound_goodput_peak": 0.0,
        "outbound_goodput_avg": 0.0
    })

    shared_state.tcp_metrics = {
        "packets_per_second": 0,
        "packet_loss": 0,
        "packet_loss_percentage": 0.0,
        "inbound_throughput": 0,
        "outbound_throughput": 0,
        "latency": 0,
        "inbound_throughput_peak": 0.0,
        "inbound_throughput_avg": 0.0,
        "outbound_throughput_peak": 0.0,
        "outbound_throughput_avg": 0.0,
        "latency_peak": 0.0,
        "latency_avg": 0.0
    }

    shared_state.rtp_metrics = {
        "packets_per_second": 0,
        "packet_loss": 0,
        "packet_loss_percentage": 0.0,
        "inbound_throughput": 0,
        "outbound_throughput": 0,
        "jitter": 0,
        "inbound_throughput_peak": 0.0,
        "inbound_throughput_avg": 0.0,
        "outbound_throughput_peak": 0.0,
        "outbound_throughput_avg": 0.0,
        "jitter_peak": 0.0,
        "jitter_avg": 0.0
    }

    shared_state.udp_metrics = {
        "packets_per_second": 0,
        "inbound_throughput": 0,
        "outbound_throughput": 0,
        "inbound_throughput_peak": 0.0,
        "inbound_throughput_avg": 0.0,
        "outbound_throughput_peak": 0.0,
        "outbound_throughput_avg": 0.0
    }

    shared_state.quic_metrics = {
        "packets_per_second": 0,
        "inbound_throughput": 0,
        "outbound_throughput": 0,
        "inbound_throughput_peak": 0.0,
        "inbound_throughput_avg": 0.0,
        "outbound_throughput_peak": 0.0,
        "outbound_throughput_avg": 0.0
    }

    shared_state.dns_metrics = {
        "packets_per_second": 0,
        "inbound_throughput": 0,
        "outbound_throughput": 0,
        "inbound_throughput_peak": 0.0,
        "inbound_throughput_avg": 0.0,
        "outbound_throughput_peak": 0.0,
        "outbound_throughput_avg": 0.0
    }

    shared_state.igmp_metrics = {
        "packets_per_second": 0,
        "inbound_throughput": 0,
        "outbound_throughput": 0,
        "inbound_throughput_peak": 0.0,
        "inbound_throughput_avg": 0.0,
        "outbound_throughput_peak": 0.0,
        "outbound_throughput_avg": 0.0
    }

    shared_state.ipv4_metrics = {
        "packets_per_second": 0,
        "inbound_throughput": 0,
        "outbound_throughput": 0,
        "inbound_throughput_peak": 0.0,
        "inbound_throughput_avg": 0.0,
        "outbound_throughput_peak": 0.0,
        "outbound_throughput_avg": 0.0
    }

    shared_state.ipv6_metrics = {
        "packets_per_second": 0,
        "inbound_throughput": 0,
        "outbound_throughput": 0,
        "inbound_throughput_peak": 0.0,
        "inbound_throughput_avg": 0.0,
        "outbound_throughput_peak": 0.0,
        "outbound_throughput_avg": 0.0
    }

    shared_state.ip_composition = {
        "ipv4_packets": 0,
        "ipv6_packets": 0,
        "ipv4_packets_cumulative": 0,
        "ipv6_packets_cumulative": 0,
        "total_packets": 0,
        "ipv4_percentage": 0.0,
        "ipv6_percentage": 0.0
    }

    shared_state.encryption_composition = {
        "encrypted_packets": 0,
        "unencrypted_packets": 0,
        "encrypted_packets_cumulative": 0,
        "unencrypted_packets_cumulative": 0,
        "total_packets": 0,
        "encrypted_percentage": 0.0,
        "unencrypted_percentage": 0.0
    }

    shared_state.top_talkers_cumulative = {}
    shared_state.top_talkers_top7 = []

    shared_state.queried_public_ips = set()
    shared_state.new_geolocations = []

    shared_state.ip_stats = {}

    shared_state.running_state = {

        'overall': {
            'inbound_throughput_peak': 0.0,
            'inbound_throughput_sum': 0.0,
            'inbound_throughput_avg': 0.0,
            'outbound_throughput_peak': 0.0,
            'outbound_throughput_sum': 0.0,
            'outbound_throughput_avg': 0.0,
            'inbound_goodput_peak': 0.0,
            'inbound_goodput_sum': 0.0,
            'inbound_goodput_avg': 0.0,
            'outbound_goodput_peak': 0.0,
            'outbound_goodput_sum': 0.0,
            'outbound_goodput_avg': 0.0,
            'cumulative_duration': 0
        },

        'tcp': {
            'inbound_throughput_peak': 0.0,
            'inbound_throughput_sum': 0.0,
            'inbound_throughput_avg': 0.0,
            'outbound_throughput_peak': 0.0,
            'outbound_throughput_sum': 0.0,
            'outbound_throughput_avg': 0.0,
            'latency_peak': 0.0,
            'latency_sum': 0.0,
            'latency_avg': 0.0,
            'latency_count': 0,
            'cumulative_duration': 0
        },

        'udp': {
            'inbound_throughput_peak': 0.0,
            'inbound_throughput_sum': 0.0,
            'inbound_throughput_avg': 0.0,
            'outbound_throughput_peak': 0.0,
            'outbound_throughput_sum': 0.0,
            'outbound_throughput_avg': 0.0,
            'cumulative_duration': 0
        },

        'rtp': {
            'inbound_throughput_peak': 0.0,
            'inbound_throughput_sum': 0.0,
            'inbound_throughput_avg': 0.0,
            'outbound_throughput_peak': 0.0,
            'outbound_throughput_sum': 0.0,
            'outbound_throughput_avg': 0.0,
            'jitter_peak': 0.0,
            'jitter_sum': 0.0,
            'jitter_avg': 0.0,
            'jitter_count': 0,
            'cumulative_duration': 0
        },

        'quic': {
            'inbound_throughput_peak': 0.0,
            'inbound_throughput_sum': 0.0,
            'inbound_throughput_avg': 0.0,
            'outbound_throughput_peak': 0.0,
            'outbound_throughput_sum': 0.0,
            'outbound_throughput_avg': 0.0,
            'cumulative_duration': 0
        },

        'dns': {
            'inbound_throughput_peak': 0.0,
            'inbound_throughput_sum': 0.0,
            'inbound_throughput_avg': 0.0,
            'outbound_throughput_peak': 0.0,
            'outbound_throughput_sum': 0.0,
            'outbound_throughput_avg': 0.0,
            'cumulative_duration': 0
        },

        'igmp': {
            'inbound_throughput_peak': 0.0,
            'inbound_throughput_sum': 0.0,
            'inbound_throughput_avg': 0.0,
            'outbound_throughput_peak': 0.0,
            'outbound_throughput_sum': 0.0,
            'outbound_throughput_avg': 0.0,
            'cumulative_duration': 0
        },

        'ipv4': {
            'inbound_throughput_peak': 0.0,
            'inbound_throughput_sum': 0.0,
            'inbound_throughput_avg': 0.0,
            'outbound_throughput_peak': 0.0,
            'outbound_throughput_sum': 0.0,
            'outbound_throughput_avg': 0.0,
            'cumulative_duration': 0
        },

        'ipv6': {
            'inbound_throughput_peak': 0.0,
            'inbound_throughput_sum': 0.0,
            'inbound_throughput_avg': 0.0,
            'outbound_throughput_peak': 0.0,
            'outbound_throughput_sum': 0.0,
            'outbound_throughput_avg': 0.0,
            'cumulative_duration': 0
        }
    }

    shared_state.last_periodic_summary_time = None


async def stop_tshark():
    """Stop tshark packet capture process"""
    if shared_state.tshark_proc:
        print("Stopping tshark...")
        try:
            # 1. Set flag to stop all loops (metrics_calculator, etc.)
            shared_state.capture_active = False
            await asyncio.sleep(0.2) # Give loops a moment to see the flag

            # 2. Terminate the process
            try:
                shared_state.tshark_proc.terminate()
                await asyncio.wait_for(shared_state.tshark_proc.wait(), timeout = 3.0)
                print("Tshark terminated gracefully")
            except asyncio.TimeoutError:
                print("Tshark didn't terminate, forcing kill...")
                shared_state.tshark_proc.kill()
                await shared_state.tshark_proc.wait()
                print("Tshark killed")
            except (ProcessLookupError, ChildProcessError, OSError) as e:
                print(f"Exception: {e}")

        except (asyncio.CancelledError, OSError, RuntimeError) as e:
            print(f"Error stopping tshark: {e}")
            return False, "Error stopping Tshark" # Return False on error
        finally:
            # 3. Clear the process variable, but DO NOT reset state here
            shared_state.tshark_proc = None

        return True, "Tshark stopped successfully"

    print("Tshark was not running")
    return False, "Tshark was not running"


# Parse packet once and store only needed fields for display
# T.C: O(1) for 1 packet
def parse_and_store_packet(parts):
    """Parse the packet"""
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
            except (ValueError, TypeError, OverflowError):
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
            "info": info
        }
        return packet_data
    except (IndexError, TypeError, ValueError) as _e:
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


async def capture_packets(duration):
    """Capture packets for specified duration using async readline"""
    if not shared_state.tshark_proc or not shared_state.capture_active:
        return

    shared_state.streams = {}
    shared_state.all_packets_history = []

    start = time.time()
    new_packets_count = 0

    while time.time() - start < duration and shared_state.capture_active:
        try:
            # Check if process is still alive
            if shared_state.tshark_proc.returncode is not None:
                print("Tshark process terminated unexpectedly")
                break

            # It won't block the event loop, so frontend commands still work
            try:
                line_bytes = await asyncio.wait_for(
                    shared_state.tshark_proc.stdout.readline(),
                    timeout = 1.0
                )
            except asyncio.TimeoutError:
                # Normal timeout - no data within 1 second, just continue
                continue
            except (asyncio.CancelledError, OSError) as e:
                print(f"Exception: {e}")
                continue

            if not line_bytes:
                break

            line = line_bytes.decode('utf-8', errors='ignore').strip()
            if not line:
                continue

            parts = line.split("|")

            try:
                # Extract fields by their new index
                src_ip = parts[2] or parts[16]
                dst_ip = parts[3] or parts[17]
                _protocol = parts[5]

                tcp_srcport = parts[23]
                tcp_dstport = parts[24]
                udp_srcport = parts[25]
                udp_dstport = parts[26]

                _src_port = tcp_srcport or udp_srcport
                dst_port = tcp_dstport or udp_dstport

                dns_query = parts[27]
                dns_responses = (parts[28] or "") + "," + (parts[29] or "")

                # Get the new SNI field
                sni_hostname = parts[30] if parts[30] else None
                quic_sni = parts[31] if parts[31] else None

                # Detect the application using the new, prioritized logic
                app_info = app_detector.detect_application(
                    src_ip, dst_ip, dst_port,
                    dns_query, dns_responses, sni_hostname, quic_sni
                )

                # Update per-IP stats for the map
                server_ip = dst_ip if dst_ip not in shared_state.ip_address else src_ip
                if server_ip:
                    if server_ip not in shared_state.ip_stats:
                        shared_state.ip_stats[server_ip] = {
                            "packets": 0,
                            "app_info": app_info
                        }

                    shared_state.ip_stats[server_ip]["packets"] += 1

                    if app_info['app'] != 'Unknown':
                        if shared_state.ip_stats[server_ip]["app_info"]['app'] == 'Unknown' or \
                            shared_state.ip_stats[server_ip]["app_info"]['category'] == 'Web':
                            shared_state.ip_stats[server_ip]["app_info"] = app_info

            except (IndexError, TypeError, ValueError, KeyError) as e:
                print(f"Exception: {e}")

            formatted_packet = parse_and_store_packet(parts)
            if formatted_packet:
                shared_state.all_packets_history.append(formatted_packet)
                new_packets_count += 1

            ip_proto = parts[15] if parts[15] else "N/A"
            proto = parts[5] if parts[5] else "N/A"
            tcp_stream = parts[7] if parts[7] else "N/A"
            udp_stream = parts[8] if parts[8] else "N/A"
            rtp_ssrc = parts[13] if parts[13] else "N/A"
            proto_temp = parts[20] if parts[20] else "N/A"

            proto_name = protocol_map.get(ip_proto, None)
            proto_temp = protocol_map.get(proto_temp, None)

            if ((proto_name == "tcp" or
                proto == "tcp" or
                proto_temp == "tcp") and
                tcp_stream != "N/A"
            ):
                key = ("tcp", tcp_stream)
            elif proto_name == "udp" and udp_stream != "N/A":
                key = ("udp", udp_stream)
            elif "RTP" in proto.upper() and rtp_ssrc != "N/A":
                key = ("rtp", rtp_ssrc)
            else:
                key = (proto.lower(), "misc")

            if key not in shared_state.streams:
                shared_state.streams[key] = []
            shared_state.streams[key].append(parts)

        except (asyncio.CancelledError, OSError, RuntimeError) as e:
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
