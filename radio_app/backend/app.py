from flask import Flask, jsonify, render_template # Add render_template
from flask_cors import CORS # Import CORS
import firebase_admin
from firebase_admin import credentials, storage
import os

# Import init_routes from routes.py
from routes import init_routes

app = Flask(__name__) # Static and template folders ('static', 'templates') are correctly picked up by default
CORS(app) # Enable CORS for all routes and origins

# Default to 'firebase-admin-sdk-key.json' in the same directory as app.py (i.e., backend/)
# If FIREBASE_SERVICE_ACCOUNT_KEY_PATH is set, use that path.
SERVICE_ACCOUNT_KEY_FILENAME = 'firebase-admin-sdk-key.json'
backend_dir = os.path.dirname(os.path.abspath(__file__))
DEFAULT_SERVICE_ACCOUNT_KEY_PATH = os.path.join(backend_dir, SERVICE_ACCOUNT_KEY_FILENAME)

SERVICE_ACCOUNT_KEY_PATH_TO_USE = os.environ.get('FIREBASE_SERVICE_ACCOUNT_KEY_PATH', DEFAULT_SERVICE_ACCOUNT_KEY_PATH)
STORAGE_BUCKET_ENV = os.environ.get('FIREBASE_STORAGE_BUCKET')

try:
    if os.path.exists(SERVICE_ACCOUNT_KEY_PATH_TO_USE):
        if not STORAGE_BUCKET_ENV:
            print("Error: FIREBASE_STORAGE_BUCKET environment variable is not set.")
            print("Firebase Admin SDK initialization will be attempted without a default storage bucket, which may limit functionality.")
            # Initialize without storage bucket if not critical, or handle error by not initializing
            cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH_TO_USE)
            firebase_admin.initialize_app(cred)
            print(f"Firebase Admin SDK initialized using key at {SERVICE_ACCOUNT_KEY_PATH_TO_USE} (no default storage bucket).")
        else:
            cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH_TO_USE)
            firebase_admin.initialize_app(cred, {
                'storageBucket': STORAGE_BUCKET_ENV
            })
            print(f"Firebase Admin SDK initialized successfully using key at {SERVICE_ACCOUNT_KEY_PATH_TO_USE}.")
            print(f"Using storage bucket: {STORAGE_BUCKET_ENV}")
    else:
        print(f"Service account key file not found at: {SERVICE_ACCOUNT_KEY_PATH_TO_USE}. Firebase Admin SDK not initialized.")
        print("Please ensure the file exists or the FIREBASE_SERVICE_ACCOUNT_KEY_PATH environment variable is set correctly.")
        print(f"For local development, place '{SERVICE_ACCOUNT_KEY_FILENAME}' in the '{backend_dir}' directory.")
except Exception as e:
    print(f"Error initializing Firebase Admin SDK: {e}")


@app.route('/')
def home():
    return "Radio App Backend is running! Visit <a href='/admin'>/admin</a> for the admin panel."

# New route for the admin panel
@app.route('/admin')
def admin_panel():
    # Check if Firebase Admin SDK was initialized and storage bucket is available
    firebase_initialized_properly = False
    try:
        firebase_admin.get_app() # Check if the default app is initialized
        if STORAGE_BUCKET_ENV:
            firebase_initialized_properly = True
    except ValueError: # Default app not found
        pass
    except Exception as e:
        print(f"Error checking Firebase app status for admin panel: {e}")


    if not firebase_initialized_properly:
        error_message = "Firebase is not properly configured for the admin panel.<ul>"
        if not os.path.exists(SERVICE_ACCOUNT_KEY_PATH_TO_USE):
            error_message += f"<li>Service account key not found at: {SERVICE_ACCOUNT_KEY_PATH_TO_USE}</li>"
        if not STORAGE_BUCKET_ENV:
            error_message += "<li>FIREBASE_STORAGE_BUCKET environment variable is not set.</li>"
        if not firebase_admin._apps: # Check if any app is initialized
             error_message += "<li>Firebase Admin SDK is not initialized at all.</li>"
        error_message += "</ul>Please check backend logs and environment variables."
        return error_message, 500
    return render_template('admin.html')

@app.route('/api/status')
def api_status():
    bucket_name = os.environ.get('FIREBASE_STORAGE_BUCKET', 'Not Configured')
    app_initialized = False
    try:
        firebase_admin.get_app()
        app_initialized = True
    except ValueError:
        pass

    if app_initialized:
        return jsonify(status="Firebase Admin SDK Initialized", storageBucket=bucket_name)
    else:
        additional_info = ""
        if not os.path.exists(SERVICE_ACCOUNT_KEY_PATH_TO_USE):
            additional_info = f"Service account key not found at {SERVICE_ACCOUNT_KEY_PATH_TO_USE}."
        elif not STORAGE_BUCKET_ENV:
             additional_info = "FIREBASE_STORAGE_BUCKET environment variable is not set."
        return jsonify(status="Firebase Admin SDK NOT Initialized", storageBucket=bucket_name, details=additional_info), 500

# Register API routes from routes.py
init_routes(app)

if __name__ == '__main__':
    if not STORAGE_BUCKET_ENV:
        print("CRITICAL WARNING: FIREBASE_STORAGE_BUCKET is not set.")
        print("The application, especially file uploads and the admin panel, may not work correctly.")

    if not firebase_admin._apps:
         print("CRITICAL WARNING: Firebase Admin SDK is not initialized. API endpoints and admin panel functionalities requiring Firebase will not work.")
         print(f"Attempted to use service account key: {SERVICE_ACCOUNT_KEY_PATH_TO_USE}")

    app.run(debug=True, port=5000)
