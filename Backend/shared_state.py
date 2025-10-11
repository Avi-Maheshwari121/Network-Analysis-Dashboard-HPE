"""
Shared state module for Network Monitoring Dashboard
Contains all global variables used across modules
"""

# Packet storage
streams = {}
all_packets_history = []

# Process state
capture_active = False
tshark_proc = None

# WebSocket connections
connected_clients = {}

# Protocol Distribution
protocol_distribution = {
    "TCP": 0,
    "UDP": 0,
    "RTP": 0,
    "TLSV": 0,
    "QUIC": 0,
    "DNS": 0,
    "Others": 0
}

# Metrics state
metrics_state = {
    "inbound_throughput": 0.0,
    "outbound_throughput": 0.0,
    "latency": 0.0,
    "jitter": 0.0,
    "packet_loss_count": 0,
    "packet_loss_percent": 0.0,
    "status": "stopped",
    "last_update": None,
    "protocol_distribution": protocol_distribution,
    "streamCount": 0,
    "totalPackets": 0
}

# Packet loss 
lost_packets_total = 0
expected_packets_total = 0

# Ip Address List
ip_address = []

# List to store a history of metrics for the session summary
session_metrics_history = []