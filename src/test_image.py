from ultralytics import YOLO
import cv2

def main():
    # Загружаем обученную модель
    model = YOLO("../models/best.pt")


    # Путь к тестовой картинке
    img_path = "3195.jpeg"  # замени на свою картинку

    # Запускаем предсказание
    results = model(img_path)

    # Сохраняем изображение с боксами
    results[0].save(filename="output.jpg")

    # Показываем результат
    annotated = results[0].plot()
    cv2.imshow("Seatbelt Detection", annotated)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
