from ultralytics import YOLO
import cv2

def main():
    # Загружаем обученную модель
    model = YOLO("../models/best.pt")


    # Путь к видеофайлу
    video_path = "testvideo.mp4" 
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Ошибка: не удалось открыть видео.")
        return

    # Получаем параметры видео
    fps = cap.get(cv2.CAP_PROP_FPS)
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Создаём выходной файл
    out = cv2.VideoWriter(
        "output_video1.mp4",
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height)
    )

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Запускаем детекцию на кадре
        results = model(frame)

        # Получаем кадр с нарисованными боксами
        annotated_frame = results[0].plot()

        # Показываем в окне
        cv2.imshow("Seatbelt Detection", annotated_frame)

        # Сохраняем в файл
        out.write(annotated_frame)

        # Выход по клавише ESC
        if cv2.waitKey(1) == 27:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
