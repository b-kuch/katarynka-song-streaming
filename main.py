import time
from fastapi import FastAPI
from fastapi import WebSocket
from starlette.responses import StreamingResponse
from starlette.websockets import WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from music import get_song

app = FastAPI()

# TODO: find out how cors should be handled
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


@app.get('/audio')
async def get_audio():

    def iter_file():
        with get_song('Here Comes A Big Black Cloud!! - Graverobbin.mp3', CHUNK_SIZE=1024) as song:
            time.sleep(1)
            print('Chunk')
            yield from song

    return StreamingResponse(iter_file(), media_type="audio/mp3")
