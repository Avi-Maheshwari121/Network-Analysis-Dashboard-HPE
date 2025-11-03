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
import llm_summarizer
import geolocation_handler


async def data_collection_loop():
    """Continuously collect data and send updates to clients - ASYNC VERSION"""
    while True:
        await asyncio.sleep(0.1)
        
        # This flag is now set to False by stop_tshark()
        if not capture_manager.is_capture_active():
            continue
        
        # Skip if no clients
        if not shared_state.connected_clients:
            await asyncio.sleep(0.5)
            continue

        # ASYNC CAPTURE - This won't block the event loop
        await capture_manager.capture_packets(shared_state.capture_duration)

        # Check again after capture if clients or not
        if not shared_state.connected_clients:
            continue

        # Check if capture became inactive *during* the packet capture.
        # If so, STOP here and do not run the final calculation.
        # The stop_capture command will handle the final steps.
        if not shared_state.capture_active:
            continue

        # This function correctly calculates and appends to history
        metrics_calculator.calculate_metrics()
        shared_state.session_metrics_history.append(shared_state.metrics_state)

        disconnected_clients = set()
        for client in list(shared_state.connected_clients.keys()):
            data_to_send = {
                "type": "update",
                "metrics": shared_state.metrics_state,
                "new_packets": shared_state.all_packets_history,
                "packets_Per_Second": shared_state.packets_Per_Second,
                "tcp_metrics": shared_state.tcp_metrics,
                "rtp_metrics": shared_state.rtp_metrics,
                "quic_metrics": shared_state.quic_metrics,
                "udp_metrics": shared_state.udp_metrics,
                "dns_metrics": shared_state.dns_metrics,
                "igmp_metrics": shared_state.igmp_metrics,
                "ipv4_metrics": shared_state.ipv4_metrics,
                "ipv6_metrics": shared_state.ipv6_metrics,
                "ip_composition": shared_state.ip_composition,
                "encryption_composition": shared_state.encryption_composition,
                "top_talkers": shared_state.top_talkers_top7,
                "new_geolocations": shared_state.new_geolocations
            }
            
            try:
                await client.send(json.dumps(data_to_send))
            except websockets.exceptions.ConnectionClosed:
                disconnected_clients.add(client)

        # Clear new geolocations after sending
        shared_state.new_geolocations = []
        
        if disconnected_clients:
            for client in disconnected_clients:
                if client in shared_state.connected_clients:
                    del shared_state.connected_clients[client]
            print(f"Cleaned up {len(disconnected_clients)} disconnected clients.")

async def handle_stop_capture_task(websocket, data):
    """
    Handles the entire stop_capture flow as a background task.
    This frees the main websocket loop to receive new commands.
    """
    
    # 0. Check if capture is active. If not, it's already stopping.
    if not shared_state.capture_active:
        return # Silently exit, another stop command is already in progress

    # 1. Get duration
    final_duration = data.get("duration") 
    if final_duration is not None:
        shared_state.session_duration_final = int(final_duration)
        print(f"Received accurate duration from frontend: {shared_state.session_duration_final}s")

    # 2. Stop Tshark (this sets capture_active = False)
    success, msg = await capture_manager.stop_tshark()
    if success:
        metrics_calculator.update_metrics_status("stopped")

    # 3. Give the data_collection_loop a grace period (0.5s) to run its
    #    FINAL metrics calculation and then stop (since capture_active is False).
    await asyncio.sleep(0.5) 

    # 4. Check if we should summarize
    should_summarize = success and bool(shared_state.session_metrics_history)
    
    summary = None
    if should_summarize:
        print("Generating AI summary...")
        shared_state.is_generating_summary = True # SET FLAG
        try:
            summary = await llm_summarizer.generate_summary()
            print("Summary generated.")
        except Exception as e:
            error_msg = f"Error during summary: {e}"
            print(error_msg)
            # Send an error summary so the frontend knows it failed
            summary = {"summary": error_msg, "breakdown": []} 
        finally:
            shared_state.is_generating_summary = False # UNSET FLAG
    else:
        if not success:
            print("Summary skipped: Tshark did not stop successfully.")
        if not bool(shared_state.session_metrics_history):
            print("Summary skipped: No session history was found.")

    # 5. Build the final response with the summary data
    response = {
        "type": "command_response", 
        "command": "stop_capture", # This is the FINAL response
        "success": success, 
        "message": msg
    }
    if summary:
        response["summary"] = summary
    
    # 6. Send the final response to the client
    try:
        await websocket.send(json.dumps(response))
    except Exception as e:
        print(f"Failed to send summary to client: {e}")
    
    # 7. NOW, reset the state for the next session
    capture_manager.resetSharedState()
    print("State reset for next session.")

async def handle_command(command, data):
    """Handles commands that are fast and can be awaited directly."""
    if command == "get_interfaces":
        interfaces = capture_manager.get_network_interfaces()
        return {"type": "interfaces_response", "interfaces": interfaces}
    
    elif command == "start_capture":
        
        # This checks the loop isn't blocked by stop_capture
        if shared_state.is_generating_summary:
            print("Start capture rejected: Summary generation in progress.")
            return {
                "type": "command_response", 
                "command": "start_capture", 
                "success": False, 
                "message": "Please wait, the previous session's summary is still being generated."
            }

        if shared_state.tshark_proc is not None:
            success, msg = False, "Tshark already running"
        else:
            capture_manager.clear_all_packets()
            interface = data.get("interface", "1")
            success, msg = await capture_manager.start_tshark(interface)
            if success:
                metrics_calculator.update_metrics_status("running")
        return {"type": "command_response", "command": "start_capture", "success": success, "message": msg}

    elif command == "get_status":
        return {"type": "status_response", "metrics": shared_state.metrics_state}
    
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
            "metrics": shared_state.metrics_state,
            "packets": shared_state.all_packets_history,
            "interfaces": interfaces,
            "new_packets": shared_state.all_packets_history,
            "packets_Per_Second": shared_state.packets_Per_Second,
            "tcp_metrics": shared_state.tcp_metrics,
            "rtp_metrics": shared_state.rtp_metrics,
            "quic_metrics": shared_state.quic_metrics,
            "udp_metrics": shared_state.udp_metrics,
            "dns_metrics": shared_state.dns_metrics,
            "igmp_metrics": shared_state.igmp_metrics,
            "ipv4_metrics": shared_state.ipv4_metrics,
            "ipv6_metrics": shared_state.ipv6_metrics,
            "ip_composition": shared_state.ip_composition,
            "encryption_composition": shared_state.encryption_composition,
            "top_talkers": shared_state.top_talkers_top7
        }
        await websocket.send(json.dumps(initial_data))

        async for message in websocket:
            data = json.loads(message)
            command = data.get("command")
            
            if command == "stop_capture":
                # 1. Detach the slow logic as a background task
                asyncio.create_task(handle_stop_capture_task(websocket, data))
                
                # 2. Send an *immediate* "Tshark stopped" response
                #    This is for the 1.5s popup.
                await websocket.send(json.dumps({
                    "type": "command_response", 
                    "command": "stop_capture_ack",
                    "success": True, 
                    "message": "Tshark stopped successfully"
                }))
                
            elif command:
                # All other commands are fast and can be awaited
                response = await handle_command(command, data)
                if response:
                    await websocket.send(json.dumps(response))

    except Exception as e:
        print(e)
        
    finally:
        if websocket in shared_state.connected_clients:
            del shared_state.connected_clients[websocket]
        
        remaining = len(shared_state.connected_clients)
        print(f"Client {client_id} session ended. Total clients: {remaining}")
        
        if remaining == 0 and capture_manager.is_capture_active():
            print("Last client disconnected, stopping capture...")
            
            # SET RESETTING FLAG 
            shared_state.is_resetting = True
            
            # Call the *modified* stop_tshark (which no longer resets)
            await capture_manager.stop_tshark()
            metrics_calculator.update_metrics_status("stopped")
            
            # Wait for complete reset 
            await asyncio.sleep(0.3)
            
            # reset the state
            capture_manager.resetSharedState()
            
            # CLEAR RESETTING FLAG 
            shared_state.is_resetting = False
            
            print("RESET COMPLETE - Ready for new connections")

async def start_websocket_server():
    """Start the WebSocket server and the data collection loop."""
    print("Starting WebSocket server on ws://localhost:8765")
    
    asyncio.create_task(data_collection_loop())
    asyncio.create_task(geolocation_handler.geolocation_loop())
    
    server = await websockets.serve(
        websocket_handler, 
        "localhost", 
        8765,
        ping_interval=None,        
        ping_timeout=None,         
    )
    await server.wait_closed()