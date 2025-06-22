import os
from uuid import uuid4
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.auth import get_current_user

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter()

@router.post("")
def upload_image(file: UploadFile = File(...), user=Depends(get_current_user)):
    ext = file.filename.split(".")[-1]
    filename = f"{uuid4().hex}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as f:
        content = file.file.read()
        f.write(content)

    return {
        "filename": filename,
        "url": f"/uploads/{filename}",
        "size": len(content)
    }