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


def _calculate_stats_for_metric(history, metric_name):
    """Calculates stats for a given metric from a history list."""
    values = [m.get(metric_name, 0) for m in history if m.get(metric_name)]
    if not values:
        return None
    return {
        "average": round(sum(values) / len(values), 2),
        "peak": round(max(values), 2),
        "min": round(min(values), 2),
    }

def analyze_protocol_history(protocol_history, metrics_to_analyze):
    """Calculates stats for a list of specified metrics (e.g., ['latency', 'jitter'])."""
    if not protocol_history:
        return {}
    analysis = {}
    for metric in metrics_to_analyze:
        stats = _calculate_stats_for_metric(protocol_history, metric)
        if stats:
            analysis[f"{metric}_ms"] = stats
    return analysis

def analyze_session_history(history):
    """Analyzes the time-series history of overall metrics."""
    if not history:
        return {}
    analysis = {
        "duration_seconds": len(history) * shared_state.capture_duration,
        "total_packets_captured": history[-1].get("totalPackets", 0),
        # This is the key: pass the protocol_distribution from the *last* history entry
        "protocol_distribution": history[-1].get("protocol_distribution", {}),
    }
    analysis["inbound_throughput_mbps"] = _calculate_stats_for_metric(history, 'inbound_throughput')
    analysis["outbound_throughput_mbps"] = _calculate_stats_for_metric(history, 'outbound_throughput')
    return analysis

# --- Main Summary Generator ---

async def generate_summary():
    """
    Generates a network session summary as a JSON object suitable for a React frontend.
    """
    if not GEMINI_API_KEY:
        return {"summary": "AI summary is unavailable. API key is not configured.", "breakdown": []}

    session_analysis = analyze_session_history(shared_state.session_metrics_history)
    if not session_analysis:
        return {"summary": "No data was captured to generate a summary.", "breakdown": []}

    tcp_stats = analyze_protocol_history(shared_state.tcp_metrics_history, ['latency'])
    rtp_stats = analyze_protocol_history(shared_state.rtp_metrics_history, ['jitter'])

    protocol_average_pps = {}
    duration = session_analysis.get("duration_seconds", 0)
    if duration > 0:
        distribution = session_analysis.get("protocol_distribution", {})
        for protocol, count in distribution.items():
            if count > 0:
                protocol_average_pps[protocol.upper()] = round(count / duration, 1)
    
    # 1. Gather ALL metrics, including new ones
    full_analysis = {
        "overall_metrics": session_analysis,
        "protocol_specific_metrics": {
            "TCP": {**shared_state.tcp_metrics, **tcp_stats},
            "RTP": {**shared_state.rtp_metrics, **rtp_stats},
            "UDP": shared_state.udp_metrics,
            "QUIC": shared_state.quic_metrics,
            "DNS": shared_state.dns_metrics,
            "IGMP": shared_state.igmp_metrics,
            "IP_Composition": shared_state.ip_composition,
        },
        "protocol_average_pps": protocol_average_pps
    }

    # 2. Update the prompt with new instructions
    prompt = f"""
    You are an expert network analyst. Your entire response MUST be a single, valid JSON object.
    The JSON object must have two keys:
    1. "summary": A string containing a crisp paragraph that summarizes the network session's stability and performance.
    2. "breakdown": An array of objects. Each object represents a protocol and must have three keys: "protocol" (string), "keyMetrics" (string), and "observations" (string).

    INSTRUCTIONS FOR "breakdown" ARRAY:
    1.  You MUST include *separate* objects for: "Overall Throughput", "IP Composition", "TCP", "UDP", "RTP", "QUIC", "DNS", and "IGMP".
    2.  Do NOT group protocols (e.g., 'TCP and RTP') into a single object, even if their data is zero.
    3.  For PACKET COUNTS (e.g., "Total Packets (15)"): Use the values from `overall_metrics.protocol_distribution`. This is the source of truth for packet counts.
    4.  For PERFORMANCE METRICS (e.g., "Average Latency (21.32 ms)"): Use the values from `protocol_specific_metrics` (e.g., `TCP.latency_ms.average`, `RTP.jitter_ms.average`).
    5.  For "IP Composition": Make sure to report the `ipv4_packets_cumulative` and `ipv6_packets_cumulative` values.
    6.  If data for a protocol is minimal or zero, state that in the observations for its own, separate object.
    7.  For AVERAGE PPS: Use the pre-calculated values from the `protocol_average_pps` object. Include it in the `keyMetrics` string (e.g., 'Packets per Second (2088.6)'). If a protocol is not in the `protocol_average_pps` object, do not mention PPS.
    Data for Analysis:
    {json.dumps(full_analysis, indent=2)}
    """

    # 3. Call the AI and parse the JSON response
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
            "breakdown": [{
                "protocol": "Analysis Status",
                "keyMetrics": "Error",
                "observations": "The AI summary service failed to return a valid analysis. This is a placeholder message."
            }]
        }

