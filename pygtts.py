from gtts import gTTS
from pydub import AudioSegment
import pyaudio
import wave
import os
import sounddevice

def speak(text, lang='en'):
    # Create the output directory if it doesn't exist
    output_dir = "../Integrated/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Define file paths
    mp3_file = os.path.join(output_dir, "output.mp3")
    wav_file = os.path.join(output_dir, "output.wav")

    # Create a gTTS objHello, this is a test.ect
    tts = gTTS(text, lang=lang)

    # Save the speech as an MP3 file
    tts.save(mp3_file)

    # Convert MP3 to WAV
    sound = AudioSegment.from_mp3(mp3_file)
    sound.export(wav_file, format="wav")

    # Play the WAV file using pyaudio
    play_audio_file(wav_file)

def play_audio_file(file):
    # Open the WAV file
    wf = wave.open(file, 'rb')

    # Instantiate PyAudio
    p = pyaudio.PyAudio()

    # Open a .Stream object to write the WAV file to
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # Read data in chunks
    chunk = 1024
    data = wf.readframes(chunk)

    # Play the sound by writing the audio data to the stream
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(chunk)

    # Close and terminate the stream
    stream.close()
    p.terminate()


import pyttsx3


if __name__ == "__main__":
    speak("Hello, this is a test.")
