import os
import subprocess
import threading

from pydub import AudioSegment
from pydub.playback import play

# if not working, try: pip install piper-tts



def speak(text):
    model_path = os.getenv('MODEL_PATH')

    # params -r = sample rate, -f = format, -t = type
    command = f'echo "{text}" | piper --model {model_path} --output-raw | aplay -r 16000 -f S16_LE -t raw -'

    # Run the command
    subprocess.run(command, shell=True, check=True)

def speak_async(text):
    thread = threading.Thread(target=speak, args=(text,))
    thread.start()

def play_audio_file(file):
    # Load your audio file
    audio = AudioSegment.from_file(file)

    # Play the audio file
    play(audio)


def play_audio_file_async(file):
    thread = threading.Thread(target=play_audio_file, args=(file,))
    thread.start()


if __name__ == '__main__':
    MODEL_PATH = "/en_US-lessac-low.onnx"  # path for running the model from this directory
    # Module testing
    speak("Hello, how are you?")
