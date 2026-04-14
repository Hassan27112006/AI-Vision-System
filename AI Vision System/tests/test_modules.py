import pytest
import os
import cv2
import numpy as np
from backend.modules.herd_detection import HerdDetector
from backend.modules.face_profiling import FaceProfiler
from backend.modules.object_counter import ObjectCounter
from backend.config import Config

# Mock an image for tests
@pytest.fixture
def mock_image():
    path = os.path.join(Config.UPLOAD_FOLDER, 'test_mock.jpg')
    img = np.zeros((640, 640, 3), dtype=np.uint8)
    cv2.imwrite(path, img)
    yield path
    if os.path.exists(path):
        os.remove(path)

def test_object_counter_logic(mock_image):
    counter = ObjectCounter()
    # On a black image, should return 0 or near 0
    res = counter.count_objects(mock_image)
    assert 'total_count' in res
    assert 'breakdown' in res
    assert os.path.exists(os.path.join(Config.BASE_DIR, res['output_url'].lstrip('/')))

def test_face_profiler_init():
    profiler = FaceProfiler()
    # It might fail if model isn't downloaded, but init should be fine
    assert profiler.detector is not None

def test_herd_detector_logic(mock_image):
    detector = HerdDetector()
    res = detector.detect(mock_image)
    assert 'count' in res
    assert 'is_herd' in res
