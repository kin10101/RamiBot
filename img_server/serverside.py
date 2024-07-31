from flask import Flask, send_file, request
import os
import subprocess

app = Flask(__name__)

# Image directory path
image_directory = '/home/kin/PycharmProjects/RamiBot/Integrated/Assets/Image Infos'  # Directory containing images

# Model path
MODEL_PATH = "en_US-lessac-low.onnx"  # Path for running the model from this directory

# Function to generate audio file from text
def generate_audio_file(text, output_path):
    if os.path.exists(output_path):
        os.remove(output_path)
    command = f'echo "{text}" | piper --model {MODEL_PATH} --output-raw | ffmpeg -y -f s16le -ar 16000 -ac 1 -i - -f mp3 {output_path}'
    subprocess.run(command, shell=True, check=True)

# Endpoint to retrieve an image
@app.route('/get_image/<image_name>')
def get_image(image_name):
    image_path = os.path.join(image_directory, image_name)
    if os.path.exists(image_path):
        return send_file(image_path, mimetype='image/jpeg')
    else:
        return "Image not found", 404

# Endpoint to generate and send audio file
@app.route('/speak', methods=['GET'])
def speak_api():
    text = request.args.get('text', default='', type=str)
    if not text:
        return "No text provided", 400

    output_path = "serveroutput.mp3"
    try:
        generate_audio_file(text, output_path)
        return send_file(output_path, as_attachment=True, download_name="output.mp3")
    except subprocess.CalledProcessError as e:
        return f"An error occurred: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0')
