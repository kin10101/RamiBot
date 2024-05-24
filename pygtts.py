from gtts import gTTS
from playsound import playsound
import pyaudio
import wave
import os
import sounddevice


def speak(text, lang='en'):
    # Create the output directory if it doesn't exist
    output_dir = "../Integrated/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Define the MP3 file path
    mp3_file = os.path.join(output_dir, "output.mp3")

    # Create a gTTS object and save the speech as an MP3 file
    tts = gTTS(text, lang=lang)
    tts.save(mp3_file)

    # Play the MP3 file
    playsound(mp3_file)

def play_audio_file(file):
    playsound(file)



if __name__ == "__main__":
    speak("Hello, this is a test.")
