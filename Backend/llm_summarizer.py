import json
import os
from dotenv import load_dotenv
import google.generativeai as genai
import shared_state

# --- AI Setup ---
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("WARNING: GEMINI_API_KEY not found. AI summary will be disabled.")

# --- Helper Functions for Pre-Calculation ---

def _calculate_average(values):
    """Safely calculates the average of a list of numbers."""
    if not values:
        return 0
    # Filter out None or non-numeric types before summing
    numeric_values = [v for v in values if isinstance(v, (int, float))]
    if not numeric_values:
        return 0
    return round(sum(numeric_values) / len(numeric_values), 2)

def analyze_protocol_performance(history, special_metrics=None):
    """Analyzes a protocol's history for throughputs and special metrics like latency or jitter."""
    if special_metrics is None:
        special_metrics = []
    if not history:
        analysis = {'average_inbound_throughput_mbps': 0, 'average_outbound_throughput_mbps': 0}
        for metric in special_metrics:
            analysis[f'average_{metric}_ms'] = 0
        return analysis
    inbound = [m.get('inbound_throughput', 0) for m in history]
    outbound = [m.get('outbound_throughput', 0) for m in history]
    analysis = {
        'average_inbound_throughput_mbps': _calculate_average(inbound),
        'average_outbound_throughput_mbps': _calculate_average(outbound),
    }
    for metric in special_metrics:
        values = [m.get(metric, 0) for m in history if m.get(metric) is not None]
        analysis[f'average_{metric}_ms'] = _calculate_average(values)
    return analysis

# --- Main Summary Generator ---

async def generate_summary():
    """
    Generates a network session summary by pre-calculating all metrics
    and then passing them to the AI for formatting.
    """
    if not GEMINI_API_KEY:
        return {"summary": "AI summary is unavailable. API key is not configured.", "breakdown": []}
    if not shared_state.session_metrics_history:
        return {"summary": "No data was captured to generate a summary.", "breakdown": []}

    # 1. Get Session Duration and Final Packet Distribution
    duration = shared_state.session_duration_final if hasattr(shared_state, 'session_duration_final') and shared_state.session_duration_final > 0 else len(shared_state.session_metrics_history) * shared_state.capture_duration
    final_distribution = shared_state.session_metrics_history[-1].get("protocol_distribution", {})
    total_packets_overall = sum(final_distribution.values())

    # 2. Pre-calculate Overall Throughput and Goodput
    overall_in_thr = [m.get('inbound_throughput', 0) for m in shared_state.session_metrics_history]
    overall_out_thr = [m.get('outbound_throughput', 0) for m in shared_state.session_metrics_history]
    overall_in_good = [m.get('inbound_goodput', 0) for m in shared_state.session_metrics_history]
    overall_out_good = [m.get('outbound_goodput', 0) for m in shared_state.session_metrics_history]
    overall_throughput_data = {
        "total_packets": total_packets_overall,
        "average_pps": round(total_packets_overall / duration, 2) if duration > 0 else 0,
        "average_inbound_throughput_mbps": _calculate_average(overall_in_thr),
        "average_outbound_throughput_mbps": _calculate_average(overall_out_thr),
        "average_inbound_goodput_mbps": _calculate_average(overall_in_good),
        "average_outbound_goodput_mbps": _calculate_average(overall_out_good),
    }

    # 3. Use final cumulative IP Composition values directly from shared_state
    ipv4_cumulative = shared_state.ip_composition.get("ipv4_packets_cumulative", 0)
    ipv6_cumulative = shared_state.ip_composition.get("ipv6_packets_cumulative", 0)
    total_ip_packets = shared_state.ip_composition.get("total_packets", 0)
    ipv4_percentage = shared_state.ip_composition.get("ipv4_percentage", 0)
    ipv6_percentage = shared_state.ip_composition.get("ipv6_percentage", 0)
    
    ip_composition_data = {
        "total_packets": total_ip_packets,
        "ipv4_packets": ipv4_cumulative,
        "ipv6_packets": ipv6_cumulative,
        "ipv4_percentage": round(ipv4_percentage,2),
        "ipv6_percentage": round(ipv6_percentage, 2),
    }
    
   # 4. Pre-calculate final Encryption Composition from shared_state
    encrypted_cumulative = shared_state.encryption_composition.get("encrypted_packets_cumulative", 0)
    unencrypted_cumulative = shared_state.encryption_composition.get("unencrypted_packets_cumulative", 0)
    total_encryption_packets = shared_state.encryption_composition.get("total_packets", 0)
    encrypted_percentage = shared_state.encryption_composition.get("encrypted_percentage", 0)
    unencrypted_percentage = shared_state.encryption_composition.get("unencrypted_percentage", 0)

    encryption_composition_data = {
        "total_packets": total_encryption_packets,
        "encrypted_packets": encrypted_cumulative,
        "unencrypted_packets": unencrypted_cumulative,
        "encrypted_percentage": round(encrypted_percentage,2),
        "unencrypted_percentage": round(unencrypted_percentage,2),
    }

    # 5. Pre-calculate all performance metrics for each protocol
    protocol_map = {
        'TCP': (analyze_protocol_performance(shared_state.tcp_metrics_history, ['latency']), shared_state.tcp_metrics),
        'RTP': (analyze_protocol_performance(shared_state.rtp_metrics_history, ['jitter']), shared_state.rtp_metrics),
        'UDP': (analyze_protocol_performance(shared_state.udp_metrics_history), shared_state.udp_metrics),
        'QUIC': (analyze_protocol_performance(shared_state.quic_metrics_history), shared_state.quic_metrics),
        'DNS': (analyze_protocol_performance(shared_state.dns_metrics_history), shared_state.dns_metrics),
        'IGMP': (analyze_protocol_performance(shared_state.igmp_metrics_history), shared_state.igmp_metrics),
    }
    protocol_data = {}
    for proto_name, (analysis_data, final_metrics) in protocol_map.items():
        total_packets = final_distribution.get(proto_name, 0)
        protocol_data[proto_name] = {
            "total_packets": total_packets,
            "average_pps": round(total_packets / duration, 2) if duration > 0 else 0,
            **analysis_data
        }

        if proto_name == 'TCP':
            protocol_data[proto_name]['total_retransmissions'] = final_metrics.get('packet_loss', 0)
            protocol_data[proto_name]['retansmission_percentage'] = round(final_metrics.get('packet_loss_percentage', 0), 2)
        
        if proto_name == 'RTP':
            protocol_data[proto_name]['total_packet_loss'] = final_metrics.get('packet_loss', 0)
            protocol_data[proto_name]['packet_loss_percentage'] = round(final_metrics.get('packet_loss_percentage', 0), 2)

    # 6. Assemble the data payload for the AI
    full_analysis = {
        "session_duration_seconds": round(duration, 2),
        "overall_throughput": overall_throughput_data,
        "ip_composition": ip_composition_data,
        "encryption_composition": encryption_composition_data,
        "protocol_data": protocol_data,
    }

    # 7. Create a new, highly specific prompt for the AI
    prompt = f"""
    You are an expert network analyst who formats pre-calculated data into a JSON report.
    Your entire response MUST be a single, valid JSON object with "summary" and "breakdown" keys.

    **INSTRUCTIONS:**
    1.  **summary**: Write a one-paragraph overview of the network session based on the provided data.
    2.  **breakdown**: Create a JSON array. Each object in the array MUST have three keys: `protocol`, `keyMetrics`, and `observations`.
    3.  **`protocol` key**: The value must be a string with the name of the metric category (e.g., "Overall Throughput", "IP Composition", "TCP").
    4.  **`keyMetrics` key**: The value MUST be a single multi-line string, with each metric on a new line (using '\\n').
    5.  **`observations` key**: The value must be a single, concise sentence providing a key insight about the metrics for that category (e.g., "Traffic was exclusively IPv4.").
    6.  For the **"Overall Throughput"** object, the `keyMetrics` string must contain: Total Packets, Average PPS, Average Inbound/Outbound Throughput, and Average Inbound/Outbound Goodput.
    7.  For the **"IP Composition"** object, the `keyMetrics` string must contain: Total IPv4 Packets (with percentage) and Total IPv6 Packets (with percentage).
    8.  For the **"Encryption Composition"** object, the `keyMetrics` string must contain: Total Encrypted Packets (with percentage) and Total Unencrypted Packets (with percentage).
    9.  For the **"TCP"** object, the `keyMetrics` string must contain: Total Packets, Average PPS, Average Inbound/Outbound Throughput, Average Latency, Total Retransmissions, and Retransmission Percentage.
    10. For the **"RTP"** object, the `keyMetrics` string must contain: Total Packets, Average PPS, Average Inbound/Outbound Throughput, Average Jitter, Total Packet Loss, and Packet Loss Percentage.
    11. For all other protocols, the `keyMetrics` string must contain: Total Packets, Average PPS, and Average Inbound/Outbound Throughput.
    12. **You MUST NOT perform any calculations.** Your only job is to format the provided data and add a brief observation. Do not return an object for `keyMetrics`.
    13. You MUST generate a breakdown object for every protocol present in the protocol_data input, even if its total_packets count is 0.

    **Pre-Calculated Data for Formatting:**
    {json.dumps(full_analysis, indent=2)}
    """

    # 8. Call the AI and parse the response
    try:
        model = genai.GenerativeModel('models/gemini-flash-latest')
        response = await model.generate_content_async(prompt)
        raw_text = response.text
        json_start = raw_text.find('{')
        json_end = raw_text.rfind('}') + 1
        if json_start != -1 and json_end != 0:
            clean_json_str = raw_text[json_start:json_end]
            return json.loads(clean_json_str)
        else:
            raise ValueError("No valid JSON object found in AI response.")
    except Exception as e:
        print(f"CRITICAL: AI summary failed or returned invalid JSON. Error: {e}.")
        return {"summary": "The AI model could not be reached or failed to process the data.", "breakdown": []}