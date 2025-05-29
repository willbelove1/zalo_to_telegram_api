from fastapi import FastAPI, File, UploadFile, Form, Header, HTTPException
import requests
from fastapi.responses import JSONResponse
import os

app = FastAPI()

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
UPLOAD_KEY = os.environ.get("UPLOAD_KEY")

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), x_token: str = Header(...)):
    if x_token != UPLOAD_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument"
        files = {
            "document": (file.filename, await file.read(), file.content_type)
        }
        data = {"chat_id": CHAT_ID}

        response = requests.post(url, data=data, files=files)
        return JSONResponse(content=response.json())
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
