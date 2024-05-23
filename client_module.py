import requests

# Server URL (use the IP address provided by the server output)
url = 'http://127.0.0.1:5000'

def get_response_from_server(text):
    try:
        response = requests.get(url, params={'text': text})
        response.raise_for_status()  # Raises an error for bad responses (4xx or 5xx)
        print(f"Server response: {response.text}")  # Debugging line
        return response.json().get('response')
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")  # Debugging line
        return None
    except ValueError as e:
        print(f"JSON decode failed: {e}")  # Debugging line
        return None

if __name__ == '__main__':
    text = input("Enter a greeting: ")
    response = get_response_from_server(text)
    if response:
        print(f'Server response: {response}')
    else:
        print('Error: Unable to get a response')
