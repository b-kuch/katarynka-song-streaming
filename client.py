import asyncio

import websockets
from fastapi import FastAPI, WebSocketDisconnect

app = FastAPI()


async def websocket_connect():
    async with websockets.connect('ws://localhost:8000/ws') as ws:
        # listen for connections
        try:
            while True:
                contents = await ws.recv()
                print(contents)
        except WebSocketDisconnect:
            print("Client disconnected")

asyncio.run(websocket_connect())
