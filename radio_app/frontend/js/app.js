// Firebase Config (user needs to replace this)
const firebaseConfig = {
    apiKey: "YOUR_API_KEY",
    authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
    projectId: "YOUR_PROJECT_ID",
    storageBucket: "YOUR_PROJECT_ID.appspot.com",
    messagingSenderId: "YOUR_SENDER_ID",
    appId: "YOUR_APP_ID"
};

// DOM Elements
const trackTitleElement = document.getElementById('track-title');
const trackArtistElement = document.getElementById('track-artist');
// const albumArtElement = document.getElementById('album-art');
const audioPlayer = document.getElementById('audio-player');
const trackListElement = document.getElementById('track-list');
const loadingMessage = document.getElementById('loading-message');
const errorMessage = document.getElementById('error-message');

let currentTrackList = []; // To store the fetched track list

// Initialize Firebase
function initializeFirebase() {
    try {
        if (firebaseConfig.apiKey === "YOUR_API_KEY" || !firebaseConfig.projectId || firebaseConfig.projectId === "YOUR_PROJECT_ID") {
            console.warn("Firebase is not configured. Please update firebaseConfig in js/app.js");
            showError("Firebase is not configured. Please update js/app.js with your Firebase project details. If you don't need Firebase for listing/playing music (e.g. using local URLs), you can ignore this for now.");
            loadingMessage.style.display = 'none';
            // Allow app to proceed if backend serves non-Firebase URLs
            // return false;
            return true; // Let's assume for now it might proceed if backend provides full URLs
        }
        firebase.initializeApp(firebaseConfig);
        // const storage = firebase.storage(); // Not directly used here yet, but good to have if needed
        console.log("Firebase App initialized successfully.");
        return true;
    } catch (e) {
        console.error("Could not initialize Firebase", e);
        showError("Error initializing Firebase. Check console for details.");
        loadingMessage.style.display = 'none';
        return false;
    }
}

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
    loadingMessage.style.display = 'none';
}

function hideError() {
    errorMessage.style.display = 'none';
}

async function fetchMusicList() {
    hideError();
    loadingMessage.style.display = 'block';
    trackListElement.innerHTML = ''; // Clear previous list

    try {
        // Assuming backend API is available at /api/music
        const response = await fetch('/api/music');
        if (!response.ok) {
            const errorData = await response.json().catch(() => null); // Try to get error from backend
            throw new Error(`HTTP error! status: ${response.status} - ${errorData ? errorData.error : response.statusText}`);
        }
        currentTrackList = await response.json();

        if (currentTrackList.length === 0) {
            loadingMessage.textContent = 'No tracks available in the playlist.';
        } else {
            populatePlaylist(currentTrackList);
            loadingMessage.style.display = 'none';
        }
    } catch (error) {
        console.error('Error fetching music list:', error);
        showError(`Failed to load music list: ${error.message}. Ensure the backend is running and accessible on the same host/port or CORS is configured.`);
        // No need to hide loadingMessage here as showError does it
    }
}

function populatePlaylist(tracks) {
    trackListElement.innerHTML = ''; // Clear existing items
    tracks.forEach((track, index) => {
        const listItem = document.createElement('li');
        listItem.textContent = track.filename; // Or track.title if we add it later
        listItem.dataset.trackIndex = index; // Store index for easy access
        listItem.addEventListener('click', function() {
            selectTrack(parseInt(this.dataset.trackIndex));
            // Remove 'selected' class from all others
            document.querySelectorAll('#track-list li').forEach(li => li.classList.remove('selected'));
            // Add 'selected' class to the clicked one
            this.classList.add('selected');
        });
        trackListElement.appendChild(listItem);
    });
}

function selectTrack(trackIndex) {
    if (trackIndex >= 0 && trackIndex < currentTrackList.length) {
        const track = currentTrackList[trackIndex];
        trackTitleElement.textContent = track.filename; // Use filename as title for now
        trackArtistElement.textContent = track.artist || "Unknown Artist"; // If artist metadata exists
        audioPlayer.src = track.url;
        // audioPlayer.play(); // Optional: auto-play on selection - might be annoying
        console.log("Selected track:", track);

        // Highlight the selected track in the list
        document.querySelectorAll('#track-list li').forEach(li => {
            if (parseInt(li.dataset.trackIndex) === trackIndex) {
                li.classList.add('selected');
            } else {
                li.classList.remove('selected');
            }
        });
    }
}

// Initial setup
if (initializeFirebase()) { // Firebase init is called
    fetchMusicList(); // Then fetch the list
} else {
    // Error message already shown by initializeFirebase or showError
    // Potentially, one could still call fetchMusicList() if Firebase is optional for the app's core functionality
    // For this app, music URLs come from our backend, which gets them from Firebase, so Firebase client config isn't strictly needed for playback if backend is proxying
    // However, the current instruction is to have Firebase config in frontend.
    console.log("Firebase not initialized, music list might not load if URLs require Firebase context (which they don't in current setup).");
    // fetchMusicList(); // Decide if to fetch even if Firebase client init fails
}

// Event listener for when audio finishes
audioPlayer.addEventListener('ended', () => {
    console.log('Track ended');
    // Future: Implement auto-play next, shuffle, or repeat functionality here
    // For example, find current track index, play next if available
    // const currentSelectedLi = document.querySelector('#track-list li.selected');
    // if (currentSelectedLi) {
    //     let currentIndex = parseInt(currentSelectedLi.dataset.trackIndex);
    //     if (currentIndex + 1 < currentTrackList.length) {
    //         selectTrack(currentIndex + 1);
    //         audioPlayer.play();
    //     }
    // }
});

audioPlayer.addEventListener('error', (e) => {
    console.error('Error with audio playback:', e);
    // Display a more user-friendly error if possible
    let errorDetails = "Unknown audio error.";
    if (e.target && e.target.error) {
        switch (e.target.error.code) {
            case e.target.error.MEDIA_ERR_ABORTED:
                errorDetails = 'Playback aborted by the user.';
                break;
            case e.target.error.MEDIA_ERR_NETWORK:
                errorDetails = 'A network error caused the audio download to fail.';
                break;
            case e.target.error.MEDIA_ERR_DECODE:
                errorDetails = 'The audio playback was aborted due to a corruption problem or because the audio used features your browser did not support.';
                break;
            case e.target.error.MEDIA_ERR_SRC_NOT_SUPPORTED:
                errorDetails = 'The audio could not be loaded, either because the server or network failed or because the format is not supported.';
                break;
            default:
                errorDetails = 'An unknown error occurred during audio playback.';
        }
    }
    showError(`Audio playback error: ${errorDetails} (URL: ${audioPlayer.src})`);
    trackTitleElement.textContent = "Error playing track";
});
