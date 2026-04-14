import pytest
from backend.app import app
import os
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test if home page loads."""
    res = client.get('/')
    assert res.status_code == 200
    assert b"Next-Gen Computer Vision" in res.data

def test_herd_page(client):
    """Test if herd module loads."""
    res = client.get('/herd/')
    assert res.status_code == 200
    assert b"Animal Herd Detection" in res.data

def test_face_page(client):
    """Test if face profiling module loads."""
    res = client.get('/face/')
    assert res.status_code == 200
    assert b"Face Profiling Intelligence" in res.data

def test_object_counter_page(client):
    """Test if object counter module loads."""
    res = client.get('/counter/')
    assert res.status_code == 200
    assert b"Intelligent Object Counting" in res.data

def test_api_upload_fail(client):
    """Test API upload fail case (no file)."""
    res = client.post('/api/upload')
    assert res.status_code == 400
    assert b"No file uploaded" in res.data
