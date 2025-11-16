# Audio-Email-Navigator
Audio Email Navigator (NLP-Based)

This project is an audio-driven email system designed to help visually impaired users or anyone who prefers voice-based interaction.
It allows users to listen to emails, compose emails through speech, and navigate the mailbox using voice commands.

Features

Voice-based email reading

Speech-to-text for composing emails

Natural language command detection

Send, read, reply, and navigate emails

Text-to-speech for audio output

Technologies Used

Python

Speech Recognition (SpeechRecognition / Google STT)

Text-to-Speech (pyttsx3 or gTTS)

NLP (spaCy / NLTK)

SMTP & IMAP for email handling

How to Run

Install dependencies:

pip install -r requirements.txt


Add your email and app password in the config file.

Run the project:

python main.py

Voice Commands (Examples)

“Read my emails”

“Send an email to ___”

“Reply to this email”

“Next email”
