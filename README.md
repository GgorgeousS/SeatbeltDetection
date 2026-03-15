# SeatbeltDetection — система детекции ремней безопасности на видео

Проект представляет собой систему компьютерного зрения, которая автоматически определяет наличие ремня безопасности у водителя на видео.  
Модель обучена на основе YOLOv8, а для удобного взаимодействия используется веб‑интерфейс Gradio.

---

## 🚀 Возможности

- Детекция ремня безопасности на видео
- Автоматическая обработка каждого кадра
- Определение статуса: **пристёгнут / не пристёгнут**
- Генерация обработанного видео с боксами
- Возможность скачать результат
- Удобный интерфейс через Gradio

---

## 🧠 Технологии

- Python 3.10+
- YOLOv8 (Ultralytics)
- PyTorch
- OpenCV
- NumPy
- Gradio

---

## 📂 Структура проекта

```
SeatbeltDetection/
	DataSet/                 # датасет (train/valid/test) + data.yaml
	models/                  # веса модели (best.pt, last.pt, yolov8n.pt)
	src/                     # код проекта
		train_seatbelt.py      # обучение YOLOv8 на DataSet
		test_image.py          # детекция на изображении (пример)
		video_detect.py        # детекция на видео (пример)
		gradio_app.py          # веб-интерфейс Gradio (видео → статус + файл)
		api.py                 # FastAPI endpoint (/detect) для изображений
	runs/                    # артефакты Ultralytics (если запускали train/predict)
	requirements.txt
	README.md
```

Важно про запуск:
- Скрипты `gradio_app.py`, `video_detect.py`, `test_image.py`, `api.py` используют путь к весам `../models/best.pt`, поэтому их удобнее запускать из папки `src/`.
- Скрипт обучения `train_seatbelt.py` использует путь к датасету `DataSet/data.yaml`, поэтому его удобнее запускать из корня проекта.

---

## 🏁 Как запустить проект

Ниже приведена пошаговая инструкция, которая позволит запустить систему на любом компьютере.

---

### 🔹 1. Клонировать репозиторий

```bash
git clone https://github.com/<your-username>/SeatbeltDetection.git
cd SeatbeltDetection


### 🔹 2. Создать и активировать виртуальное окружение

PowerShell (Windows):

```powershell
python -m venv .venv
./.venv/Scripts/Activate.ps1
```

CMD (Windows):

```bat
python -m venv .venv
.venv\Scripts\activate
```


### 🔹 3. Установить зависимости

```bash
python -m pip install -U pip
pip install -r requirements.txt
```

Примечание про `torch`: на некоторых машинах/версиях Python может потребоваться установка CPU-сборки с официального индекса PyTorch. Если `pip install -r requirements.txt` падает на `torch`, поставьте PyTorch по инструкции с https://pytorch.org/ и повторите установку остальных пакетов.


## ✅ Быстрый старт (Gradio)

Запуск веб-интерфейса для видео (определяет «пристёгнут/не пристёгнут», а также даёт скачать обработанное видео):

```bash
cd src
python gradio_app.py
```

После запуска откройте ссылку, которую выведет Gradio (обычно `http://127.0.0.1:7860`).


## 🖼️ Детекция на изображении (пример)

1) Положите тестовую картинку рядом со `src/test_image.py` или укажите полный путь.
2) В файле `src/test_image.py` замените `img_path = "3195.jpeg"` на ваш файл.
3) Запустите:

```bash
cd src
python test_image.py
```

Результат сохранится как `output.jpg` (в текущей папке запуска), а также откроется окно с визуализацией.


## 🎥 Детекция на видео (пример)

1) Положите видео рядом со `src/video_detect.py` или укажите полный путь.
2) В файле `src/video_detect.py` замените `video_path = "testvideo.mp4"`.
3) Запустите:

```bash
cd src
python video_detect.py
```

Выходное видео пишется в `output_video1.mp4` (в папке запуска). Выход из окна — клавиша `Esc`.


## 🏋️ Обучение модели

Обучение запускается из корня проекта (потому что путь к датасету задан как `DataSet/data.yaml`):

```bash
python src/train_seatbelt.py
```

По умолчанию в [src/train_seatbelt.py](src/train_seatbelt.py) выставлено `device="cpu"` (подходит для AMD/без CUDA). Если у вас есть NVIDIA + CUDA, можно поменять на `device="cuda"`.

После обучения веса обычно лежат в папке проекта Ultralytics (зависит от версии/настроек), например:
- `runs_seatbelt/yolov8n_seatbelt/weights/best.pt`

Чтобы использовать новые веса в приложениях, скопируйте/замените файл `models/best.pt`.


## 🌐 API (FastAPI) — опционально

В проекте есть простой эндпоинт для детекции на изображении: `POST /detect`.

Запуск (важно запускать из `src/`, чтобы относительный путь `../models/best.pt` корректно находился):

```bash
cd src
uvicorn api:app --reload
```

Пример запроса (PowerShell):

```powershell
$resp = Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/detect -Form @{ file = Get-Item "C:\\path\\to\\image.jpg" }
$resp | ConvertTo-Json -Depth 5
```

Ответ содержит список детекций с `confidence` и `bbox`.


## 🧪 Датасет

Описание датасета и классов находится в `DataSet/data.yaml`.
Сейчас класс один: `Seat-Belt`.


## 🧩 Частые проблемы

- `cv2.VideoCapture` не открывает видео: попробуйте MP4 (H.264), проверьте путь к файлу (лучше полный путь), либо перекодируйте видео.
- Ошибка загрузки весов: убедитесь, что файл `models/best.pt` существует и вы запускаете приложения из папки `src/`.

