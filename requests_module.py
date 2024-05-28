
from whisper_live.server import TranscriptionServer


server = TranscriptionServer()
print("Server starting")
server.run("0.0.0.0", 9090)
print("Server started")