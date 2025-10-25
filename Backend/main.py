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

async def cleanup_and_exit():
    """Async cleanup before exit"""
    try:
        await capture_manager.stop_tshark()
    except Exception as e:
        print(f"Error during cleanup: {e}")
    finally:
        import os
        os._exit(0)


def signal_handler(sig, frame):
    """Handle shutdown signals gracefully"""
    print("\nReceived shutdown signal. Cleaning up...")
    
    # Set flag to stop capture
    shared_state.capture_active = False
    
    # If there's a running event loop, schedule the async cleanup
    try:
        loop = asyncio.get_running_loop()
        # Schedule the coroutine in the running loop
        loop.create_task(cleanup_and_exit())
    except RuntimeError:
        # No running loop, just exit
        import os
        os._exit(0)


def main():
    """Main application entry point"""
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("Network Monitoring Dashboard - Backend")
    
    try:
        capture_manager.get_device_ips()
        asyncio.run(start_websocket_server())
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
    except Exception as e:
        print(f"Application error: {e}")
    finally:
        print("Application shutdown complete")


if __name__ == "__main__":
    main()
