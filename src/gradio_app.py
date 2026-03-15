import gradio as gr
from ultralytics import YOLO
import cv2
import numpy as np
import tempfile
import os

# Загружаем модель
model = YOLO("../models/best.pt")

def process_video(video_file):
    # Создаём временный mp4-файл безопасным способом
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    output_path = tmp.name
    tmp.close()

    cap = cv2.VideoCapture(video_file)
    if not cap.isOpened():
        return "Ошибка: не удалось открыть видео", None

    fps = cap.get(cv2.CAP_PROP_FPS)
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = cv2.VideoWriter(
        output_path,
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height)
    )

    seatbelt_found = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)

        if len(results[0].boxes) > 0:
            seatbelt_found = True

        annotated = results[0].plot()
        out.write(annotated)

    cap.release()
    out.release()

    status = "ПРИСТЁГНУТ" if seatbelt_found else "НЕ ПРИСТЁГНУТ"

    return status, output_path



# Gradio интерфейс
interface = gr.Interface(
    fn=process_video,
    inputs=gr.Video(label="Загрузите видео"),
    outputs=[
        gr.Textbox(label="Статус"),
        gr.File(label="Скачать обработанное видео")
    ],
    title="Seatbelt Detection — Video",
    description="Загрузите видео, и модель определит наличие ремня безопасности."
)

interface.launch()
