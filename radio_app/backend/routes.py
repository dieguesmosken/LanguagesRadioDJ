from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import firebase_admin
from firebase_admin import storage
import os
import json
import datetime

# Define a Blueprint for API routes
api_bp = Blueprint('api', __name__, url_prefix='/api')

METADATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'metadata.json')
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads') # Temporary local storage before Firebase

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(os.path.join(os.path.dirname(__file__), 'data')):
    os.makedirs(os.path.join(os.path.dirname(__file__), 'data'))


def load_metadata():
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return [] # Return empty list if JSON is invalid
    return []

def save_metadata(data):
    with open(METADATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@api_bp.route('/upload', methods=['POST'])
def upload_music():
    if not firebase_admin._apps: # Check if Firebase app is initialized
        return jsonify(error="Firebase Admin SDK is not initialized. Please check backend configuration."), 500

    if 'file' not in request.files:
        return jsonify(error="No file part in the request"), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify(error="No selected file"), 400

    if file:
        filename = secure_filename(file.filename)
        temp_filepath = os.path.join(UPLOAD_FOLDER, filename)

        try:
            file.save(temp_filepath) # Save locally first

            # Upload to Firebase Storage
            bucket_name = os.environ.get('FIREBASE_STORAGE_BUCKET')
            if not bucket_name:
                # Attempt to clean up before returning error
                if os.path.exists(temp_filepath):
                    os.remove(temp_filepath)
                return jsonify(error="FIREBASE_STORAGE_BUCKET environment variable not set."), 500

            bucket = storage.bucket(bucket_name) # Get bucket using configured name
            blob = bucket.blob(f"music/{filename}") # Store in a 'music/' folder in Firebase

            # Upload the file
            blob.upload_from_filename(temp_filepath)

            # Make the blob publicly viewable AFTER upload
            blob.make_public()
            public_url = blob.public_url

            # Clean up local temp file
            os.remove(temp_filepath)

            # Store metadata
            metadata = load_metadata()
            new_entry = {
                "id": len(metadata) + 1,
                "filename": filename,
                "url": public_url,
                "uploaded_at": datetime.datetime.utcnow().isoformat()
                # Add other fields like title, artist, duration later
            }
            metadata.append(new_entry)
            save_metadata(metadata)

            return jsonify(message="File uploaded successfully to Firebase Storage", file_info=new_entry), 201

        except Exception as e:
            # Clean up local temp file if it exists and an error occurred
            if os.path.exists(temp_filepath):
                os.remove(temp_filepath)
            return jsonify(error=f"An error occurred: {str(e)}"), 500

    return jsonify(error="Unknown error during upload"), 500

@api_bp.route('/music', methods=['GET'])
def get_music_list():
    metadata = load_metadata()
    return jsonify(metadata), 200

def init_routes(app):
    app.register_blueprint(api_bp)
