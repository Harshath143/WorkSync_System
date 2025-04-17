# app/routers/image_upload.py
from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import CapturedImage
import shutil
import os
from datetime import datetime

router = APIRouter()

UPLOAD_DIR = "uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload-image/")
def upload_image(
    file: UploadFile = File(...),
    staff_id: int = Form(...),
    session_id: int = Form(...),
    db: Session = Depends(get_db)
):
    filename = f"{staff_id}_{session_id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{file.filename}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    image = CapturedImage(
        image_path=filepath,
        staff_id=staff_id,
        session_id=session_id
    )
    db.add(image)
    db.commit()

    return {"message": "Image uploaded successfully", "path": filepath}

@router.get("/images/")
def get_all_images(db: Session = Depends(get_db)):
    images = db.query(CapturedImage).all()
    return [
        {
            "id": img.id,
            "image_url": f"/uploaded_images/{os.path.basename(img.image_path)}",
            "timestamp": img.timestamp,
            "staff_id": img.staff_id,
            "session_id": img.session_id
        } for img in images
    ]
# Import `get_db` inside the function where it’s needed
def some_function():
    from app.database import get_db  # local import
    # Use get_db here
    db = get_db()
    # Do something with db
    # Close the db session when done
    db.close()  
