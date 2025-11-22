from fastapi import FastAPI
import yt_dlp

app = FastAPI()

@app.get("/audio")
def get_audio(url: str):
    ydl_opts = {
        "format": "bestaudio/best",
        "noplaylist": True,
        "quiet": True,
        # 💚 обход защиты YouTube
        "extractor_args": {
            "youtube": {
                "player_client": ["web"]
            }
        }
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return {"audio_url": info["url"]}
