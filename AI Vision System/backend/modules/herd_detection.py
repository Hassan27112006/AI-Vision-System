import os
import cv2
import numpy as np
import time
from ultralytics import YOLO
from backend.config import Config

class HerdDetector:
    def __init__(self):
        self.model_path = Config.YOLO_HERD
        if not os.path.exists(self.model_path):
            # Fallback to default pretrained if custom not found
            self.model = YOLO('yolov8n.pt')
        else:
            self.model = YOLO(self.model_path)
        
        self.animal_classes = Config.HERD_CLASSES
        self.logs = []

    def detect(self, input_path, save_output=True):
        """
        Detect herds in an image or video frame.
        """
        self.logs = []
        self.logs.append(f"Starting detection on: {os.path.basename(input_path)}")
        
        results = self.model(input_path, stream=True)
        detections = []
        frame_idx = 0
        
        # Create output video/image location
        output_filename = f"detected_{os.path.basename(input_path)}"
        output_path = os.path.join(Config.UPLOAD_FOLDER, output_filename)

        processed_results = []
        for r in results:
            img = r.orig_img.copy()
            boxes = r.boxes
            animal_count = 0
            
            frame_detections = []
            for box in boxes:
                cls = int(box.cls[0])
                if cls in self.animal_classes:
                    animal_count += 1
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    conf = float(box.conf[0])
                    label = f"{r.names[cls]} {conf:.2f}"
                    
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    
                    frame_detections.append({
                        "class": r.names[cls],
                        "confidence": conf,
                        "bbox": [x1, y1, x2, y2]
                    })
            
            # Special logic for "herds" - if count > 5, it's a herd
            is_herd = animal_count > 5
            self.logs.append(f"Detected {animal_count} animals. Herd Status: {'YES' if is_herd else 'NO'}")
            
            if save_output:
                cv2.imwrite(output_path, img)

            processed_results.append({
                "count": animal_count,
                "is_herd": is_herd,
                "output_url": f"/static/uploads/{output_filename}",
                "detections": frame_detections,
                "timestamp": time.time(),
                "logs": self.logs
            })
            
            # For images, we only have one frame
            if not input_path.endswith('.mp4'):
                break

        return processed_results[0]
