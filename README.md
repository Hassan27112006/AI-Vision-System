# VisionAI - AI Vision Intelligence Platform 🚀

A professional, modular, and production-ready **AI Dashboard** built with **Flask, YOLOv8, and Dlib**. 

Integrates three powerful computer vision modules for real-time analysis, alerting, and biometric profiling.

## 🛠️ Tech Stack
| Layer | Technologies |
| --- | --- |
| **Backend** | Python 3.x, Flask, Flask-CORS |
| **AI/CV** | YOLOv8 (Ultralytics), Dlib, OpenCV |
| **Frontend** | HTML5, TailwindCSS, JavaScript |
| **Maps** | Leaflet.js + OpenStreetMap (Dark Theme) |
| **Reports** | jsPDF (Frontend PDF generation) |

---

## 🏗️ Modules

### 1. 🐾 Animal Herd Detection
- **Detection**: Uses YOLOv8 (cat, dog, cow, sheep, elephant, zebra, etc.).
- **Logic**: Intelligent counting and herd identification (count > 5).
- **Map View**: Real-time GPS alerts for herd locations.
- **Inputs**: Image / Video / Webcam.

### 2. 👤 Face Profiling
- **Landmarks**: 68-point facial landmark extraction using Dlib's shape predictor.
- **Biometrics**: Accurate measurement of eye distance, jaw width, and face ratio.
- **Profiling**: Rule-based personality profiling engine based on facial features.

### 3. 🔢 Universal Object Counter
- **Versatility**: Multi-class object detection.
- **Insights**: Visual breakdown of detected classes (people, cars, electronics, etc.).
- **Controls**: Adjustable threshold and playback controls.

---

## 🚀 Installation & Setup

### 1. Clone & Setup Environment
```bash
python -m venv env
source env/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### 2. Download Pretrained Models
The platform requires YOLOv8 weights and Dlib's 68-point landmark detector.
```bash
python scripts/download_models.py
```

### 3. Preprocess Datasets (Optional)
This converts Kaggle raw data into standardized CSV annotations for future training.
```bash
python scripts/preprocess_datasets.py
```

### 4. Run the Application
```bash
python -m backend.app
```
Then visit `http://localhost:5000` in your browser.

---

## 📁 Project Structure
```text
ai-vision-platform/
├── backend/            # Flask API & AI Logic
│   ├── modules/        # Module specific implementations
│   ├── models/         # Pretrained weight files (.pt, .dat, .xml)
│   └── config.py       # Global paths & thresholds
├── frontend/           # Modern UI
│   ├── templates/      # HTML (Jinja2)
│   └── static/         # CSS/JS/Assets
├── data/               # Preprocessed annotations & DB
├── scripts/            # Model downloader & Preprocessing
└── tests/              # Pytest suite
```

## ⚖️ License
MIT License. Created for AI research and production demonstration.
