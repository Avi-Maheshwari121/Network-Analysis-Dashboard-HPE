import json
import os
from dotenv import load_dotenv
import google.generativeai as genai
import shared_state


# --- AI Summary Setup ---
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("WARNING: GEMINI_API_KEY not found. AI summary will be disabled.")


# --- AI Summary Helper Functions ---
def analyze_session_history(history):
    if not history:
        return {}
    count = len(history)
    in_throughputs = [m['inbound_throughput'] for m in history]
    out_throughputs = [m['outbound_throughput'] for m in history]
    analysis = {
        "duration_seconds": count * shared_state.capture_duration,
        "total_packets_captured": history[-1].get("totalPackets", 0),
        "protocol_distribution": history[-1].get("protocol_distribution", {}),
        "throughput_stats_mbps": {
            "average_inbound": round(sum(in_throughputs) / len(in_throughputs), 2) if in_throughputs else 0,
            "peak_inbound": round(max(in_throughputs), 2) if in_throughputs else 0,
            "average_outbound": round(sum(out_throughputs) / len(out_throughputs), 2) if out_throughputs else 0,
            "peak_outbound": round(max(out_throughputs), 2) if out_throughputs else 0,
        }
    }
    return analysis


async def generate_summary():
    if not GEMINI_API_KEY:
        return "AI summary is unavailable. API key is not configured."
    session_analysis = analyze_session_history(shared_state.session_metrics_history)
    if not session_analysis:
        return "No data was captured to generate a summary."
    prompt = f"""
    You are a network analysis expert. Based on the following summary data from a network capture session, 
    provide a concise, easy-to-understand overview for a non-technical user.
    IMPORTANT: Do not use any markdown formatting (like **, ##, or lists). Write the entire summary as plain text with standard paragraphs.
    Focus on:
    1.  Overall Stability and Performance: Was the connection good, average, or problematic?
    2.  Key Observations: Mention any significant events like high latency spikes or packet loss.
    3.  Traffic Type: Briefly mention what the network was likely used for based on protocol distribution.
    Do not just list the numbers. Interpret them. For example, if peak latency is much higher than the average, point that out as a sign of instability.
    Data:
    {json.dumps(session_analysis, indent=2)}
    """
    try:
        model = genai.GenerativeModel('models/gemini-flash-latest')
        response = await model.generate_content_async(prompt)
        return response.text
    except Exception as e:
        print(f"CRITICAL: AI summary failed. Error: {e}. Returning a mock summary instead.")
        duration = session_analysis.get('duration_seconds', 0)
        packets = session_analysis.get('total_packets_captured', 0)
        mock_summary = (
            f"--- MOCK SUMMARY ---\n\n"
            f"The capture session lasted for approximately {int(duration)} seconds, capturing a total of {packets} packets.\n\n"
            f"(This is a placeholder summary. The AI model could not be reached.)"
        )
        return mock_summary