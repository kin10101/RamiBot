import time
from faster_whisper import WhisperModel

# def transcribe_audio():
#     start_time = time.time()
#
#     model = WhisperModel("tiny.en")
#     print("Model loaded")
#     segments, _ = model.transcribe("/home/kin/PycharmProjects/RamiBot/Integrated/output.mp3")
#     text = ''.join(segment.text for segment in segments)
#
#     end_time = time.time()
#     elapsed_time = end_time - start_time
#     print(f"Function transcribe_audio took {elapsed_time} seconds to execute")
#
#     return text
#
# # Call the function
# transcribe_audio()



# import whisper
# model = whisper.load_model("tiny.en")
# print("Model loaded")
# result = model.transcribe("/home/kin/PycharmProjects/RamiBot/Integrated/output.mp3")
# print(f' The text in video: \n {result["text"]}')
#

import pyaudio
import wave


def record_audio(duration, filename):
    # Set up audio recording parameters
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    rate = 16000  # Sample rate (Hz)

    # Initialize PyAudio object
    p = pyaudio.PyAudio()

    # Open a stream to record audio
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

    print("Recording...")

    # Initialize array to store frames
    frames = []

    # Record audio in chunks for the given duration
    for _ in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    print("Recording finished")

    # Save the recorded audio to a file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))


def transcribe_audio_from_mic(duration=5):
    start_time = time.time()

    # Record audio from microphone and save to a temporary file
    audio_filename = "temp_audio.wav"
    record_audio(duration, audio_filename)

    # Load Whisper model
    model = WhisperModel("tiny")
    print("Model loaded")

    # Transcribe the audio file
    segments, _ = model.transcribe(audio_filename)
    text = ''.join(segment.text for segment in segments)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Function transcribe_audio_from_mic took {elapsed_time} seconds to execute")

    return text


# Example usage
transcribed_text = transcribe_audio_from_mic(duration=5)
print("Transcribed text:", transcribed_text)