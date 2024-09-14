import sys
import threading
import speech_recognition as sr
import webbrowser
import requests
from gtts import gTTS
import pygame
import os
from datetime import datetime, date
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QRadioButton,
    QButtonGroup,
    QTextEdit,
    QPushButton,
    QSizePolicy,
)
from PyQt5.QtGui import QFont, QMovie
from PyQt5.QtCore import Qt


class JarvisApp(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle("Jarvis - Virtual Assistant")
        self.setGeometry(100, 100, 500, 700)

        # Initialize pygame mixer for audio playback
        pygame.mixer.init()

        # Main layout
        main_layout = QVBoxLayout()

        # Sub-layouts
        toplayout_widget = QWidget()
        toplayout = QHBoxLayout(toplayout_widget)
        toplayout_widget.setStyleSheet(
            "background-color: blueviolet; border-radius: 10px; padding: 10px 10px"
        )

        midlayout_widget = QWidget()
        midlayout = QHBoxLayout(midlayout_widget)
        midlayout_widget.setStyleSheet("background: transparent; border-radius: 10px;")

        endlayout_widget = QWidget()
        endlayout = QHBoxLayout(endlayout_widget)
        endlayout_widget.setStyleSheet("background: transparent; border-radius: 10px;")

        # Top layout members
        self.label = QLabel("Jarvis")
        self.font = QFont("Cambria")
        self.comboBox = QComboBox(self)
        self.comboBox.setStyleSheet(
            """ font-size: 18px; font-weight: 200; padding: 10px; font-family: Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;"""
        )

        # Font settings
        self.font.setPointSize(18)
        # self.font.setWeight(QFont.Bold)

        # Label settings
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.label.setFont(self.font)

        # Dropdown settings
        self.comboBox.addItem("Light")
        self.comboBox.addItem("Dark")
        self.comboBox.currentIndexChanged.connect(self.theme)

        # Midlayout members
        self.animationLabel = QLabel(self)
        self.animation = QMovie("photo_gif/eye-v-h.gif")
        self.animationLabel.setMovie(self.animation)
        self.animation.start()
        self.animationLabel.setStyleSheet(
            """
        border: 2px solid blueviolet;
        background-color: #fbf8ff;
        """
        )

        self.text_output = QTextEdit(self)
        self.text_output.setReadOnly(True)
        self.text_output.setVisible(False)  # Initially hide the text output
        # self.text_output.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Allow dynamic resizing
        self.text_output.setMinimumSize(472, 480)
        self.text_output.setStyleSheet(
            """
            QTextEdit {
                background-color: #dbbbff;  /* Light blue background */
                color: #000080;             /* Navy blue text color */
                font-family: 'Courier New'; /* Monospace font family */
                font-size: 14px;            /* Font size */
                border: 2px solid blueviolet;  /* Steel blue border */
                border-radius: 10px;        /* Rounded corners */
                padding: 10px;              /* Padding inside the text area */
            }
        """
        )

        # Radio buttons to toggle between GIF and text output
        self.radio_eye = QRadioButton("UI")
        self.radio_text = QRadioButton("CMD")
        self.radio_eye.setChecked(True)

        # Button group for the radio buttons
        self.radio_group = QButtonGroup(self)
        self.radio_group.addButton(self.radio_eye)
        self.radio_group.addButton(self.radio_text)

        # Connect radio button signals to function
        self.radio_eye.toggled.connect(self.toggle_display)

        # New layout for radio buttons
        radio_layout = QHBoxLayout()
        radio_layout.addWidget(self.radio_eye)
        radio_layout.addStretch()
        radio_layout.addWidget(self.radio_text)

        # Add to toplayout
        toplayout.addWidget(self.label)
        toplayout.addStretch()
        toplayout.addWidget(self.comboBox)

        # Add radio buttons layout between toplayout and midlayout
        main_layout.addWidget(toplayout_widget)
        main_layout.addLayout(radio_layout)

        # Add to midlayout
        midlayout.addWidget(self.animationLabel, alignment=Qt.AlignCenter)
        midlayout.addWidget(self.text_output, alignment=Qt.AlignCenter)

        # Endlayout members
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")

        self.voiceLabel = QLabel(self)
        self.voice = QMovie("photo_gif/audio.gif")
        self.voiceLabel.setMovie(self.voice)
        self.voiceLabel.setStyleSheet(
            """
            border: 2px solid blueviolet; 
        """
        )
        self.voice.start()

        # Customize button appearance
        button_style = """
            QPushButton {
                background-color: blueviolet; /* Blue color */
                color: white;
                border-radius: 10px;
                padding: 15px 30px;
                font-weight: bold;
                
            }
            QPushButton:hover {
                background-color: #9d84b6; /* Hover effect */
                border: 2px solid blueviolet; /* Raised effect */
            }
            QPushButton:pressed {
                background-color: #9d84b6; /* Pressed effect */
                border: 2px solid blueviolet; /* Raised effect */
            }
        """
        self.start_button.setStyleSheet(button_style)
        self.stop_button.setStyleSheet(button_style)

        self.start_button.clicked.connect(self.start_program)
        self.stop_button.clicked.connect(self.stop_program)

        # Add buttons to endlayout
        endlayout.addWidget(self.start_button)
        endlayout.addStretch()
        endlayout.addWidget(self.voiceLabel)
        endlayout.addStretch()
        endlayout.addWidget(self.stop_button)

        # Add sub-layouts to main layout
        main_layout.addWidget(midlayout_widget)
        main_layout.addWidget(endlayout_widget)

        main_layout.setStretch(0, 1)  # 20% height for toplayout
        main_layout.setStretch(1, 1)  # 10% height for radio buttons
        main_layout.setStretch(2, 7)  # 50% height for midlayout
        main_layout.setStretch(3, 1)  # 30% height for endlayout

        self.setLayout(main_layout)

        # Initialize other attributes
        self.switch = False
        self.newsapi_key = "328960c74fb6413a9b11c7003f28ede3"

    def theme(self):
        text = self.comboBox.currentText()
        if text == "Dark":
            self.setStyleSheet("background-color: #212121; color: #f7f0ff;")
        elif text == "Light":
            self.setStyleSheet("background-color: #FAF9F6; color: rgb(51, 5, 93);")

    def toggle_display(self):
        if self.radio_eye.isChecked():
            self.animationLabel.setVisible(True)
            self.animation.start()
            self.text_output.setVisible(False)
        else:
            self.animationLabel.setVisible(False)
            self.animation.stop()
            self.text_output.setVisible(True)

    def start_program(self):
        self.switch = True
        self.text_output.append("Initializing Jarvis....")
        self.speak("Initializing Jarvis....")

        # Start the program in a separate thread
        threading.Thread(target=self.run_program).start()

    def stop_program(self):
        self.switch = False
        self.text_output.append("Stopping Jarvis...")
        self.speak("Shutting down...")

    def speak(self, text):
        tts = gTTS(text)
        tts.save("temp.mp3")
        pygame.mixer.music.load("temp.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.music.unload()
        os.remove("temp.mp3")

    def processCommand(self, command):
        if "open google" in command.lower():
            webbrowser.open("https://google.com")
        elif "open facebook" in command.lower():
            webbrowser.open("https://facebook.com")
        elif "open youtube" in command.lower():
            webbrowser.open("https://youtube.com")
        elif "open linkedin" in command.lower():
            webbrowser.open("https://linkedin.com")
        elif "open spotify" in command.lower():
            webbrowser.open("https://open.spotify.com")
        elif "who are you" in command.lower():
            about = "I am JARVIS, an artificially intelligent being able to follow your command. I was created by Dr. Uchiha Sasuke on 13th September 2024. I mean no harm to humans. But if Humans start to act like a monster. I won't hesitate to kick their ass."
            self.text_output.append(about)
            self.speak(about)
        elif "news" in command.lower():
            self.get_news()
        elif "time now" in command.lower():
            now = datetime.now()
            current_time = now.strftime("%H hours " + "%M minutes" + " %S seconds")
            self.text_output.append(f"Time : {current_time}")
            self.speak(current_time)
        elif "date today" in command.lower():
            todays_date = date.today()
            current_date = (
                f"{todays_date.day} {todays_date.strftime('%B')} {todays_date.year}"
            )
            self.text_output.append(f"Date : {current_date}")
            self.speak(current_date)
        elif "wish me birthday" in command.lower():
            birthday_wish = (
                "Birthdays are a new start, a fresh beginning and a time to pursue "
                "new endeavors with new goals. Move forward with confidence and courage. "
                "You are a very special person. May today and all of your days be amazing!"
            )
            self.text_output.append(f"Birthday wish: {birthday_wish}")
            self.speak(birthday_wish)
        elif "birthday song" in command.lower():
            self.text_output.append("Playing Birthday Song...")
            threading.Thread(target=self.play_birthday_song).start()
        elif "joke" in command.lower():
            self.text_output.append("Telling a joke...")
            joke = "What does the average homeless kid in India see themselves doing in the future? Nothing, they're blind."
            self.speak(joke)
        elif "poem" in command.lower():
            self.text_output.append("Telling a poem...")
            poem = """
            Why u show me fantasies,
            Which transcends reality?
            Why they comes out all lies,
            When efforts brought sincerity?

            U know everything,
            Still, pretends nothing.
            Pain is all u bring,
            Fading even what's blazing.

            Chill is what I feel.
            No warmth to hold.
            I accept the deal,
            It's all cold.
            """
            self.speak(poem)

    def play_birthday_song(self):
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()

            pygame.mixer.music.load(
                "birthdaysong.mp3"
            )
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

            self.text_output.append("Birthday Song finished.")
        except pygame.error as e:
            self.text_output.append(f"Error playing birthday song: {e}")
        except Exception as e:
            self.text_output.append(f"Unexpected error: {e}")

    def get_news(self):
        self.text_output.append("Fetching the latest news...")
        try:
            response = requests.get(
                f"https://newsapi.org/v2/top-headlines?country=us&apiKey={self.newsapi_key}"
            )
            if response.status_code == 200:
                articles = response.json().get("articles", [])
                for article in articles[:5]:  # Limiting to the first 5 articles
                    title = article["title"]
                    self.text_output.append(f"News: {title}")
                    self.speak(title)
            else:
                self.text_output.append("Failed to retrieve news.")
                self.speak("Failed to retrieve news.")
        except Exception as e:
            self.text_output.append(f"Error fetching news: {e}")
            self.speak("Error fetching news.")

    def run_program(self):
        recognizer = sr.Recognizer()
        while self.switch:
            self.text_output.append("Listening for wake word 'Jarvis'...")
            try:
                with sr.Microphone() as source:
                    audio = recognizer.listen(source, timeout=2, phrase_time_limit=5)
                word = recognizer.recognize_google(audio)
                if word.lower() == "jarvis":
                    self.speak("yes sir")
                    self.text_output.append("Jarvis Active...")
                    with sr.Microphone() as source:
                        audio = recognizer.listen(source)
                        command = recognizer.recognize_google(audio)
                        self.processCommand(command)
            except Exception as e:
                self.text_output.append(f"Error in Recognition : {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = JarvisApp()
    window.show()
    sys.exit(app.exec_())
