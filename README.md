Jarvis - Virtual Assistant
Jarvis is a Python-based virtual assistant that can recognize voice commands, speak responses, and interact with users via a user-friendly PyQt5 interface. Jarvis can perform various tasks, including opening websites, fetching the latest news, telling jokes or poems, and more.

Features
Voice Commands: Jarvis listens for a wake word ("Jarvis") and responds to a variety of voice commands such as opening websites, telling jokes, playing a birthday song, and fetching the latest news.
Text-to-Speech (TTS): Jarvis can convert its text output to speech using the Google Text-to-Speech (gTTS) API.
Speech Recognition: Jarvis uses the speech_recognition library to process voice input.
PyQt5 Interface:
Two display modes:
UI Mode: A graphical interface with GIF animations.
CMD Mode: A text-based interface for command-line style interactions.
Dark/Light Theme Switcher: Users can toggle between light and dark mode via a dropdown menu.
Audio Feedback: Uses Pygame to play back audio files, such as birthday songs or voice responses.
Google News Integration: Fetches the latest news headlines using the News API.
Demo

Installation
Clone the repository:

Download and install PyQt5
Install pygame, gTTS, and speech_recognition libraries if not already done:
bash
Copy code
pip install pygame gtts speechrecognition requests
API Key Setup:

Jarvis uses the News API to fetch the latest news headlines. To use this feature:
Sign up for an API key at News API.
Replace the newsapi_key in the JarvisApp class with your own API key:
python
Copy code
self.newsapi_key = "your_news_api_key"
Run the application:

You can run the application by executing the following:

bash
Copy code
python jarvis_app.py
Usage
Start and Stop: Use the "Start" and "Stop" buttons to initiate or terminate Jarvis.

Voice Interaction:

Say "Jarvis" to activate voice commands.
Available voice commands:
"Open Google"
"Open YouTube"
"Play Birthday Song"
"Tell me a joke"
"Give me a poem"
"What's the news?"
"What's the time?"
"What's the date?"
Themes:

Toggle between Light and Dark themes via the dropdown at the top-right corner.
Display Modes:

UI Mode: Shows animated GIFs and graphical output.
CMD Mode: Outputs commands and results in text format.
Dependencies
PyQt5: For GUI components
gTTS: For text-to-speech conversion
speech_recognition: For processing voice commands
pygame: For audio playback
requests: To fetch news from the News API
Directory Structure
bash
Copy code
.
├── main.py         # Main Python application file
├── requirements.txt      # Required Python dependencies
├── README.md             # Project documentation
├── photo_gif/            # Contains animated GIFs for the UI
│   ├── eye-v-h.gif       # Eye animation GIF
│   └── audio.gif         # Audio feedback GIF
└── assets/
    └── birthdaysong.mp3  # Audio file for the birthday song
Troubleshooting
Audio issues:
Make sure pygame is properly initialized and that the audio file paths are correct.
Speech recognition errors:
Ensure your microphone is properly configured, and speech_recognition is able to access it.
News API issues:
Double-check your API key, and ensure the request limit of the News API has not been exceeded.
Future Improvements
Add more voice commands and interactions.
Improve error handling for network and voice recognition issues.
Extend UI customization (e.g., more themes or layouts).
