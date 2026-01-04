from flask import Flask, request, jsonify
from flask_cors import CORS
import face_recognition
import numpy as np
import base64
from PIL import Image
import io
import sqlite3
import pickle
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Database setup
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'faces.db')
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'database', 'images')

# Ensure directories exist
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def init_db():
    """Initialize the database"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS faces (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            encoding BLOB NOT NULL,
            image_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def decode_image(image_data):
    """Decode base64 image to numpy array"""
    try:
        # Remove data URL prefix if present
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        return np.array(image)
    except Exception as e:
        print(f"Error decoding image: {e}")
        return None

@app.route('/api/register', methods=['POST'])
def register_face():
    """Register a new face with a name"""
    try:
        data = request.json
        name = data.get('name')
        image_data = data.get('image')
        
        if not name or not image_data:
            return jsonify({'error': 'Name and image are required'}), 400
        
        # Decode image
        image_np = decode_image(image_data)
        if image_np is None:
            return jsonify({'error': 'Invalid image data'}), 400
        
        # Detect faces
        face_locations = face_recognition.face_locations(image_np)
        
        if len(face_locations) == 0:
            return jsonify({'error': 'No face detected in the image'}), 400
        
        if len(face_locations) > 1:
            return jsonify({'error': 'Multiple faces detected. Please upload an image with only one face'}), 400
        
        # Get face encoding
        face_encodings = face_recognition.face_encodings(image_np, face_locations)
        face_encoding = face_encodings[0]
        
        # Save image
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        image_filename = f"{name.replace(' ', '_')}_{timestamp}.jpg"
        image_path = os.path.join(UPLOAD_FOLDER, image_filename)
        
        image_pil = Image.fromarray(image_np)
        image_pil.save(image_path)
        
        # Store in database
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute(
            'INSERT INTO faces (name, encoding, image_path) VALUES (?, ?, ?)',
            (name, pickle.dumps(face_encoding), image_path)
        )
        conn.commit()
        face_id = c.lastrowid
        conn.close()
        
        return jsonify({
            'success': True,
            'message': f'Face registered successfully for {name}',
            'id': face_id,
            'name': name
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recognize', methods=['POST'])
def recognize_face():
    """Recognize a face from an image"""
    try:
        data = request.json
        image_data = data.get('image')
        
        if not image_data:
            return jsonify({'error': 'Image is required'}), 400
        
        # Decode image
        image_np = decode_image(image_data)
        if image_np is None:
            return jsonify({'error': 'Invalid image data'}), 400
        
        # Detect faces
        face_locations = face_recognition.face_locations(image_np)
        
        if len(face_locations) == 0:
            return jsonify({'error': 'No face detected in the image'}), 400
        
        # Get face encodings for all faces in the image
        face_encodings = face_recognition.face_encodings(image_np, face_locations)
        
        # Get all known faces from database
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT id, name, encoding FROM faces')
        known_faces = c.fetchall()
        conn.close()
        
        if len(known_faces) == 0:
            return jsonify({'error': 'No faces registered in the system'}), 400
        
        known_face_encodings = []
        known_face_names = []
        known_face_ids = []
        
        for face_id, name, encoding_blob in known_faces:
            known_face_encodings.append(pickle.loads(encoding_blob))
            known_face_names.append(name)
            known_face_ids.append(face_id)
        
        # Recognize faces
        recognized_faces = []
        
        for face_encoding, face_location in zip(face_encodings, face_locations):
            # Compare with known faces
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            
            name = "Unknown"
            confidence = 0
            face_id = None
            
            if True in matches:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    face_id = known_face_ids[best_match_index]
                    # Convert distance to confidence (0-100%)
                    confidence = round((1 - face_distances[best_match_index]) * 100, 2)
            
            top, right, bottom, left = face_location
            recognized_faces.append({
                'name': name,
                'confidence': confidence,
                'location': {
                    'top': int(top),
                    'right': int(right),
                    'bottom': int(bottom),
                    'left': int(left)
                },
                'id': face_id
            })
        
        return jsonify({
            'success': True,
            'faces': recognized_faces,
            'count': len(recognized_faces)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/faces', methods=['GET'])
def get_all_faces():
    """Get all registered faces"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT id, name, created_at FROM faces ORDER BY created_at DESC')
        faces = c.fetchall()
        conn.close()
        
        face_list = []
        for face_id, name, created_at in faces:
            face_list.append({
                'id': face_id,
                'name': name,
                'created_at': created_at
            })
        
        return jsonify({
            'success': True,
            'faces': face_list,
            'count': len(face_list)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/faces/<int:face_id>', methods=['DELETE'])
def delete_face(face_id):
    """Delete a registered face"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Get image path before deleting
        c.execute('SELECT image_path FROM faces WHERE id = ?', (face_id,))
        result = c.fetchone()
        
        if result:
            image_path = result[0]
            # Delete from database
            c.execute('DELETE FROM faces WHERE id = ?', (face_id,))
            conn.commit()
            
            # Delete image file if exists
            if image_path and os.path.exists(image_path):
                os.remove(image_path)
            
            conn.close()
            return jsonify({'success': True, 'message': 'Face deleted successfully'}), 200
        else:
            conn.close()
            return jsonify({'error': 'Face not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get system statistics"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM faces')
        total_faces = c.fetchone()[0]
        conn.close()
        
        return jsonify({
            'success': True,
            'total_faces': total_faces
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
