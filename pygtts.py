import pydub
import subprocess
from playsound import playsound
import threading

from pydub import AudioSegment
from pydub.playback import play


# if not working, try: pip install piper-tts

def speak(text):
    model_path = "../en_US-lessac-medium.onnx"  # Update this with the path to your local model file


    # Define the command to be run with the local model path
    command = f'echo "{text}" | piper --model {model_path} --output-raw | aplay -r 22050 -f S16_LE -t raw -'

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


speak("")
