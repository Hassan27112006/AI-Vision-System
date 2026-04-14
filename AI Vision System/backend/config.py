import os

class Config:
    # Project Paths
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    MODELS_DIR = os.path.join(BASE_DIR, 'backend', 'models')
    STATIC_DIR = os.path.join(BASE_DIR, 'frontend', 'static')
    UPLOAD_FOLDER = os.path.join(STATIC_DIR, 'uploads')
    
    # Model Paths
    YOLO_HERD = os.path.join(MODELS_DIR, 'yolov8_herd.pt')
    YOLO_OBJECTS = os.path.join(MODELS_DIR, 'yolov8_objects.pt')
    HAAR_ANIMAL = os.path.join(MODELS_DIR, 'haarcascade_animal.xml')
    DLIB_SHAPE_68 = os.path.join(MODELS_DIR, 'shape_predictor_68_face_landmarks.dat')
    
    # Bounding Box Thresholds (Confidence)
    THRESHOLD_HERD = 0.4
    THRESHOLD_OBJECTS = 0.5
    
    # DB
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'data', 'history.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Detection Classes (COCO examples or custom)
    HERD_CLASSES = [14, 15, 16, 17, 18, 19, 20, 21, 22, 23] # Animal classes (bird, cat, dog, horse, sheep, cow, elephant, bear, zebra, giraffe)
    
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
os.makedirs(os.path.join(Config.BASE_DIR, 'data'), exist_ok=True)
