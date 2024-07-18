from whisper_live.client import TranscriptionClient
import os
import subprocess
import TTS
import sounddevice as sd
from Voicebot.voice_assistant_module import VoiceAssistant

voice_assistant = VoiceAssistant()

# Set the TERM environment variable if not already set
if 'TERM' not in os.environ:
    os.environ['TERM'] = 'xterm-256color'

last_text = ""

def clear_console():
    """Clear the console based on the operating system."""
    os.system("cls" if os.name == "nt" else "clear")

def sample_callback(text, is_final):
    global last_text
    global client

    try:
        if is_final and text != last_text:
            print("\r" + text[-1], end='', flush=True)
            last_text = text
            client.paused = True
            context =[""]
            out = voice_assistant.handle_command(text[-1],context)
            TTS.speak(out)
            client.paused = False
        else:
            clear_console()
            print(text[-1], end='', flush=True)
    except Exception as e:
        print(f"An error occurred: {e}")

def initialize_client():
    """Initialize the transcription client with the specified parameters."""
    return TranscriptionClient(
        "localhost",
        9090,
        lang="en",
        translate=False,
        model="tiny.en",
        use_vad=True,
        callback=sample_callback
    )

def main():
    global client
    client = initialize_client()
    try:
        client()
    except Exception as e:
        print(f"An error occurred while running the transcription client: {e}")

if __name__ == "__main__":
    main()
