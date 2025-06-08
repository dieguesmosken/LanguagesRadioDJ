# Backend

This directory contains the Flask backend for the Radio App.

## Setup
1. Make sure you have Python 3 installed.
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `source venv/bin/activate` (Linux/macOS) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
      (This now includes `Flask-CORS` to handle Cross-Origin Resource Sharing, making local development easier when the frontend is served from a different origin than the backend, e.g. via `file://` protocol).
5. **Firebase Admin SDK:**
   - Place your downloaded `firebase-admin-sdk-key.json` file in this `backend/` directory.
   - **IMPORTANT:** This file should NOT be committed to version control. Ensure it's listed in the main `radio_app/.gitignore` file.
   - You also need to set the `FIREBASE_STORAGE_BUCKET` environment variable to your Firebase project's storage bucket URL (e.g., `your-project-id.appspot.com`). You can set this in your shell or directly in `app.py` for local testing (not recommended for production).

## Running
`python app.py`
The server will start on `http://127.0.0.1:5000`.
- Visit `http://127.0.0.1:5000/admin` for the Admin Panel.

## Data
- Music metadata is stored in `data/metadata.json`.
- Temporary file uploads are stored in `uploads/` before being sent to Firebase. This folder is cleared after upload and should be in `.gitignore`.

## API Endpoints
- `GET /api/status`: Checks the status of the Firebase Admin SDK initialization.
- `POST /api/upload`: Uploads a music file. Expects a multipart form with a 'file' field.
- `GET /api/music`: Retrieves a list of uploaded music tracks and their metadata.

## Admin Panel
- A simple admin panel is available at `/admin` to upload music and view the list of uploaded tracks.
