from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import yt_dlp
import tempfile
import os

app = FastAPI()

def write_cookies_from_env():
    cookies_env = os.getenv("YT_COOKIES")
    if not cookies_env:
        return None

    # Создаем путь в /tmp
    cookies_path = "/tmp/yt_cookies.txt"

    # Записываем с заменой \n -> настоящий перенос строки
    with open(cookies_path, "w") as f:
        f.write(cookies_env.replace("\\n", "\n"))

    return cookies_path


@app.get("/audio")
async def extract_audio(url: str = Query(...)):
    try:
        # создаём cookies-файл
        cookies_file_path = write_cookies_from_env()
        if not cookies_file_path:
            return JSONResponse({"error": "YT_COOKIES not found"}, status_code=500)

        # yt-dlp параметры
        ydl_opts = {
            "format": "bestaudio/best",
            "cookiefile": cookies_file_path,
            "nocheckcertificate": True,
            "extract_flat": False,
            "quiet": False,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            if "url" in info:
                return {"audio_url": info["url"]}
            else:
                return JSONResponse({"error": "Audio URL not found"}, status_code=500)

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
