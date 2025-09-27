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

# Metrics state
metrics_state = {
    "inbound_throughput": 0.0,
    "outbound_throughput": 0.0,
    "latency": 0.0,
    "jitter": 0.0,
    "packet_loss_count": 0,
    "packet_loss_percent": 0.0,
    "status": "stopped",
    "last_update": None
}

# Packet loss 
lost_packets_total = 0
expected_packets_total = 0

# Ip Address List
ip_address = []