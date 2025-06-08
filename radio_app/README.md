# Radio Application (Proof of Concept)

This directory contains the source code for a web-based Radio Application. It allows administrators to upload music tracks and users to listen to them via a playback panel.

**Note:** This is a proof-of-concept application. For production use, further enhancements regarding security, scalability, error handling, and features would be necessary.

## Features

*   **Admin Panel:**
    *   Upload music files (e.g., MP3, WAV).
    *   View a list of uploaded music tracks.
*   **User Playback Panel:**
    *   Lists available music tracks.
    *   Allows selection and playback of tracks using a standard HTML5 audio player.
*   **Storage:**
    *   Music files are stored in Google Firebase Storage.
    *   Track metadata is stored in a JSON file (`backend/data/metadata.json`) on the backend.

## Project Structure

*   `backend/`: Contains the Python Flask backend server.
    *   Serves the Admin Panel.
    *   Provides API endpoints for music upload (`/api/upload`) and listing (`/api/music`).
    *   Handles communication with Firebase Storage for uploads.
    *   See `backend/README.md` for specific backend setup and details.
*   `frontend/`: Contains the user-facing playback panel.
    *   HTML, CSS, and JavaScript client-side application.
    *   Communicates with the backend API to fetch track lists and URLs.
    *   See `frontend/README.md` for specific frontend setup and details.
*   `.gitignore`: Specifies intentionally untracked files (e.g., Firebase keys, virtual environments).

## Core Technologies Used

*   **Backend:** Python, Flask, Firebase Admin SDK
*   **Frontend:** HTML, CSS, JavaScript, Firebase Client SDK
*   **Storage:** Google Firebase Storage

## General Setup and Running

Detailed setup instructions are available in the respective `README.md` files for the backend and frontend. However, here's a general overview:

1.  **Firebase Project Setup:**
    *   Create a Firebase project and enable Firebase Storage.
    *   Obtain your Firebase Admin SDK service account key (JSON file).
    *   Obtain your Firebase web app configuration details (`firebaseConfig` object).

2.  **Backend Setup (`radio_app/backend/`):**
    *   Place the service account key in the `backend/` directory (as `firebase-admin-sdk-key.json` or configure path via environment variable).
    *   Set the `FIREBASE_STORAGE_BUCKET` environment variable to your Firebase Storage bucket URL.
    *   Install Python dependencies: `pip install -r requirements.txt`.
    *   Run the backend server: `python app.py`.
    *   The admin panel will be available at `http://localhost:5000/admin`.
    *   Refer to `backend/README.md` for detailed steps.

3.  **Frontend Setup (`radio_app/frontend/`):**
    *   Update `frontend/js/app.js` with your Firebase web app configuration (`firebaseConfig`).
    *   Open `frontend/index.html` in your web browser.
    *   Refer to `frontend/README.md` for detailed steps.

## Next Steps & Potential Enhancements

*   **Security:**
    *   Implement proper authentication and authorization for the admin panel.
    *   Secure Firebase Storage rules for production (currently uses public/test mode rules).
    *   Input validation and sanitization.
*   **Metadata:**
    *   Use a proper database (e.g., Firestore, PostgreSQL, MySQL) instead of a JSON file for metadata.
    *   Allow editing/deleting of tracks.
    *   Extract more metadata from audio files (duration, artist, title, album art).
*   **User Experience:**
    *   More advanced audio player controls.
    *   Playlists, shuffle, repeat.
    *   Search and filtering of tracks.
    *   User accounts and personalized experiences.
*   **Deployment:** Containerization (Docker), deployment to a cloud platform.
