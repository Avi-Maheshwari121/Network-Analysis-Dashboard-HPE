"""
WebSocket server for client communication with robust delta updates.
"""
import json
import asyncio
import websockets
from datetime import datetime
import capture_manager
import metrics_calculator
import shared_state


async def data_collection_loop():
    """Continuously collect data and send delta updates to clients."""
    while True:
        await asyncio.sleep(0.1)  # Send updates every second
        
        if not capture_manager.is_capture_active() or not shared_state.connected_clients:
            continue

        capture_manager.capture_packets(1.5)
        metrics_calculator.calculate_metrics()
        stats = capture_manager.get_packet_statistics()
        
        disconnected_clients = set()

        for client in list(shared_state.connected_clients.keys()):
            data_to_send = {
                "type": "update",
                "metrics": metrics_calculator.get_metrics_state(),
                "new_packets": shared_state.all_packets_history,  
                "stream_count": stats["stream_count"],
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
        return {
            "type": "interfaces_response",
            "interfaces": interfaces
        }
    
    elif command == "start_capture":
        # When starting a new capture, clear old data first
        capture_manager.clear_all_packets()
            
        interface = data.get("interface", "Wi-Fi")
        success, msg = capture_manager.start_tshark(interface)
        
        if success:
            metrics_calculator.update_metrics_status("running")
            
        return {
            "type": "command_response", 
            "command": "start_capture", 
            "success": success, 
            "message": msg
        }
    
    # Other commands remain the same...
    elif command == "stop_capture":
        success, msg = capture_manager.stop_tshark()
        
        if success:
            metrics_calculator.update_metrics_status("stopped")
            
        return {
            "type": "command_response", 
            "command": "stop_capture", 
            "success": success, 
            "message": msg
        }
        
    elif command == "get_status":
        return {
            "type": "status_response", 
            "metrics": metrics_calculator.get_metrics_state()
        }
        
    else:
        return {
            "type": "error", 
            "message": f"Unknown command: {command}"
        }



async def websocket_handler(websocket):
    """Handle a single WebSocket client connection."""
    try:
        shared_state.connected_clients[websocket] = {
            "connected_at": datetime.now().isoformat()
        }
        print(f"Client connected. Total clients: {len(shared_state.connected_clients)}")
        
        # Send interfaces on initial connection
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
                await websocket.send(json.dumps(response))

    except (websockets.exceptions.ConnectionClosed, websockets.exceptions.ConnectionClosedError):
        print("Client connection closed.")
        
    finally:
        if websocket in shared_state.connected_clients:
            del shared_state.connected_clients[websocket]
        print(f"Client session ended. Total clients: {len(shared_state.connected_clients)}")



async def start_websocket_server():
    """Start the WebSocket server and the data collection loop."""
    print("Starting WebSocket server on ws://localhost:8765")
    
    asyncio.create_task(data_collection_loop())
    server = await websockets.serve(websocket_handler, "localhost", 8765)
    await server.wait_closed()
