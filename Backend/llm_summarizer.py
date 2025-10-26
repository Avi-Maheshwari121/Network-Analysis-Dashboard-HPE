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
    return round(sum(values) / len(values), 2)

def analyze_protocol_performance(history, special_metrics=None):
    """
    Analyzes a protocol's history list to calculate average throughputs
    and any special metrics like latency or jitter.
    """
    if special_metrics is None:
        special_metrics = []
        
    if not history:
        # Return a default structure if no history is available
        analysis = {
            'average_inbound_throughput_mbps': 0,
            'average_outbound_throughput_mbps': 0,
        }
        for metric in special_metrics:
            analysis[f'average_{metric}_ms'] = 0
        return analysis

    inbound_throughputs = [m.get('inbound_throughput', 0) for m in history]
    outbound_throughputs = [m.get('outbound_throughput', 0) for m in history]
    
    analysis = {
        'average_inbound_throughput_mbps': _calculate_average(inbound_throughputs),
        'average_outbound_throughput_mbps': _calculate_average(outbound_throughputs),
    }

    # Calculate special metrics like latency or jitter
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

    # 1. Calculate Session Duration and Final Packet Distribution
    if hasattr(shared_state, 'session_duration_final') and shared_state.session_duration_final > 0:
        duration = shared_state.session_duration_final
    else:
        duration = len(shared_state.session_metrics_history) * shared_state.capture_duration
    final_distribution = shared_state.session_metrics_history[-1].get("protocol_distribution", {})

    # 2. Pre-calculate all performance metrics for each protocol
    tcp_analysis = analyze_protocol_performance(shared_state.tcp_metrics_history, ['latency'])
    rtp_analysis = analyze_protocol_performance(shared_state.rtp_metrics_history, ['jitter'])
    udp_analysis = analyze_protocol_performance(shared_state.udp_metrics_history)
    quic_analysis = analyze_protocol_performance(shared_state.quic_metrics_history)
    dns_analysis = analyze_protocol_performance(shared_state.dns_metrics_history)
    igmp_analysis = analyze_protocol_performance(shared_state.igmp_metrics_history)

    # 3. Assemble the complete, pre-calculated data payload for the AI
    full_analysis = {
        "session_duration_seconds": round(duration, 2),
        "protocol_data": {}
    }

    protocol_map = {
        'TCP': (tcp_analysis, shared_state.tcp_metrics_history),
        'RTP': (rtp_analysis, shared_state.rtp_metrics_history),
        'UDP': (udp_analysis, shared_state.udp_metrics_history),
        'QUIC': (quic_analysis, shared_state.quic_metrics_history),
        'DNS': (dns_analysis, shared_state.dns_metrics_history),
        'IGMP': (igmp_analysis, shared_state.igmp_metrics_history)
    }

    for proto_name, (analysis_data, history) in protocol_map.items():
        total_packets = final_distribution.get(proto_name, 0)
        
        # Only add protocol to analysis if it has packets
        if total_packets > 0:
            full_analysis["protocol_data"][proto_name] = {
                "total_packets": total_packets,
                "average_pps": round(total_packets / duration, 2) if duration > 0 else 0,
                **analysis_data
            }

    # 4. Create a focused prompt for the AI
    prompt = f"""
    You are an expert network analyst. Your task is to format the provided pre-calculated data into a human-readable JSON summary.
    Your entire response MUST be a single, valid JSON object with two keys: "summary" and "breakdown".

    **INSTRUCTIONS:**
    1.  **"summary"**: Write a crisp, one-paragraph overview of the network session's performance based on the data.
    2.  **"breakdown"**: Create a JSON array. For each protocol in the `protocol_data` object you receive, create a corresponding object in the array with three keys: "protocol", "keyMetrics", and "observations".
    3.  **"keyMetrics"**: For each protocol, format the provided data into a string. You MUST include:
        - Total Packets
        - Average PPS (not for overall throughput), Use the values from `overall_metrics.protocol_distribution` for protocol packets amount and divide it by time duration.
        - Average Inbound Throughput
        - Average Outbound Throughput
        - For TCP, you MUST also include Average Latency.
        - For RTP, you MUST also include Average Jitter.
    4.  **DO NOT perform any calculations.** Simply present the data provided below in the specified format.
    5.  You MUST include *separate* objects for: "Overall Throughput", "IP Composition", "TCP", "UDP", "RTP", "QUIC", "DNS", and "IGMP".
    6.  Do NOT group protocols (e.g., 'TCP and RTP') into a single object, even if their data is zero.
    7.  For "IP Composition": Make sure to report the `ipv4_packets_cumulative` and `ipv6_packets_cumulative` values with their respective percentages
    8.  For PACKET COUNTS (e.g., "Total Packets (15)"): Use the values from `overall_metrics.protocol_distribution`. This is the source of truth for packet counts.

    **Pre-Calculated Data for Formatting:**
    {json.dumps(full_analysis, indent=2)}
    """

    # 5. Call the AI and parse the response
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
        return {
            "summary": "The AI model could not be reached or failed to process the data. Please check the backend console for more details.",
            "breakdown": []
        }