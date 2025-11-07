import json
import os
from dotenv import load_dotenv
import google.generativeai as genai
import shared_state
from datetime import datetime

# --- AI Setup ---
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("WARNING: GEMINI_API_KEY not found. AI summary will be disabled.")


def _format_throughput(bits):
    """Converts raw bits to a human-readable string with the best unit."""
    if bits == 0:
        return "0.0 bps"
    
    gbps = 1_000_000_000
    mbps = 1_000_000
    kbps = 1_000
    
    if bits >= gbps:
        return f"{round(bits / gbps, 2)} Gbps"
    elif bits >= mbps:
        return f"{round(bits / mbps, 2)} Mbps"
    elif bits >= kbps:
        return f"{round(bits / kbps, 2)} Kbps"
    else:
        return f"{round(bits, 2)} bps"
    

def analyze_protocol_performance(protocol_metrics, special_metrics=None):
    """
    Analyzes protocol performance using pre-calculated averages from _running_state.
    No history arrays needed.
    """
    if special_metrics is None:
        special_metrics = []

    # Get averages directly from protocol_metrics (which has _peak and _avg fields)
    analysis = {
        'average_inbound_throughput': _format_throughput(
            protocol_metrics.get('inbound_throughput_avg', 0)
        ),
        'average_outbound_throughput': _format_throughput(
            protocol_metrics.get('outbound_throughput_avg', 0)
        ),
    }

    # Add special metrics (latency/jitter) if present
    for metric in special_metrics:
        avg_value = protocol_metrics.get(f'{metric}_avg', 0)
        analysis[f'average_{metric}_ms'] = round(avg_value, 2)

    return analysis
    

# --- Main Summary Generator ---
async def generate_summary():
    """
    Generates a network session summary by pre-calculating all metrics
    and then passing them to the AI for formatting.
    """
    if not GEMINI_API_KEY:
        return {"summary": "AI summary is unavailable. API key is not configured.", "breakdown": []}
    
    if not hasattr(shared_state, 'session_start_time') or shared_state.session_start_time is None:
        return {"summary": "No data was captured to generate a summary.", "breakdown": []}

    # 1. Get Session Duration and Final Packet Distribution
    duration = shared_state.session_duration_final if hasattr(shared_state, 'session_duration_final') and shared_state.session_duration_final > 0 else (datetime.now() - shared_state.session_start_time).total_seconds()
    final_distribution = shared_state.metrics_state.get("protocol_distribution", {})
    total_packets_overall = sum(final_distribution.values())

    # 2. Pre-calculate Overall Throughput and Goodput
    overall_throughput_data = {
        "total_packets": total_packets_overall,
        "average_pps": f"{round(total_packets_overall / duration, 2) if duration > 0 else 0} PPS",
        "average_inbound_throughput": _format_throughput(
            shared_state.metrics_state.get('inbound_throughput_avg', 0)
        ),
        "average_outbound_throughput": _format_throughput(
            shared_state.metrics_state.get('outbound_throughput_avg', 0)
        ),
        "average_inbound_goodput": _format_throughput(
            shared_state.metrics_state.get('inbound_goodput_avg', 0)
        ),
        "average_outbound_goodput": _format_throughput(
            shared_state.metrics_state.get('outbound_goodput_avg', 0)
        ),
    }

    # 3. Use final cumulative IP Composition values directly from shared_state
    ipv4_cumulative = shared_state.ip_composition.get("ipv4_packets_cumulative", 0)
    ipv6_cumulative = shared_state.ip_composition.get("ipv6_packets_cumulative", 0)
    total_ip_packets = ipv4_cumulative + ipv6_cumulative
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
    total_encryption_packets = encrypted_cumulative + unencrypted_cumulative
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
        'TCP': (analyze_protocol_performance(shared_state.tcp_metrics, ['latency']), shared_state.tcp_metrics),
        'RTP': (analyze_protocol_performance(shared_state.rtp_metrics, ['jitter']), shared_state.rtp_metrics),
        'UDP': (analyze_protocol_performance(shared_state.udp_metrics), shared_state.udp_metrics),
        'QUIC': (analyze_protocol_performance(shared_state.quic_metrics), shared_state.quic_metrics),
        'DNS': (analyze_protocol_performance(shared_state.dns_metrics), shared_state.dns_metrics),
        'IGMP': (analyze_protocol_performance(shared_state.igmp_metrics), shared_state.igmp_metrics),
    }
    protocol_data = {}
    for proto_name, (analysis_data, final_metrics) in protocol_map.items():
        total_packets = final_distribution.get(proto_name, 0)
        protocol_data[proto_name] = {
            "total_packets": total_packets,
            "average_pps": f"{round(total_packets / duration, 2) if duration > 0 else 0} PPS",
            **analysis_data
        }

        if proto_name == 'TCP':
            protocol_data[proto_name]['total_retransmissions'] = final_metrics.get('packet_loss', 0)
            protocol_data[proto_name]['retransmission_percentage'] = f"{round(final_metrics.get('packet_loss_percentage', 0), 2)} %"
            protocol_data[proto_name]['average_latency'] = f"{analysis_data.get('average_latency_ms', 0)} ms"
        
        if proto_name == 'RTP':
            protocol_data[proto_name]['total_packet_loss'] = final_metrics.get('packet_loss', 0)
            protocol_data[proto_name]['packet_loss_percentage'] = f"{round(final_metrics.get('packet_loss_percentage', 0), 2)} %"
            protocol_data[proto_name]['average_jitter'] = f"{analysis_data.get('average_jitter_ms', 0)} ms"

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
    4.  **`keyMetrics` key**: The value MUST be a single multi-line string. Each line MUST be in a 'Key: Value' format (e.g., 'Total Packets: 1728\nAverage PPS: 192.0 PPS'). Use the metric names from the instructions below as the keys. You MUST include the units (e.g., PPS, ms, %, Kbps, Mbps) as provided in the data.
    5.  **`observations` key**: The value must be a single, concise sentence providing a key insight about the metrics for that category (e.g., "Traffic was exclusively IPv4.").
    6.  For the **"Overall Throughput"** object, the `keyMetrics` string must contain: Total Packets, Average PPS, Average Inbound Throughput, Average Outbound Throughput, Average Inbound Goodput, and Average Outbound Goodput. The values for PPS and throughput/goodput already include their units.
    7.  For the **"IP Composition"** object, the `keyMetrics` string must contain: Total IP Packets, Total IPv4 Packets (with percentage) and Total IPv6 Packets (with percentage).
    8.  For the **"Encryption Composition"** object, the `keyMetrics` string must contain: Total Encrypted Packets (with percentage) and Total Unencrypted Packets (with percentage).
    9.  For the **"TCP"** object, the `keyMetrics` string must contain: Total Packets, Average PPS, Average Inbound Throughput, Average Outbound Throughput, Average Latency, Total Retransmissions, and Retransmission Percentage. The values for PPS, latency, throughput, and percentage already include their units.
    10. For the **"RTP"** object, the `keyMetrics` string must contain: Total Packets, Average PPS, Average Inbound Throughput, Average Outbound Throughput, Average Jitter, Total Packet Loss, and Packet Loss Percentage. The values for PPS, jitter, throughput, and percentage already include their units.
    11. For all other protocols, the `keyMetrics` string must contain: Total Packets, Average PPS, Average Inbound Throughput, and Average Outbound Throughput. The values for PPS and throughput already include their units.
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