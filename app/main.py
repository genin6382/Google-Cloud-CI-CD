import time
from google.cloud import storage
from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from config import GOOGLE_CLOUD_PROJECT, BUCKET_NAME

storage_client = storage.Client(project=GOOGLE_CLOUD_PROJECT)
bucket = storage_client.bucket(BUCKET_NAME)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_files(audio: UploadFile, video: UploadFile, image: UploadFile):
    try:
        print("Starting upload process...")
        start_time = time.time()
        files = [
            ("audio/", audio),
            ("video/", image),
            ("drawings/", image)
        ]
        uploaded = []

        for folder, file in files:
            blob_name = f"{folder}{file.filename}"
            blob = bucket.blob(blob_name)

            # Upload file
            blob.upload_from_file(file.file, content_type=file.content_type)
            uploaded.append(blob_name)

        elapsed_time = round(time.time() - start_time, 3)

        return JSONResponse({
            "status": "success",
            "uploaded_files": uploaded,
            "upload_time_seconds": elapsed_time
        })

    except Exception as e:
        return JSONResponse({
            "status": "error",
            "message": str(e)
        })
