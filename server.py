from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import yt_dlp
import os

app = FastAPI()

@app.get("/audio")
async def extract_audio(url: str = Query(...)):
    try:
        # Путь к cookies-файлу, который лежит в Secret Files Render
        cookies_file_path = "/etc/secrets/yt_cookies.txt"

        # Проверяем, что файл существует
        if not os.path.exists(cookies_file_path):
            return JSONResponse({"error": "cookies file not found"}, status_code=500)

        # Настройки yt-dlp
        ydl_opts = {
            "format": "bestaudio/best",
            "cookiefile": cookies_file_path,
            "nocheckcertificate": True,
            "quiet": False,
        }

        # Извлекаем данные
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        # Возвращаем прямой URL на аудиопоток
        if "url" in info:
            return {"audio_url": info["url"]}
        else:
            return JSONResponse({"error": "Could not extract audio URL"}, status_code=500)

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
