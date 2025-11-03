"""
Shared state module for Network Monitoring Dashboard
Contains all global variables used across modules
"""

# Duration default value
capture_duration = 1.5

# Packet storage
streams = {}
all_packets_history = []

# Process state
capture_active = False
tshark_proc = None
is_resetting = False  # Flag to block new connections during reset
is_generating_summary = False # Flag to block 'start' during summary

# WebSocket connections
connected_clients = {}

# Protocol Distribution
protocol_distribution = {
    "TCP": 0,
    "UDP": 0,
    "RTP": 0,
    "TLS": 0,
    "QUIC": 0,
    "DNS": 0,
    "Others": 0
}

# Metrics state
metrics_state = {
    "inbound_throughput": 0.0,
    "outbound_throughput": 0.0,
    "inbound_goodput": 0.0,      
    "outbound_goodput": 0.0,
    "status": "stopped",
    "last_update": None,
    "protocol_distribution": protocol_distribution,
    "streamCount": 0,
    "totalPackets": 0,
    "packets_per_second": 0
}

# Packet loss 
tcp_lost_packets_total = 0
tcp_expected_packets_total = 0
rtp_lost_packets_total = 0
rtp_expected_packets_total = 0

# Ip Address List
ip_address = []
ipv4_ips = []
ipv6_ips = []

# List to store a history of metrics for the session summary
session_metrics_history = []

# Packets per second
packets_Per_Second = 0

# TCP Data
tcp_metrics = {
    "packets_per_second": 0,
    "packet_loss": 0,
    "packet_loss_percentage": 0,
    "inbound_throughput": 0,
    "outbound_throughput": 0,
    "latency": 0,
}

# RTP Data
rtp_metrics = {
    "packets_per_second": 0,
    "packet_loss": 0,
    "packet_loss_percentage": 0,
    "inbound_throughput": 0,
    "outbound_throughput": 0,
    "jitter": 0,
}

# UDP Data
udp_metrics = {
    "packets_per_second": 0,
    "inbound_throughput": 0,
    "outbound_throughput": 0,
}

# QUIC Data
quic_metrics = {
    "packets_per_second": 0,
    "inbound_throughput": 0,
    "outbound_throughput": 0,
}

# DNS Data
dns_metrics = {
    "packets_per_second": 0,
    "inbound_throughput": 0,
    "outbound_throughput": 0,
}

# IGMP Data
igmp_metrics = {
    "packets_per_second": 0,
    "inbound_throughput": 0,
    "outbound_throughput": 0,
}

# IPV4 Data
ipv4_metrics = {
    "packets_per_second": 0,
    "inbound_throughput": 0,
    "outbound_throughput": 0,
}

# IPV6 Data
ipv6_metrics = {
    "packets_per_second": 0,
    "inbound_throughput": 0,
    "outbound_throughput": 0,
}

# IP Composition
ip_composition = {
    "ipv4_packets": 0,
    "ipv6_packets": 0,
    "ipv4_packets_cumulative": 0,
    "ipv6_packets_cumulative": 0,
    "total_packets": 0,
    "ipv4_percentage": 0,
    "ipv6_percentage": 0
}

# Encryption Composition
encryption_composition = {
    "encrypted_packets": 0,
    "unencrypted_packets": 0,
    "encrypted_packets_cumulative": 0,
    "unencrypted_packets_cumulative": 0,
    "total_packets": 0,         
    "encrypted_percentage": 0,
    "unencrypted_percentage": 0
}

# History lists for statistical analysis
tcp_metrics_history = []
rtp_metrics_history = []
udp_metrics_history = []
quic_metrics_history = []
dns_metrics_history = []
igmp_metrics_history = []

# Top Talkers - Cumulative tracking
# Dictionary structure: {(src_ip, dst_ip): {"packets": count, "bytes": total_bytes}}
top_talkers_cumulative = {}

# Top 7 talkers to send to frontend
top_talkers_top7 = []

# Geolocation tracking
queried_public_ips = set()  # Track IPs we've already queried
new_geolocations = []  # New geolocations to send to frontend {ip: {lat, lon, city, country}}

# Map resolved IPs to their DNS query name
ip_to_dns = {}

# Per-IP statistics for map visualization
# Structure: {"ip_address": {"packets": Y, "app_info": {...}}}
ip_stats = {}