""" Text to speech functionality using flask and PiperTTS. Make sure to connect to the server before running this
script."""
import os
import threading

import requests
from pydub import AudioSegment
from pydub.playback import play
from dotenv import load_dotenv

load_dotenv()

HOST_IP = os.getenv('HOST_IP')  # Use this for deployment
AUDIO_PATH = os.getenv('AUDIO_PATH')


# override for local testing
# HOST_IP = 'http://127.0.0.1:5000'


def TTSapi(text):
    """Request audio from the server and save it locally. Takes in the text as a parameter."""
    try:
        response = requests.get(f'{HOST_IP}/speak', params={'text': text})
        if response.status_code == 200:
            # Check if the file exists
            if not os.path.isfile(AUDIO_PATH):
                # Create the file if it doesn't exist
                open(AUDIO_PATH, 'a').close()

            # Overwrite the existing file to avoid storage bloat
            with open(AUDIO_PATH, 'wb') as f:
                f.write(response.content)
        else:
            print(f"Failed to load audio: {response.status_code}")
    except Exception as e:
        print(f"Failed to load audio: {e}")


def speak(text):
    TTSapi(text)
    # Play the audio file
    play_audio_file(AUDIO_PATH)
    # delete the audio file after playing
    os.remove(AUDIO_PATH)


def speak_async(text):
    thread = threading.Thread(target=speak, args=(text,))
    thread.start()


def play_audio_file(file):
    # Load your audio file
    audio = AudioSegment.from_file(file)
    # Play the audio file
    play(audio)


# async functions


def play_audio_file_async(file):
    thread = threading.Thread(target=play_audio_file, args=(file,))
    thread.start()


if __name__ == '__main__':
    # testing the module
    speak("Hello, how are you?")
