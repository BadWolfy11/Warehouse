from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import shutil
import os

router = APIRouter(tags=["Images"]) #Создание тега для работы с изображениями
#Папка для сохранения изображений, если ее не существует, то она будет создана
UPLOAD_DIR = "static/images/products"


@router.post("/upload-image/")
#Создание асинхронной функции, которая на вход ожидает файл
# File(...) обозначает, что параметр принимается из тела запроса,
# (...) - обозначает обязательный параметр
async def upload_image(file: UploadFile = File(...)):
    # Создает папку, если ее не существует
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    # Открывает запись в бинарном режиме и называет файл buffer
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer) # Копирует полученный файл в только что созданный

    return {"url": f"/static/images/products/{file.filename}"}

@router.delete("/delete-image/{filename}")
async def delete_image(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return {"message": "Файл удалён"}
    return {"message": "Файл не найден", "status": "skipped"}