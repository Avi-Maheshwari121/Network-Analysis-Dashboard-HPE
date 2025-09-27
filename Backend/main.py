"""
Network Monitoring Dashboard - Backend
Main entry point for the application
"""
import asyncio
import signal
import sys
from websocket_server import start_websocket_server
import capture_manager
import shared_state

def signal_handler(sig, frame):
    """Handle shutdown signals gracefully"""
    print("\nReceived shutdown signal. Cleaning up...")
    capture_manager.stop_tshark()
    
    # Instead of sys.exit(0), set a flag and let asyncio handle shutdown
    shared_state.capture_active = False
    
    # Exit more gracefully
    import os
    os._exit(0)  # Forces immediate exit without raising SystemExit


def main():
    """Main application entry point"""
    # Set up signal handlers for graceful shutdown
    # Without signal_handler, resources will leak because tshark not stopped, still running
    # Resource Cleanup
    # Pressing Ctrl + C in terminal to stop the program
    signal.signal(signal.SIGINT, signal_handler) # Interrupt Signal
    signal.signal(signal.SIGTERM, signal_handler) # Termination Signal
    
    print("Network Monitoring Dashboard - Backend")
    
    try:
        shared_state.ip_address = capture_manager.get_device_ips()
        # Start the WebSocket server
        asyncio.run(start_websocket_server()) # Async event loop
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
    except Exception as e:
        print(f"Application error: {e}")
    finally:
        # Ensure cleanup
        capture_manager.stop_tshark()
        print("Application shutdown complete")

if __name__ == "__main__":
    main()
