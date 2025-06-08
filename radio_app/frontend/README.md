# Frontend

This directory contains the HTML, CSS, and JavaScript for the user-facing radio player.

## Setup
1. **Firebase Configuration:**
   - Open `js/app.js`.
   - Replace the placeholder `firebaseConfig` object with the actual Firebase configuration details for your web app. You can get this from your Firebase project settings. While the app fetches track URLs from the backend (which sourced them from Firebase Storage), having the correct Firebase client configuration in `js/app.js` is good practice and was part of the initial setup, though not strictly necessary for playing publicly accessible Firebase Storage URLs if the backend provides them directly. The current JavaScript attempts to initialize Firebase but will still try to fetch the music list if this step has issues (displaying a warning).
2. **Backend Server:**
   - Ensure the backend server (`radio_app/backend/app.py`) is running, as this frontend fetches the music list from the `/api/music` endpoint served by the backend. The backend needs to be accessible from where you open the `index.html` (e.g., same machine, or CORS configured on the backend if different origins).

## Running
Simply open `index.html` in a web browser (e.g., `file:///path/to/radio_app/frontend/index.html`). It will attempt to connect to the backend API (assumed to be running on the same host or correctly configured for CORS) to load the playlist.

## Features
- Lists available music tracks fetched from the backend's `/api/music` endpoint.
- Allows selection of a track from the playlist by clicking on it.
- Plays the selected track using the HTML5 `<audio>` element.
- Displays the filename of the currently selected track.
- Provides basic audio controls (play, pause, volume, seek) via the default browser controls for the `<audio>` element.
- Includes basic styling for the player and playlist sections.
- Playlist is scrollable if the number of tracks exceeds the designated height.
- Displays loading and error messages for playlist fetching and audio playback issues.
