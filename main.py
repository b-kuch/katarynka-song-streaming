import asyncio
from functools import partial

from fastapi import FastAPI
from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect

from music import get_song

app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        with get_song('Here Comes A Big Black Cloud!! - Graverobbin.mp3', CHUNK_SIZE=1024*1024) as song_file:
            while song_file:
                # await asyncio.sleep(0.3)
                payload = next(song_file)
                await websocket.send_bytes(payload)
    except WebSocketDisconnect as e:
        print(e)
    except StopIteration:
        print('song sent')
        await websocket.send_text('song sent!')


def stream_song(song_public_id: str, buffer_size: int = 1024):
    return {"message": f"Hello {song_public_id}"}
