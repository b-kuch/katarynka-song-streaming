from fastapi import FastAPI
from starlette.responses import StreamingResponse
from src.streaming.music import get_song, file_size

app = FastAPI()


@app.get('/')
async def hello():
    return {'hello': 'song_streaming'}


@app.get('/audio/{song_id}')
async def get_audio(song_id: str):
    def iter_file():
        with get_song(song_id) as song:
            yield from song

    size = file_size(song_id)
    return StreamingResponse(iter_file(), media_type="audio/mp3", headers={'Content-Length': str(size)})
