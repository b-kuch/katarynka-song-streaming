import time
from fastapi import FastAPI
from starlette.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from src.streaming.music import get_song

app = FastAPI()

# TODO: find out how cors should be handled
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
async def hello():
    return {'hello': 'song_streaming'}


@app.get('/audio/{song_id}')
async def get_audio(song_id: str):

    def iter_file():
        with get_song(song_id) as song:
            yield from song

    return StreamingResponse(iter_file(), media_type="audio/mp3")
