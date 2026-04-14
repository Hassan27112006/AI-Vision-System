import os
import requests
import bz2
import shutil
import wget

def download_file(url, destination):
    if os.path.exists(destination):
        print(f"{destination} already exists, skipping download.")
        return
    print(f"Downloading {url} to {destination}...")
    wget.download(url, destination)
    print("\nDownload complete.")

def main():
    models_dir = os.path.join(os.path.dirname(__file__), '..', 'backend', 'models')
    os.makedirs(models_dir, exist_ok=True)

    # dlib 68 points landmark predictor
    landmark_url = "http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2"
    landmark_bz2 = os.path.join(models_dir, "shape_predictor_68_face_landmarks.dat.bz2")
    landmark_dat = os.path.join(models_dir, "shape_predictor_68_face_landmarks.dat")

    if not os.path.exists(landmark_dat):
        download_file(landmark_url, landmark_bz2)
        print("Decompressing dlib model...")
        with bz2.BZ2File(landmark_bz2) as fr, open(landmark_dat, 'wb') as fw:
            shutil.copyfileobj(fr, fw)
        os.remove(landmark_bz2)
        print("dlib model extracted.")
    else:
        print("dlib model exists.")

    # YOLOv8 Weights (will be downloaded automatically by ultralytics, but we can pre-fetch)
    # yolo_herd could be a custom trained one, but for now we use yolov8n.pt or similar
    # In a real project, user would train it, here we provide placeholders or use yolov8n
    
    # We will use yolov8n.pt as a base for Object Counting and Herd Detection (Animal class)
    print("Pre-loading YOLOv8 models...")
    from ultralytics import YOLO
    
    # Object counting model
    objects_path = os.path.join(models_dir, 'yolov8_objects.pt')
    if not os.path.exists(objects_path):
        print("Downloading YOLOv8 weights...")
        model = YOLO('yolov8n.pt')
        # Check if it was downloaded locally
        local_weights = 'yolov8n.pt'
        if os.path.exists(local_weights):
            shutil.move(local_weights, objects_path)
            print(f"Moved YOLO weights to {objects_path}")
        else:
            print("Warning: yolov8n.pt not found locally after download attempt.")

    # Herd detection model (using same base)
    herd_path = os.path.join(models_dir, 'yolov8_herd.pt')
    if not os.path.exists(herd_path) and os.path.exists(objects_path):
        shutil.copy(objects_path, herd_path)
        print(f"Copied {objects_path} to {herd_path}")

    # HAAR Cascade (Standard OpenCV)
    # Usually available in cv2.data.haarcascades, but we copy for modularity
    import cv2
    haar_animal_path = os.path.join(models_dir, 'haarcascade_animal.xml')
    # OpenCV doesn't have a generic "animal" cascade, usually it's frontal face or eye.
    # We'll use catface as a proxy or download a generic one if available.
    catface_cascade_path = os.path.join(cv2.data.haarcascades, 'haarcascade_frontalcatface.xml')
    if os.path.exists(catface_cascade_path):
        shutil.copy(catface_cascade_path, haar_animal_path)

    print("All models ready.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error downloading models: {e}")
        print("Note: You might need to install 'wget' and 'ultralytics' first.")
