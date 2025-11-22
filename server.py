from fastapi import FastAPI
import yt_dlp

app = FastAPI()

@app.get("/audio")
def get_audio(url: str):
    ydl_opts = {"format": "bestaudio", "noplaylist": True, "quiet": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return {"audio_url": info["url"]}
