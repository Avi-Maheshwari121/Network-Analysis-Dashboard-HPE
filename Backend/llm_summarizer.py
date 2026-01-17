"""
LLM-based network session summarizer using Gemini.
Generates final and periodic summaries from shared metrics state.
"""

import json
import os
from datetime import datetime

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


def _format_throughput(bits):
    """Converts raw bits to a human-readable string with the best unit."""
    if bits == 0:
        return "0.0 bps"

    gbps = 1_000_000_000
    mbps = 1_000_000
    kbps = 1_000

    if bits >= gbps:
        return f"{round(bits / gbps, 2)} Gbps"
    if bits >= mbps:
        return f"{round(bits / mbps, 2)} Mbps"
    if bits >= kbps:
        return f"{round(bits / kbps, 2)} Kbps"

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
    duration = (shared_state.session_duration_final
                if hasattr(shared_state, 'session_duration_final')
                and shared_state.session_duration_final > 0
                else (datetime.now() - shared_state.session_start_time).total_seconds()
    )
    final_distribution = shared_state.metrics_state.get("protocol_distribution", {})
    total_packets_overall = sum(final_distribution.values())

    # 2. Pre-calculate Overall Throughput and Goodput
    overall_throughput_data = {
        "total_packets": total_packets_overall,
        "average_pps": (
            f"{round(total_packets_overall / duration, 2) if duration > 0 else 0} PPS"
        ),
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
    encryption_state = shared_state.encryption_composition
    encrypted_cumulative = encryption_state.get("encrypted_packets_cumulative", 0)
    unencrypted_cumulative = encryption_state.get("unencrypted_packets_cumulative", 0)
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
        'TCP': (analyze_protocol_performance(
            shared_state.tcp_metrics, ['latency']),
            shared_state.tcp_metrics),
        'RTP': (analyze_protocol_performance(
            shared_state.rtp_metrics, ['jitter']),
            shared_state.rtp_metrics),
        'UDP': (analyze_protocol_performance(
            shared_state.udp_metrics),
            shared_state.udp_metrics),
        'QUIC': (analyze_protocol_performance(
            shared_state.quic_metrics),
            shared_state.quic_metrics),
        'DNS': (analyze_protocol_performance(
            shared_state.dns_metrics),
            shared_state.dns_metrics),
        'IGMP': (analyze_protocol_performance(
            shared_state.igmp_metrics),
            shared_state.igmp_metrics),
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
            protocol_data[proto_name]['total_retransmissions'] = (
                final_metrics.get('packet_loss', 0)
            )
            protocol_data[proto_name]['retransmission_percentage'] = (
                f"{round(final_metrics.get('packet_loss_percentage', 0), 2)} %"
            )
            protocol_data[proto_name]['average_latency'] = (
                f"{analysis_data.get('average_latency_ms', 0)} ms"
            )

        if proto_name == 'RTP':
            protocol_data[proto_name]['total_packet_loss'] = (
                final_metrics.get('packet_loss', 0)
            )
            protocol_data[proto_name]['packet_loss_percentage'] = (
                f"{round(final_metrics.get('packet_loss_percentage', 0), 2)} %"
            )
            protocol_data[proto_name]['average_jitter'] = (
                f"{analysis_data.get('average_jitter_ms', 0)} ms"
            )

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

        raise ValueError("No valid JSON object found in AI response.")
    except (
        TimeoutError,
        RuntimeError,
        ValueError,
        TypeError,
        json.JSONDecodeError,
    ) as e:
        print(f"CRITICAL: AI summary failed or returned invalid JSON. Error: {e}.")
        return {
            "summary": "The AI model could not be reached or failed to process the data.",
            "breakdown": []
        }


def safe_get(d, *path, default=0.0):
    """Safely obtain value"""
    cur = d
    for k in path:
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    return cur


async def generate_periodic_summary():
    """Generate a short AI-based periodic network status summary."""

    if not GEMINI_API_KEY:
        return {"summary": "AI summary is unavailable.", "timestamp": datetime.now().isoformat()}

    if not hasattr(shared_state, 'session_start_time') or shared_state.session_start_time is None:
        return {"summary": "No data available.", "timestamp": datetime.now().isoformat()}

    # Calculate current session duration
    duration = (datetime.now() - shared_state.session_start_time).total_seconds()

    # Get protocol distribution and total packets
    final_distribution = shared_state.metrics_state.get("protocol_distribution", {})
    total_packets = sum(final_distribution.values())

    # Get top 3 protocols
    sorted_protocols = sorted(final_distribution.items(), key=lambda x: x[1], reverse=True)
    top_3_protocols = sorted_protocols[:3] if len(sorted_protocols) >= 3 else sorted_protocols

    # Helper function to safely get nested values
    rs = getattr(shared_state, "running_state", {})

    # === OVERALL METRICS - average only ===
    overall_in_avg = safe_get(rs, "overall", "inbound_throughput_avg")
    overall_out_avg = safe_get(rs, "overall", "outbound_throughput_avg")

    # === TCP METRICS - average only ===
    tcp_in_avg = safe_get(rs, "tcp", "inbound_throughput_avg")
    tcp_out_avg = safe_get(rs, "tcp", "outbound_throughput_avg")
    tcp_lat_avg = safe_get(rs, "tcp", "latency_avg")
    tcp_loss_cnt = shared_state.tcp_metrics.get("packet_loss", 0)
    tcp_loss_pct = shared_state.tcp_metrics.get("packet_loss_percentage", 0.0)

    # === RTP METRICS - average only ===
    rtp_in_avg = safe_get(rs, "rtp", "inbound_throughput_avg")
    rtp_out_avg = safe_get(rs, "rtp", "outbound_throughput_avg")
    rtp_jit_avg = safe_get(rs, "rtp", "jitter_avg")
    rtp_loss_cnt = shared_state.rtp_metrics.get("packet_loss", 0)
    rtp_loss_pct = shared_state.rtp_metrics.get("packet_loss_percentage", 0.0)

    # === UDP METRICS - average only ===
    udp_in_avg = safe_get(rs, "udp", "inbound_throughput_avg")
    udp_out_avg = safe_get(rs, "udp", "outbound_throughput_avg")

    # === QUIC METRICS - average only ===
    quic_in_avg = safe_get(rs, "quic", "inbound_throughput_avg")
    quic_out_avg = safe_get(rs, "quic", "outbound_throughput_avg")

    # === DNS METRICS - average only ===
    dns_in_avg = safe_get(rs, "dns", "inbound_throughput_avg")
    dns_out_avg = safe_get(rs, "dns", "outbound_throughput_avg")

    # === IGMP METRICS - average only ===
    igmp_in_avg = safe_get(rs, "igmp", "inbound_throughput_avg")
    igmp_out_avg = safe_get(rs, "igmp", "outbound_throughput_avg")

    # === IP COMPOSITION ===
    ipv4_cumulative = shared_state.ip_composition.get("ipv4_packets_cumulative", 0)
    ipv6_cumulative = shared_state.ip_composition.get("ipv6_packets_cumulative", 0)
    ipv4_pct = shared_state.ip_composition.get("ipv4_percentage", 0)
    ipv6_pct = shared_state.ip_composition.get("ipv6_percentage", 0)

    # === ENCRYPTION COMPOSITION ===
    encrypted_cumulative = (
        shared_state.encryption_composition.get("encrypted_packets_cumulative", 0)
    )
    unencrypted_cumulative = (
        shared_state.encryption_composition.get("unencrypted_packets_cumulative", 0)
    )
    encrypted_pct = (
        shared_state.encryption_composition.get("encrypted_percentage", 0)
    )
    unencrypted_pct = (
        shared_state.encryption_composition.get("unencrypted_percentage", 0)
    )

    # === BUILD PROTOCOL_DATA - simplified (no peak, no goodput) ===
    protocol_data = {}

    # TCP
    tcp_packets = final_distribution.get("TCP", 0)
    protocol_data['TCP'] = {
        "total_packets": tcp_packets,
        "average_pps": f"{round(tcp_packets / duration, 2) if duration > 0 else 0} PPS",
        "average_inbound_throughput": _format_throughput(tcp_in_avg),
        "average_outbound_throughput": _format_throughput(tcp_out_avg),
        "average_latency": f"{round(tcp_lat_avg, 2)} ms",
        "total_retransmissions": int(tcp_loss_cnt),
        "retransmission_percentage": f"{round(tcp_loss_pct, 2)} %",
    }

    # RTP
    rtp_packets = final_distribution.get("RTP", 0)
    protocol_data['RTP'] = {
        "total_packets": rtp_packets,
        "average_pps": f"{round(rtp_packets / duration, 2) if duration > 0 else 0} PPS",
        "average_inbound_throughput": _format_throughput(rtp_in_avg),
        "average_outbound_throughput": _format_throughput(rtp_out_avg),
        "average_jitter": f"{round(rtp_jit_avg, 2)} ms",
        "total_packet_loss": int(rtp_loss_cnt),
        "packet_loss_percentage": f"{round(rtp_loss_pct, 2)} %",
    }

    # UDP
    udp_packets = final_distribution.get("UDP", 0)
    protocol_data['UDP'] = {
        "total_packets": udp_packets,
        "average_pps": f"{round(udp_packets / duration, 2) if duration > 0 else 0} PPS",
        "average_inbound_throughput": _format_throughput(udp_in_avg),
        "average_outbound_throughput": _format_throughput(udp_out_avg),
    }

    # QUIC
    quic_packets = final_distribution.get("QUIC", 0)
    protocol_data['QUIC'] = {
        "total_packets": quic_packets,
        "average_pps": f"{round(quic_packets / duration, 2) if duration > 0 else 0} PPS",
        "average_inbound_throughput": _format_throughput(quic_in_avg),
        "average_outbound_throughput": _format_throughput(quic_out_avg),
    }

    # DNS
    dns_packets = final_distribution.get("DNS", 0)
    protocol_data['DNS'] = {
        "total_packets": dns_packets,
        "average_pps": f"{round(dns_packets / duration, 2) if duration > 0 else 0} PPS",
        "average_inbound_throughput": _format_throughput(dns_in_avg),
        "average_outbound_throughput": _format_throughput(dns_out_avg),
    }

    # IGMP
    igmp_packets = final_distribution.get("IGMP", 0)
    protocol_data['IGMP'] = {
        "total_packets": igmp_packets,
        "average_pps": f"{round(igmp_packets / duration, 2) if duration > 0 else 0} PPS",
        "average_inbound_throughput": _format_throughput(igmp_in_avg),
        "average_outbound_throughput": _format_throughput(igmp_out_avg),
    }

    # Prepare comprehensive data for AI (used ONLY for prompt, NOT sent to user)
    periodic_data = {
        "session_duration_seconds": round(duration, 2),
        "total_packets_captured": total_packets,
        "average_pps": round(total_packets / duration, 2) if duration > 0 else 0,

        "top_3_protocols": [{"protocol": p[0], "packets": p[1]} for p in top_3_protocols],

        # Overall metrics - average only
        "overall": {
            "inbound_throughput_avg": _format_throughput(overall_in_avg),
            "outbound_throughput_avg": _format_throughput(overall_out_avg),
        },

        # IP composition
        "ip_composition": {
            "ipv4_packets": ipv4_cumulative,
            "ipv6_packets": ipv6_cumulative,
            "ipv4_percentage": round(ipv4_pct, 2),
            "ipv6_percentage": round(ipv6_pct, 2),
        },

        # Encryption composition
        "encryption": {
            "encrypted_packets": encrypted_cumulative,
            "unencrypted_packets": unencrypted_cumulative,
            "encrypted_percentage": round(encrypted_pct, 2),
            "unencrypted_percentage": round(unencrypted_pct, 2),
        },

        # Protocol data - simplified
        "protocol_data": protocol_data,
    }

    # Create a focused prompt for periodic summaries
    prompt = f"""
        You are a network analyst providing a brief status update.
        Generate a JSON object with ONLY a "summary" key containing a SHORT 3-4 sentence update.

        Focus on:
        - Current traffic volume, top protocols, and average throughput
        - IP version distribution (IPv4 vs IPv6) and encryption status
        - Any notable performance issues for TCP (latency, retransmissions) and RTP (jitter, packet loss) or any other protocol
        - Overall network health status

        Keep it concise and actionable. Highlight only the most important insights.

        **Current Network Data:**
        {json.dumps(periodic_data, indent=2)}

        Return ONLY valid JSON: {{"summary": "your brief summary here"}}
        """

    try:
        model = genai.GenerativeModel('models/gemini-flash-latest')
        response = await model.generate_content_async(prompt)
        raw_text = response.text

        # Extract JSON
        json_start = raw_text.find('{')
        json_end = raw_text.rfind('}') + 1

        if json_start != -1 and json_end != 0:
            clean_json_str = raw_text[json_start:json_end]
            result = json.loads(clean_json_str)
            result['timestamp'] = datetime.now().isoformat()
            result['duration_seconds'] = round(duration, 2)
            return result

        raise ValueError("No valid JSON in AI response")

    except (
        TimeoutError,
        RuntimeError,
        ValueError,
        TypeError,
        json.JSONDecodeError,
    ) as e:
        print(f"Periodic summary generation failed: {e}")
        # Fallback summary with key metrics
        fallback = (
            f"Network: {total_packets} packets, {_format_throughput(overall_in_avg)} in / "
            f"{_format_throughput(overall_out_avg)} out. "
            f"Top protocol: {top_3_protocols[0][0] if top_3_protocols else 'None'}."
            f"TCP latency: {round(tcp_lat_avg, 2)} ms avg, retransmissions: {round(tcp_loss_pct, 2)}%."
            f"RTP jitter: {round(rtp_jit_avg, 2)} ms avg, loss: {round(rtp_loss_pct, 2)}%. "
            f"IPv4: {round(ipv4_pct, 2)}%, Encrypted: {round(encrypted_pct, 2)}%."
        )
        return {
            "summary": fallback,
            "timestamp": datetime.now().isoformat(),
            "duration_seconds": round(duration, 2)
        }
