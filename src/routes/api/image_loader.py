from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import shutil
import os

router = APIRouter(tags=["Images"])
UPLOAD_DIR = "static/images/products"


@router.post("/upload-image/")

async def upload_image(file: UploadFile = File(...)):

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"url": f"/static/images/products/{file.filename}"}

@router.delete("/delete-image/{filename}")
async def delete_image(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return {"message": "Файл удалён"}
    return {"message": "Файл не найден", "status": "skipped"}