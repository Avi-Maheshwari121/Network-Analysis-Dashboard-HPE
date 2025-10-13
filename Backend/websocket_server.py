"""
WebSocket server for client communication with robust delta updates.
Auto-stops capture when all clients disconnect (like on refresh).
"""
import json
import asyncio
import websockets
from datetime import datetime
import capture_manager
import metrics_calculator
import shared_state
# AI summary imports
import os
from dotenv import load_dotenv
import google.generativeai as genai

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
    latencies = [m['latency'] for m in history if m['latency'] > 0]
    jitters = [m['jitter'] for m in history if m['jitter'] > 0]
    in_throughputs = [m['inbound_throughput'] for m in history]
    out_throughputs = [m['outbound_throughput'] for m in history]
    analysis = {
        "duration_seconds": count * 1.5,
        "total_packets_captured": history[-1].get("totalPackets", 0),
        "final_packet_loss_percent": history[-1].get("packet_loss_percent", 0),
        "protocol_distribution": history[-1].get("protocol_distribution", {}),
        "latency_stats_ms": {
            "average": round(sum(latencies) / len(latencies), 2) if latencies else 0,
            "peak": round(max(latencies), 2) if latencies else 0,
            "jitter_average": round(sum(jitters) / len(jitters), 2) if jitters else 0,
        },
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
        loss = session_analysis.get('final_packet_loss_percent', 0)
        avg_latency = session_analysis.get('latency_stats_ms', {}).get('average', 0)
        mock_summary = (
            f"--- MOCK SUMMARY ---\n\n"
            f"The capture session lasted for approximately {int(duration)} seconds, capturing a total of {packets} packets.\n\n"
            f"The connection showed an average latency of {avg_latency:.2f} ms. "
            f"The final packet loss was recorded at {loss:.2f}%.\n\n"
            f"(This is a placeholder summary. The AI model could not be reached.)"
        )
        return mock_summary

async def data_collection_loop():
    """Continuously collect data and send updates to clients - ASYNC VERSION"""
    while True:
        await asyncio.sleep(0.1)
        
        if not capture_manager.is_capture_active():
            continue
        
        # Skip if no clients
        if not shared_state.connected_clients:
            await asyncio.sleep(0.5)
            continue

        # ASYNC CAPTURE - This won't block the event loop
        await capture_manager.capture_packets(1.5)

        # Check again after capture if clients or not
        if not shared_state.connected_clients:
            continue
        
        metrics_calculator.calculate_metrics()
        current_metrics = metrics_calculator.get_metrics_state()
        shared_state.session_metrics_history.append(current_metrics)
        
        disconnected_clients = set()
        for client in list(shared_state.connected_clients.keys()):
            data_to_send = {
                "type": "update",
                "metrics": current_metrics,
                "new_packets": shared_state.all_packets_history
            }
            try:
                await client.send(json.dumps(data_to_send))
            except websockets.exceptions.ConnectionClosed:
                disconnected_clients.add(client)

        if disconnected_clients:
            for client in disconnected_clients:
                if client in shared_state.connected_clients:
                    del shared_state.connected_clients[client]
            print(f"Cleaned up {len(disconnected_clients)} disconnected clients.")

async def handle_command(command, data):
    """Handle incoming WebSocket commands."""
    if command == "get_interfaces":
        interfaces = capture_manager.get_network_interfaces()
        return {"type": "interfaces_response", "interfaces": interfaces}
    
    elif command == "start_capture":
        if shared_state.tshark_proc is not None:
            success, msg = False, "Tshark already running"
        else:
            capture_manager.clear_all_packets()
            interface = data.get("interface", "1")
            success, msg = await capture_manager.start_tshark(interface)
            if success:
                metrics_calculator.update_metrics_status("running")
        return {"type": "command_response", "command": "start_capture", "success": success, "message": msg}
    
    elif command == "stop_capture":
        should_summarize = shared_state.capture_active and bool(shared_state.session_metrics_history)
        
        summary = None
        if should_summarize:
            print("Generating AI summary...")
            summary = await generate_summary()
            print("Summary generated.")

        success, msg = await capture_manager.stop_tshark()
        if success:
            metrics_calculator.update_metrics_status("stopped")
        
        response = {
            "type": "command_response", 
            "command": "stop_capture", 
            "success": success, 
            "message": msg
        }
        if summary:
            response["summary"] = summary
            
        return response

    elif command == "get_status":
        return {"type": "status_response", "metrics": metrics_calculator.get_metrics_state()}
    
    else:
        return {"type": "error", "message": f"Unknown command: {command}"}

async def websocket_handler(websocket):
    """Handle a single WebSocket client connection."""
    client_id = id(websocket)
    try:
        # WAIT if system is resetting 
        while shared_state.is_resetting:
            print(f"Client {client_id} waiting - system is resetting...")
            await asyncio.sleep(0.1)

        shared_state.connected_clients[websocket] = {"connected_at": datetime.now().isoformat()}
        print(f"Client {client_id} connected. Total clients: {len(shared_state.connected_clients)}")
        
        interfaces = capture_manager.get_network_interfaces()
        initial_data = {
            "type": "initial_state",
            "metrics": metrics_calculator.get_metrics_state(),
            "packets": shared_state.all_packets_history,
            "interfaces": interfaces
        }
        await websocket.send(json.dumps(initial_data))

        async for message in websocket:
            data = json.loads(message)
            command = data.get("command")
            
            if command:
                response = await handle_command(command, data)
                if response:
                    await websocket.send(json.dumps(response))

    except (websockets.exceptions.ConnectionClosed, websockets.exceptions.ConnectionClosedError):
        print(f"Client {client_id} connection closed.")
        
    finally:
        if websocket in shared_state.connected_clients:
            del shared_state.connected_clients[websocket]
        
        remaining = len(shared_state.connected_clients)
        print(f"Client {client_id} session ended. Total clients: {remaining}")
        
        if remaining == 0 and capture_manager.is_capture_active():
            print("Last client disconnected, stopping capture...")
            
            # SET RESETTING FLAG 
            shared_state.is_resetting = True
            
            await capture_manager.stop_tshark()
            metrics_calculator.update_metrics_status("stopped")
            
            # Wait for complete reset 
            await asyncio.sleep(0.3)
            
            # CLEAR RESETTING FLAG 
            shared_state.is_resetting = False
            
            print("RESET COMPLETE - Ready for new connections")

async def start_websocket_server():
    """Start the WebSocket server and the data collection loop."""
    print("Starting WebSocket server on ws://localhost:8765")
    
    asyncio.create_task(data_collection_loop())
    server = await websockets.serve(websocket_handler, "localhost", 8765)
    await server.wait_closed()