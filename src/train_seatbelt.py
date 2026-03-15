from ultralytics import YOLO

def main():
    # Загружаем предобученную модель YOLOv8 (nano — самая лёгкая)
    model = YOLO("yolov8n.pt")

    # Запускаем обучение
    model.train(
        data="DataSet/data.yaml",      # путь к твоему YAML
        epochs=50,             # количество эпох
        imgsz=640,             # размер входного изображения
        batch=8,               # размер батча (если мало RAM — уменьшай)
        device="cpu",          # AMD → тренируем на CPU
        project="runs_seatbelt",
        name="yolov8n_seatbelt"
    )

if __name__ == "__main__":
    main()
