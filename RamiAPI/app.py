from flask import Flask, send_file, request, jsonify
import os
import subprocess
import chatbot
# if nothing is being encoded onto the audio file, try pip install piper-tts.

app = Flask(__name__)

# Image directory path
image_directory = 'Image_Infos/'  # SET DIRECTORY CONTAINING THE IMAGES TO BE SHOWN

# Model path
MODEL_PATH = "Voices/en_US-lessac-low.onnx"  # Path for running the model from this directory


# Function to generate audio file from text
def generate_audio_file(text, output_path):
    if os.path.exists(output_path):
        os.remove(output_path)
    command = f'echo "{text}" | piper --model {MODEL_PATH} --output-raw | ffmpeg -y -f s16le -ar 16000 -ac 1 -i - serveroutput.mp3'

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


# Endpoint to receive text and return a text response
@app.route('/chatbot', methods=['POST', 'GET'])
def chatbot_api():
    try:
        # Check the request method and get the message accordingly
        if request.method == 'POST':
            data = request.get_json(force=True)
            message = data.get('message')
        else:  # Handling GET request with query parameters (if used)
            message = request.args.get('message')

        response, confidence_score, intent_tag = chatbot.handle_request(message)

        # Return the processed response as JSON
        return jsonify({
            'response': response,
            'confidence_score': confidence_score,
            'intent_tag': intent_tag
        })

    except Exception as e:
        # Log the error and return it as JSON
        app.logger.error(f"Error occurred: {e}")
        return jsonify({'error': str(e)}), 500


# Endpoint to receive text input and return a voice response along with the text response, confidence score, and intent tag
# Combined endpoint for generating text and audio responses
@app.route('/voicebot', methods=['POST', 'GET'])
def voicebot_api():
    try:
        # Retrieve the message depending on the request method
        if request.method == 'POST':
            data = request.get_json(force=True)
            message = data.get('message')
        else:  # Handle GET requests with query parameters
            message = request.args.get('message')

        # Step 1: Get the response from the chatbot (mimicking the /chatbot API)
        response, confidence_score, intent_tag = chatbot.handle_request(message)

        # Step 2: Generate audio from the chatbot response text (mimicking the /speak API)
        output_path = "serveroutput.mp3"
        generate_audio_file(response, output_path)

        # Step 3: Return the chatbot response and a link to the generated audio file
        return jsonify({
            'response': response,
            'confidence_score': confidence_score,
            'intent_tag': intent_tag,
            'audio_file_url': request.url_root + 'get_audio'  # This provides a URL to fetch the audio
        })

    except subprocess.CalledProcessError as e:
        return f"An error occurred during audio generation: {str(e)}", 500
    except Exception as e:
        app.logger.error(f"Error occurred: {e}")
        return jsonify({'error': str(e)}), 500


# Endpoint to serve the generated audio file
@app.route('/get_audio')
def get_audio():
    output_path = "serveroutput.mp3"
    return send_file(output_path, as_attachment=True, download_name="output.mp3")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
