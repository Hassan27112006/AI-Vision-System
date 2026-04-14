import os
import cv2
import dlib
import numpy as np
import time
from backend.config import Config

class FaceProfiler:
    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()
        # Path to shape predictor 68
        self.predictor_path = Config.DLIB_SHAPE_68
        if os.path.exists(self.predictor_path):
            self.predictor = dlib.shape_predictor(self.predictor_path)
        else:
            self.predictor = None
            print("ERROR: dlib shape predictor not found. Run download_models.py first.")

    def analyze(self, img_path):
        if self.predictor is None:
            return {"error": "Shape predictor not loaded."}
            
        img = cv2.imread(img_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.detector(gray)
        
        results = []
        for face in faces:
            landmarks = self.predictor(gray, face)
            pts = np.array([[landmarks.part(i).x, landmarks.part(i).y] for i in range(68)])
            
            # Eye Dist (P36:P45) - approx
            eye_dist = np.linalg.norm(pts[36] - pts[45])
            # Jaw Width (P0:P16)
            jaw_width = np.linalg.norm(pts[0] - pts[16])
            # Nose Height (P27:P33)
            nose_height = np.linalg.norm(pts[27] - pts[33])
            # Face Height (P19:P8)
            face_height = np.linalg.norm((pts[19] + pts[24])/2 - pts[8])
            
            face_ratio = jaw_width / face_height
            
            # Personality Rule Engine (Simplified)
            # Rule 1: High eye distance -> Highly analytical
            # Rule 2: High face height -> Determined
            # Rule 3: Balanced ratio -> High empathy
            
            personality = "Analytical" if eye_dist > 100 else "Intuitive"
            personality += " & " + ("Determined" if face_height > 200 else "Adaptable")
            
            res = {
                "bbox": [face.left(), face.top(), face.right(), face.bottom()],
                "measurements": {
                    "eye_distance": round(eye_dist, 2),
                    "jaw_width": round(jaw_width, 2),
                    "nose_height": round(nose_height, 2),
                    "face_ratio": round(face_ratio, 2)
                },
                "personality_type": personality,
                "landmarks": pts.tolist()
            }
            results.append(res)
            
            # Draw landmarks on result image
            for (x, y) in pts:
                cv2.circle(img, (x, y), 2, (0, 255, 0), -1)
            cv2.rectangle(img, (face.left(), face.top()), (face.right(), face.bottom()), (255, 0, 0), 2)

        output_filename = f"profiled_{os.path.basename(img_path)}"
        output_path = os.path.join(Config.UPLOAD_FOLDER, output_filename)
        cv2.imwrite(output_path, img)

        return {
            "num_faces": len(results),
            "faces": results,
            "output_url": f"/static/uploads/{output_filename}"
        }
