from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import pandas as pd
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
UPLOAD_DIRECTORY_PATH = os.getenv("UPLOAD_DIRECTORY", "./uploaded_files")
CLEANED_DIRECTORY_PATH = os.getenv("CLEANED_DIRECTORY", "./cleaned_files")

Path(UPLOAD_DIRECTORY_PATH).mkdir(parents=True, exist_ok=True)
Path(CLEANED_DIRECTORY_PATH).mkdir(parents=True, exist_ok=True)


def save_uploaded_file(uploadedFile: UploadFile):
    try:
        file_destination_path = f"{UPLOAD_DIRECTORY_PATH}/{uploadedFile.filename}"
        with open(file_destination_path, "wb") as file_buffer:
            file_buffer.write(uploadedFile.file.read())
        return file_destination_path
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error saving file: {error}")


def clean_uploaded_data(file_path):
    try:
        if file_path.endswith('.csv'):
            data_frame = pd.read_csv(file_path)
        elif file_path.endswith(('.xls', '.xlsx')):
            data_frame = pd.read_excel(file_path)
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported file format: {file_path}")

        cleaned_data_frame = data_frame.dropna()

        cleaned_file_path = file_path.replace(UPLOAD_DIRECTORY_PATH, CLEANED_DIRECTORY_PATH).replace(' ', '_')
        if cleaned_file_path.endswith('.csv'):
            cleaned_data_frame.to_csv(cleaned_file_path, index=False)
        else:
            cleaned_data_frame.to_excel(cleaned_file_path, index=False)

        return cleaned_file_path
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error cleaning data: {error}")


def generate_statistics(cleaned_file_path):
    try:
        data_frame = pd.read_csv(cleaned_file_path) if cleaned_file_path.endswith('.csv') else pd.read_excel(cleaned_file_path)
        statistics = data_frame.describe().to_dict()
        return statistics
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error generating statistics: {error}")


@app.post("/upload/")
async def upload_file_endpoint(file: UploadFile = File(...)):
    file_path = save_uploaded_file(file)
    return {"filename": file.filename, "file_path": file_path}


@app.get("/clean/{filename}")
async def clean_file_endpoint(filename: str):
    source_file_path = f"{UPLOAD_DIRECTORY_PATH}/{filename}"
    if not os.path.exists(source_file_path):
        raise HTTPException(status_code=404, detail="File not found")

    cleaned_file_path = clean_uploaded_data(source_file_path)
    return FileResponse(cleaned_file_path, media_type='application/octet-stream', filename=filename)


@app.get("/stats/{filename}")
async def get_statistics_endpoint(filename: str):
    cleaned_file_path = f"{CLEANED_DIRECTORY_PATH}/{filename}"
    if not os.path.exists(cleaned_file_path):
        raise HTTPException(status_code=404, detail="File not found for statistics")

    statistics = generate_statistics(cleaned_file_path)
    return statistics