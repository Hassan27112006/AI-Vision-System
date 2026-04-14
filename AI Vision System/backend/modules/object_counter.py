import os
import cv2
import numpy as np
import time
from ultralytics import YOLO
from backend.config import Config

class ObjectCounter:
    def __init__(self):
        self.model_path = Config.YOLO_OBJECTS
        if not os.path.exists(self.model_path):
            self.model = YOLO('yolov8n.pt')
        else:
            self.model = YOLO(self.model_path)
            
        self.logs = []

    def count_objects(self, input_path):
        """
        Detect and count generic objects in an image or video frame.
        """
        self.logs = []
        self.logs.append(f"Analyzing: {os.path.basename(input_path)}")
        
        results = self.model(input_path, conf=Config.THRESHOLD_OBJECTS)
        detections = []
        
        output_filename = f"counted_{os.path.basename(input_path)}"
        output_path = os.path.join(Config.UPLOAD_FOLDER, output_filename)
        
        processed_results = []
        for r in results:
            img = r.orig_img.copy()
            counts = {}
            for box in r.boxes:
                cls_id = int(box.cls[0])
                label = r.names[cls_id]
                counts[label] = counts.get(label, 0) + 1
                
                det = {
                    "class": label,
                    "confidence": float(box.conf[0]),
                    "bbox": [int(x) for x in box.xyxy[0]]
                }
                detections.append(det)
                
                # Draw on result
                x1, y1, x2, y2 = det['bbox']
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 2)
                cv2.putText(img, f"{label} {det['confidence']:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)

            total_count = sum(counts.values())
            self.logs.append(f"Total Objects Detected: {total_count}")
            for lbl, cnt in counts.items():
                self.logs.append(f"- {lbl}: {cnt}")
                
            cv2.imwrite(output_path, img)

            processed_results.append({
                "total_count": total_count,
                "breakdown": counts,
                "output_url": f"/static/uploads/{output_filename}",
                "detections": detections,
                "logs": self.logs
            })
            break # Just one result for images

        return processed_results[0]
