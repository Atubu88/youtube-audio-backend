from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import yt_dlp
import os

app = FastAPI()

# Путь к cookies-файлу (Render создаёт файл в /etc/secrets/)
COOKIES_PATH = "/etc/secrets/COOKIES_FILE"


@app.get("/audio")
async def get_audio(url: str = Query(..., description="YouTube URL")):

    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "nocheckcertificate": True,
        "cookiefile": COOKIES_PATH,   # ← используем куки!
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            # Ищем аудио URL
            if "url" in info:
                return {"audio_url": info["url"]}

            if "formats" in info:
                for f in info["formats"]:
                    if f.get("acodec") != "none" and "url" in f:
                        return {"audio_url": f["url"]}

        return JSONResponse({"error": "No audio found"}, status_code=404)

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


@app.get("/")
def root():
    return {"status": "ok"}
