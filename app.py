from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import pandas as pd
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
UPLOAD_DIR = os.getenv("UPLOAD_DIRECTORY", "./uploaded_files")
CLEANED_DIR = os.getenv("CLEANED_DIRECTORY", "./cleaned_files")

Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
Path(CLEANED_DIR).mkdir(parents=True, exist_ok=True)


def save_upload_file(upload_file: UploadFile):
    try:
        file_path = f"{UPLOAD_DIR}/{upload_file.filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(upload_file.file.read())
        return file_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File save error: {e}")


def clean_data(file_path):
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file_path)
        else:
            raise HTTPException(status_code=400, detail=f"File format not supported: {file_path}")

        cleaned_df = df.dropna()

        cleaned_path = file_path.replace(UPLOAD_DIR, CLEANED_DIR).replace(' ', '_')
        if cleaned_path.endswith('.csv'):
            cleaned_df.to_csv(cleaned_path, index=False)
        else:
            cleaned_df.to_excel(cleaned_path, index=False)

        return cleaned_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Data cleaning error: {e}")


def calculate_statistics(file_path):
    try:
        df = pd.read_csv(file_path) if file_path.endswith('.csv') else pd.read_excel(file_path)
        stats = df.describe().to_dict()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Statistics calculation error: {e}")


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_path = save_upload_file(file)
    return {"filename": file.filename, "location": file_path}


@app.get("/clean/{filename}")
async def clean_file(filename: str):
    file_path = f"{UPLOAD_DIR}/{filename}"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    cleaned_path = clean_data(file_path)
    return FileResponse(cleaned_path, media_type='application/octet-stream', filename=filename)


@app.get("/stats/{filename}")
async def get_statistics(filename: str):
    cleaned_path = f"{CLEANED_DIR}/{filename}"
    if not os.path.exists(cleaned_path):
        raise HTTPException(status_code=404, detail="File not found for statistics")

    stats = calculate_statistics(cleaned_path)
    return stats