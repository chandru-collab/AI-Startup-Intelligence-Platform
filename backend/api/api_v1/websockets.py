from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
import logging

logger = logging.getLogger(__name__)

websocket_router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info("New WebSocket connection accepted.")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info("WebSocket connection closed.")

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Error sending message to websocket: {e}")

manager = ConnectionManager()

# Helper for synchronous background threads to emit websocket messages
import asyncio
import threading

# We need to capture the main event loop when the app starts
main_loop = None

def get_main_loop():
    global main_loop
    if main_loop is None:
        try:
            main_loop = asyncio.get_running_loop()
        except RuntimeError:
            pass
    return main_loop

def sync_broadcast(message: str):
    """Safely queues a broadcast message from a synchronous thread to the async event loop."""
    loop = get_main_loop()
    if loop and loop.is_running():
        asyncio.run_coroutine_threadsafe(manager.broadcast(message), loop)
    else:
        logger.warning(f"Could not broadcast message (no active event loop): {message}")

@websocket_router.websocket("/ws/alerts")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive, listen for any messages from client if needed
            data = await websocket.receive_text()
            logger.debug(f"Received WS message: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
