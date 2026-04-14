import os
import cv2
import time

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(img_path, size=(640, 640)):
    """Preprocess image for AI inference."""
    img = cv2.imread(img_path)
    if img is None:
        return None
    img_resized = cv2.resize(img, size)
    return img_resized

def get_timestamp():
    """Readable timestamp for logs."""
    return time.strftime("%Y-%m-%d %H:%M:%S")

def format_bbox(bbox):
    """Normalize bbox format: [x, y, w, h] to [x1, y1, x2, y2] if needed."""
    (x, y, w, h) = bbox
    return [x, y, x + w, y + h]
