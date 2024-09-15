# TESTER FOR THE API ENDPOINTS. Sends requests to the API endpoints
import os

from flask import jsonify
import requests
import json
import TTS
import requests

def request_chatbot_api(message):
    # Define the endpoint URL (update 'http://localhost:5000' if your Flask app is hosted elsewhere)
    url = 'http://192.168 .80.4:5000/chatbot'

    # Prepare the data payload
    data = {
        'message': message  # The message sent by the client
    }

    try:
        # Send the POST request to the Flask endpoint with the message data
        result = requests.post(url, json=data)  # Changed to POST

        # Check if the request was successful
        if result.status_code == 200:
            # Parse the JSON response
            response_data = result.json()
            response = response_data['response']
            confidence_score = response_data['confidence_score']
            intent_tag = response_data['intent_tag']

            # Print or process the received response, confidence score, and intent tag
            print('Response:', response)
            print('Confidence Score:', confidence_score)
            print('Intent Tag:', intent_tag)
            return response, confidence_score, intent_tag
        else:
            print(f'Error: Received status code {result.status_code}')
            return None, None, None
    except Exception as e:
        print(f'An error occurred: {e}')
        return None, None, None


def request_voicebot_api(message):
    # Define the endpoint URL (update 'http://localhost:5000' if your Flask app is hosted elsewhere)
    url = 'http://192.168.80.4:5000/voicebot'
    #url = 'http://172.24.70.176:5000/voicebot'

    # Prepare the data payload
    data = {
        'message': message  # The message sent by the client
    }

    try:
        # Send the POST request to the Flask endpoint with the message data
        result = requests.post(url, json=data)

        # Check if the request was successful
        if result.status_code == 200:
            # Parse the JSON response
            response_data = result.json()
            response = response_data['response']
            confidence_score = response_data['confidence_score']
            intent_tag = response_data['intent_tag']
            audio_file_url = response_data.get('audio_file_url')  # URL to download the audio file

            # Print the received response, confidence score, intent tag, and audio URL
            print('Response:', response)
            print('Confidence Score:', confidence_score)
            print('Intent Tag:', intent_tag)
            print('Audio File URL:', audio_file_url)

            # Optionally download the audio file
            if audio_file_url:
                audio_response = requests.get(audio_file_url)
                if audio_response.status_code == 200:
                    with open("output.mp3", "wb") as f:
                        f.write(audio_response.content)
                    print("Audio file downloaded successfully.")
                else:
                    print("Failed to download the audio file.")

                TTS.play_audio_file("output.mp3")

            return response, confidence_score, intent_tag, audio_file_url

        else:
            print(f'Error: Received status code {result.status_code}')
            return None, None, None, None

    except Exception as e:
        print(f'An error occurred: {e}')
        return None, None, None, None




def request_speak_api(text):
    HOST_IP = 'http://192.168.80.4:5000'
    # HOST_IP = 'http://172.24.70.176:5000'
    AUDIO_PATH = 'output.mp3'

    try:
        response = requests.get(f'{HOST_IP}/speak', params={'text': text})
        if response.status_code == 200:
            # Overwrite the existing file to avoid storage bloat
            with open('output.mp3', 'wb') as f:
                f.write(response.content)
        else:
            print(f"Failed to load audio: {response.status_code}")
    except Exception as e:
        print(f"Failed to load audio: {e}")
    TTS.play_audio_file(AUDIO_PATH)


def request_train_api():
    # Define the endpoint URL (update 'http://localhost:5000' if your Flask app is hosted elsewhere)
    url = 'http://localhost:5000/train_model'
    response = requests.get(url)
    # Check the status code and print the response
    if response.status_code == 200:
        print('Model training initiated.')
    else:
        print('Failed to initiate model training. Status code:', response.status_code)


if __name__ == "__main__":
    # while True:
    #     request_voicebot_api(input("WRITE YOUR MESSAGE: "))
    #     #request_speak_api("HI")
    request_train_api()