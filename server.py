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

    tmp_path = "/tmp/yt_cookies.txt"
    with open(tmp_path, "w") as f:
        f.write(cookies_env.replace("\\n", "\n"))  # важное преобразование
    return tmp_path



@app.get("/audio")
async def extract_audio(url: str = Query(...)):
    try:
        cookies_data = os.environ.get("YT_COOKIES")
        if not cookies_data:
            return JSONResponse({"error": "YT_COOKIES not found"}, status_code=500)

        # создаём временный файл cookies в /tmp
        with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".txt") as tmp:
            tmp.write(cookies_data.replace("\\n", "\n"))
            cookies_file_path = tmp.name

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": "/tmp/audio.%(ext)s",
            "cookiefile": cookies_file_path,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            if "url" in info:
                return {"audio_url": info["url"]}
            else:
                return JSONResponse({"error": "audio URL not found"}, status_code=500)

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
