from whisper_live.client import TranscriptionClient
audio_file_path = "/home/kin/PycharmProjects/RamiBot/Integrated/output.mp3"
client = TranscriptionClient("localhost", 9090)
client(audio_file_path)