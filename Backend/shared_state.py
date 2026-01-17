"""
Shared mutable runtime state for the Network Analysis Dashboard.

This module intentionally defines module-level variables that represent
mutable application state (not constants). These variables are updated
at runtime by multiple components such as the capture manager,
WebSocket server, metrics calculator, and summarization logic.

Because these are runtime state holders and not constants, they follow
snake_case naming instead of UPPER_CASE. And since pylint consider them 
as constants which is not true and therefore disabled invalid-name error here.
"""

# pylint: disable=invalid-name

# Duration value
capture_duration = 1.5

session_start_time = None
session_duration_final = 0

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
    "IGMP": 0,
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
    "packets_per_second": 0,
    "inbound_throughput_peak": 0.0,
    "inbound_throughput_avg": 0.0,
    "outbound_throughput_peak": 0.0,
    "outbound_throughput_avg": 0.0,
    "inbound_goodput_peak": 0.0,
    "inbound_goodput_avg": 0.0,
    "outbound_goodput_peak": 0.0,
    "outbound_goodput_avg": 0.0
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

# Packets per second
packets_Per_Second = 0

# TCP Data
tcp_metrics = {
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

# RTP Data
rtp_metrics = {
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

# UDP Data
udp_metrics = {
    "packets_per_second": 0,
    "inbound_throughput": 0,
    "outbound_throughput": 0,
    "inbound_throughput_peak": 0.0,
    "inbound_throughput_avg": 0.0,
    "outbound_throughput_peak": 0.0,
    "outbound_throughput_avg": 0.0
}

# QUIC Data
quic_metrics = {
    "packets_per_second": 0,
    "inbound_throughput": 0,
    "outbound_throughput": 0,
    "inbound_throughput_peak": 0.0,
    "inbound_throughput_avg": 0.0,
    "outbound_throughput_peak": 0.0,
    "outbound_throughput_avg": 0.0
}

# DNS Data
dns_metrics = {
    "packets_per_second": 0,
    "inbound_throughput": 0,
    "outbound_throughput": 0,
    "inbound_throughput_peak": 0.0,
    "inbound_throughput_avg": 0.0,
    "outbound_throughput_peak": 0.0,
    "outbound_throughput_avg": 0.0
}

# IGMP Data
igmp_metrics = {
    "packets_per_second": 0,
    "inbound_throughput": 0,
    "outbound_throughput": 0,
    "inbound_throughput_peak": 0.0,
    "inbound_throughput_avg": 0.0,
    "outbound_throughput_peak": 0.0,
    "outbound_throughput_avg": 0.0
}

# IPV4 Data
ipv4_metrics = {
    "packets_per_second": 0,
    "inbound_throughput": 0,
    "outbound_throughput": 0,
    "inbound_throughput_peak": 0.0,
    "inbound_throughput_avg": 0.0,
    "outbound_throughput_peak": 0.0,
    "outbound_throughput_avg": 0.0
}

# IPV6 Data
ipv6_metrics = {
    "packets_per_second": 0,
    "inbound_throughput": 0,
    "outbound_throughput": 0,
    "inbound_throughput_peak": 0.0,
    "inbound_throughput_avg": 0.0,
    "outbound_throughput_peak": 0.0,
    "outbound_throughput_avg": 0.0
}

# IP Composition
ip_composition = {
    "ipv4_packets": 0,
    "ipv6_packets": 0,
    "ipv4_packets_cumulative": 0,
    "ipv6_packets_cumulative": 0,
    "total_packets": 0,
    "ipv4_percentage": 0.0,
    "ipv6_percentage": 0.0
}

# Encryption Composition
encryption_composition = {
    "encrypted_packets": 0,
    "unencrypted_packets": 0,
    "encrypted_packets_cumulative": 0,
    "unencrypted_packets_cumulative": 0,
    "total_packets": 0,
    "encrypted_percentage": 0.0,
    "unencrypted_percentage": 0.0
}

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

# Internal tracking for running averages (NOT sent to frontend)
running_state = {
    # throughtput_sum represents bits sum

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

last_periodic_summary_time = None
