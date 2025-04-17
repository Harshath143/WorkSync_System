from fastapi import APIRouter, UploadFile, File
import shutil
import os
from datetime import datetime

router = APIRouter(prefix="/upload", tags=["Uploads"])

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
    save_path = os.path.join("captured_media", filename)

    os.makedirs("captured_media", exist_ok=True)

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": "File uploaded", "filename": filename}
