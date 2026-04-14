import os
import random
from backend.config import Config

class MapAlert:
    @staticmethod
    def generate_alerts(herd_status, count):
        """
        Generate mock GPS alerts for herd detection.
        In a real scenario, this would interface with a GPS sensor or a fixed coordinate table.
        """
        if not herd_status:
            return []
            
        alerts = []
        # Randomly generate coordinates near a fixed center point (e.g., National Park)
        # Center: Serengeti National Park
        center_lat, center_lon = -2.3333, 34.8333
        
        for _ in range(count):
            lat = center_lat + random.uniform(-0.05, 0.05)
            lon = center_lon + random.uniform(-0.05, 0.05)
            alerts.append({
                "lat": lat,
                "lon": lon,
                "type": "Animal Herd",
                "severity": "High" if count > 5 else "Medium",
                "message": f"Detected {count} animals at {lat:.4f}, {lon:.4f}"
            })
            
        return alerts
