from fastapi import FastAPI, UploadFile, File
from ultralytics import YOLO
import cv2
import numpy as np

app = FastAPI()

# Загружаем обученную модель
model = YOLO("../models/best.pt")

@app.post("/detect")
async def detect_seatbelt(file: UploadFile = File(...)):
    # Читаем изображение
    contents = await file.read()
    np_img = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    # Запускаем детекцию
    results = model(img)

    detections = []
    for box in results[0].boxes:
        cls = int(box.cls[0])
        conf = float(box.conf[0])
        x1, y1, x2, y2 = box.xyxy[0].tolist()

        detections.append({
            "class": "seatbelt",
            "confidence": conf,
            "bbox": [x1, y1, x2, y2]
        })

    return {"detections": detections}
