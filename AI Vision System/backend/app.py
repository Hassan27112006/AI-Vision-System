import os
import time
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from backend.config import Config

from backend.modules.herd_detection import HerdDetector
from backend.modules.face_profiling import FaceProfiler
from backend.modules.object_counter import ObjectCounter
from backend.modules.map_alert import MapAlert

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
CORS(app)
app.config.from_object(Config)

# Initialize AI Modules
herd_detector = HerdDetector()
face_profiler = FaceProfiler()
object_counter = ObjectCounter()

# ROUTES
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/herd/')
def herd_page():
    return render_template('herd.html')

@app.route('/face/')
def face_page():
    return render_template('face.html')

@app.route('/counter/')
def counter_page():
    return render_template('counter.html')

# API ENDPOINTS
@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Save Upload
    filename = f"{int(time.time())}_{file.filename}"
    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(upload_path)
    
    return jsonify({
        "filename": filename,
        "url": f"/static/uploads/{filename}"
    })

@app.route('/api/analyze/herd', methods=['POST'])
def analyze_herd():
    data = request.json
    filename = data.get('filename')
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    result = herd_detector.detect(input_path)
    # Add alerts
    result['alerts'] = MapAlert.generate_alerts(result['is_herd'], result['count'])
    
    return jsonify(result)

@app.route('/api/analyze/face', methods=['POST'])
def analyze_face():
    data = request.json
    filename = data.get('filename')
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    result = face_profiler.analyze(input_path)
    return jsonify(result)

@app.route('/api/analyze/object', methods=['POST'])
def analyze_object():
    data = request.json
    filename = data.get('filename')
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    result = object_counter.count_objects(input_path)
    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port)
