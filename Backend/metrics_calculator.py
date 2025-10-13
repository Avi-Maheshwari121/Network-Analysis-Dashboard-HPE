# Network performance metrics calculation

from datetime import datetime 
import shared_state

# Static payload type to clock rate mapping 
STATIC_PAYLOAD_RATES = {
    0: 8000,     # PCMU (G.711 μ-law)
    3: 8000,     # GSM  
    4: 8000,     # G723
    5: 8000,     # DVI4 8kHz
    6: 16000,    # DVI4 16kHz
    7: 8000,     # LPC
    8: 8000,     # PCMA (G.711 A-law)
    9: 8000,     # G722
    10: 44100,   # L16 stereo
    11: 44100,   # L16 mono
    12: 8000,    # QCELP
    13: 8000,    # Comfort Noise
    14: 90000,   # MPA (MPEG Audio)
    15: 8000,    # G728 
    16: 11025,   # DVI4 11kHz
    17: 22050,   # DVI4 22kHz
    18: 8000,    # G729
    26: 90000,   # JPEG
    31: 90000,   # H261
    32: 90000,   # MPV (MPEG Video)
    33: 90000,   # MP2T (MPEG2 Transport)
    34: 90000,   # H263
}


def get_protocol_category(protocol_name):
    if not protocol_name or protocol_name == "N/A":
        return "OTHERS"
    
    protocol = protocol_name.upper().strip()  # Convert to uppercase for comparison
    
    if protocol == "TCP":
        return "TCP"
    elif protocol == "UDP":
        return "UDP"
    elif protocol == "RTP" or protocol == "SRTP":
        return "RTP"
    elif protocol == "QUIC":
        return "QUIC"
    elif protocol == "DNS":
        return "DNS"
    elif "TLSV" in protocol:  # matches TLSV1.2, TLSV1.3, etc.
        return "TLSV"
    else:
        return "Others"
    

def detect_dynamic_clock_rate_inline(stream_packets):
    """Detect clock rate using consecutive packet time/timestamp differences"""
    if len(stream_packets) < 2:
        return None
    
    # Find first valid consecutive pair
    for i in range(1, min(5, len(stream_packets))):
        pkt1, pkt2 = stream_packets[i-1], stream_packets[i]
        
        # Time difference (seconds)
        time_diff = pkt2['arrival'] - pkt1['arrival']
        
        # RTP timestamp difference
        rtp_diff = pkt2['rtp_ts'] - pkt1['rtp_ts']
        
        if time_diff > 0 and rtp_diff > 0:
            # Calculate potential clock rate
            calculated_rate = rtp_diff / time_diff
            
            # Match to known rates with 15% tolerance
            known_rates = [8000, 16000, 22050, 44100, 48000, 90000]
            for known_rate in known_rates:
                if abs(calculated_rate - known_rate) / known_rate < 0.15:
                    return known_rate
            
            # Fallback based on magnitude
            return 8000 if calculated_rate < 20000 else 90000
    
    return None


def calculate_metrics():
    """Calculate network performance metrics from streams"""
    import time

    timing_start = time.perf_counter() # For checking how much time metrics calculation took

    # If no packets in streams then return
    if not shared_state.streams:

        # Default Values
        shared_state.metrics_state.update({
            "inbound_throughput": 0.0,
            "outbound_throughput": 0.0,
            "latency": 0.0,
            "jitter": 0.0,
            "last_update": datetime.now().isoformat(),
            "protocol_distribution": shared_state.protocol_distribution,
            "streamCount": 0,
            "totalPackets": 0
        })

        return shared_state.metrics_state

    # Throughput calculation
    inbound_bytes = 0
    outbound_bytes = 0
    start_time, end_time = float("inf"), 0 # float("inf") = positive infinity

    # Packet Loss percentage and count
    total_rtp_loss = 0
    total_tcp_retransmissions = 0
    expected_tcp_packets = 0
    expected_rtp_packets = 0

    # Latency
    latency = 0.0  # Default value
    total_weighted_latency = 0  # Sum of (latency × packet_count)
    total_weight = 0            # Sum of all packet counts (weights)

    # Jitter
    local_jitter_state = {}
    total_weighted_jitter = 0.0
    total_jitter_weight = 0

    # Packet Statistics
    streams_count = len(shared_state.streams)
    total_packets = len(shared_state.all_packets_history)

    # Iterate over all streams
    for (proto, stream_id), packet_list in shared_state.streams.items():
        if proto == "tcp":
            
            # Latency
            stream_rtt_sum = 0
            stream_rtt_count = 0

            # Packet Loss Percentage count
            expected_tcp_packets += len(packet_list)

            for pkt in packet_list:
                try:
                    
                    # Protocol Distribution
                    protocol_name = pkt[5] if pkt[5] else "N/A"
                    protocol_category = get_protocol_category(protocol_name)
                    shared_state.protocol_distribution[protocol_category] = shared_state.protocol_distribution.get(protocol_category, 0) + 1

                    # Packet Loss
                    retrans = str(pkt[10].strip()) if pkt[10] else "0"
                    fast_retrans = str(pkt[11].strip()) if pkt[11] else "0" 
                    spurious = str(pkt[12].strip()) if pkt[12] else "0"

                    if (retrans != "0" or fast_retrans != "0") and spurious == "0":
                        total_tcp_retransmissions += 1


                    # Throughput
                    time_rel = float(pkt[1]) if pkt[1] else -1 
                    length = int(pkt[4]) if pkt[4] else 0

                    source_ip = pkt[2] or pkt[16] or "N/A"
                    destination_ip = pkt[3] or pkt[17] or "N/A"

                    if(source_ip in shared_state.ip_address):
                        outbound_bytes += length
                    elif(destination_ip in shared_state.ip_address):
                        inbound_bytes += length
                    
                    if time_rel >= 0:
                        start_time = min(start_time, time_rel)
                        end_time = max(end_time, time_rel)

                    # Latency
                    rtt_str = pkt[9] if pkt[9] else ""
                    rtt = float(rtt_str) if rtt_str else 0 # stores in seconds

                    if rtt > 0:
                        rtt_ms = rtt * 1000
                        stream_rtt_sum += rtt_ms
                        stream_rtt_count += 1

                except (ValueError, IndexError):
                    continue

            # Latency
            # WEIGHTED AVERAGE: Add this stream's contribution
            if stream_rtt_count > 0:
                stream_avg_rtt = stream_rtt_sum / stream_rtt_count
                stream_weight = len(packet_list)  # Weight by total packets in stream
                
                total_weighted_latency += stream_avg_rtt * stream_weight
                total_weight += stream_weight

        elif proto == "rtp":
            last_seq = None

            expected_rtp_packets += len(packet_list)
            
            jitter_key = f"rtp_{stream_id}"
            if jitter_key not in local_jitter_state:
                local_jitter_state[jitter_key] = {
                    'jitter': 0.0,
                    'prev_transit': None,
                    'clock_rate': None,
                    'packets_for_detection': []  # For dynamic clock rate detection
                }
            
            jitter_state = local_jitter_state[jitter_key]
            
            # Processing packets in arrival order and not as per sorted order of sequence
            for pkt in packet_list:
                try:
                    # Packet Loss
                    seq_str = pkt[14] if pkt[14] else ""
                    seq = int(seq_str) if seq_str else None

                    if seq is not None:
                        if last_seq is not None: 
                            if seq > last_seq:
                                gap = seq - last_seq - 1
                            elif seq < last_seq and (last_seq - seq) > 32768:
                                # Tshark value wrap around
                                # Wraparound case: last_seq was near 65535, seq is near 0
                                gap = (65536 - last_seq - 1) + seq
                            else:
                                gap = 0

                            if gap > 0:
                                total_rtp_loss += gap
                        last_seq = seq

                    # Throughput
                    length = int(pkt[4]) if pkt[4] else 0
                    time_rel = float(pkt[1]) if pkt[1] else -1
                    
                    source_ip = pkt[2] or pkt[16] or "N/A"
                    destination_ip = pkt[3] or pkt[17] or "N/A"

                    if(source_ip in shared_state.ip_address):
                        outbound_bytes += length
                    elif(destination_ip in shared_state.ip_address):
                        inbound_bytes += length
                    
                    if time_rel > 0:
                        start_time = min(start_time, time_rel)
                        end_time = max(end_time, time_rel)


                    # Protocol Distribution
                    protocol_name = pkt[5] if pkt[5] else "N/A"
                    protocol_category = get_protocol_category(protocol_name)
                    shared_state.protocol_distribution[protocol_category] = shared_state.protocol_distribution.get(protocol_category, 0) + 1


                    # Jitter
                    rtp_ts_str = pkt[18] if pkt[18] else 0
                    arrival_time = time_rel
                    
                    if rtp_ts_str and arrival_time > 0 and seq is not None:
                        rtp_ts = int(rtp_ts_str)
                        
                        # DYNAMIC CLOCK RATE DETECTION (inline)
                        if jitter_state['clock_rate'] is None:
                            # Store packet for clock rate detection
                            jitter_state['packets_for_detection'].append({
                                'seq': seq,
                                'rtp_ts': rtp_ts,
                                'arrival': arrival_time
                            })
                            
                            # Try static payload type first
                            payload_type = pkt[19] if pkt[19] else None
                            if payload_type:
                                try:
                                    pt = int(payload_type)
                                    if pt in STATIC_PAYLOAD_RATES:
                                        jitter_state['clock_rate'] = STATIC_PAYLOAD_RATES[pt]
                                except ValueError:
                                    pass
                            
                            # If still no clock rate and we have enough packets, detect dynamically
                            if (jitter_state['clock_rate'] is None and len(jitter_state['packets_for_detection']) >= 2):
                                
                                detected_rate = detect_dynamic_clock_rate_inline(
                                    jitter_state['packets_for_detection']
                                )
                                if detected_rate:
                                    jitter_state['clock_rate'] = detected_rate
                                else:
                                    jitter_state['clock_rate'] = 8000  # Fallback
                        
                        # Calculate RFC 3550 jitter if we have clock rate
                        if jitter_state['clock_rate'] is not None:
                            clock_rate = jitter_state['clock_rate']
                            
                            # RFC 3550 jitter calculation (arrival order processing)
                            arrival_rtp = int(arrival_time * clock_rate)
                            transit = arrival_rtp - rtp_ts
                            
                            if jitter_state['prev_transit'] is not None:
                                d = abs(transit - jitter_state['prev_transit'])
                                # RFC 3550 formula with 1/16 smoothing
                                jitter_state['jitter'] = jitter_state['jitter'] + (d - jitter_state['jitter']) / 16
                            
                            jitter_state['prev_transit'] = transit
                        
                except (ValueError, IndexError):
                    continue
            
            # WEIGHTED JITTER CALCULATION: Weight by packet count
            if jitter_state['jitter'] > 0 and jitter_state['clock_rate']:
                # Convert jitter to milliseconds
                jitter_ms = (jitter_state['jitter'] / jitter_state['clock_rate']) * 1000
                
                # Weight by packet count (more packets = more influence)
                stream_weight = len(packet_list)
                
                # Add to total weighted jitter
                total_weighted_jitter += jitter_ms * stream_weight
                total_jitter_weight += stream_weight

        else:
            # Other protocols
            for pkt in packet_list:
                try:

                    # Throughput 
                    length = int(pkt[4]) if pkt[4] else 0
                    time_rel = float(pkt[1]) if pkt[1] else -1
                    
                    source_ip = pkt[2] or pkt[16] or "N/A"
                    destination_ip = pkt[3] or pkt[17] or "N/A"

                    if(source_ip in shared_state.ip_address):
                        outbound_bytes += length
                    elif(destination_ip in shared_state.ip_address):
                        inbound_bytes += length
                    
                    if time_rel > 0:
                        start_time = min(start_time, time_rel)
                        end_time = max(end_time, time_rel) 

                    # Protocol Distribution
                    protocol_name = pkt[5] if pkt[5] else "N/A"
                    protocol_category = get_protocol_category(protocol_name)
                    shared_state.protocol_distribution[protocol_category] = shared_state.protocol_distribution.get(protocol_category, 0) + 1

                except (ValueError, IndexError):
                    continue

    # Calculate final metrics

    # Throughput
    duration = max(end_time - start_time, 1e-6) if start_time != float("inf") else 1e-6
    duration = max(duration, 1.5) 

    in_throughput = ((inbound_bytes * 8) / duration) / 1000000 # Mbps
    out_throughput = ((outbound_bytes * 8) / duration) / 1000000

    # Packet Loss Count
    total_loss = total_tcp_retransmissions + total_rtp_loss

    # Packet Loss Percentage
    expected_rtp_packets += total_rtp_loss

    shared_state.lost_packets_total += total_loss
    shared_state.expected_packets_total += expected_tcp_packets + expected_rtp_packets
    packet_loss_percent = (shared_state.lost_packets_total * 100)/max(shared_state.expected_packets_total, 1)

    # Weighted Average Latency Calculation
    if total_weight > 0:
        latency = total_weighted_latency / total_weight  

    # WEIGHTED AVERAGE JITTER (more accurate than simple average)
    weighted_average_jitter = (total_weighted_jitter / total_jitter_weight if total_jitter_weight > 0 else 0.0)

    # Update metrics
    shared_state.metrics_state.update({
        "inbound_throughput": in_throughput,
        "outbound_throughput": out_throughput,
        "latency": latency,
        "jitter": weighted_average_jitter,
        "packet_loss_count": shared_state.lost_packets_total,
        "packet_loss_percent": packet_loss_percent,
        "last_update": datetime.now().isoformat(),
        "protocol_distribution": shared_state.protocol_distribution,
        "streamCount": streams_count,
        "totalPackets": total_packets
    })

    timing_end = time.perf_counter()  # ← Different name for timing, for checking purpose
    print(f"Metrics calculation took: {(timing_end - timing_start) * 1000:.2f}ms")
 
    return shared_state.metrics_state


def update_metrics_status(status):
    """Update the status in metrics state"""
    shared_state.metrics_state["status"] = status


def get_metrics_state():
    """Get current metrics state"""
    return shared_state.metrics_state.copy()
