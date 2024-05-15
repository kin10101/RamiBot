import requests

def get_http_image(url, filename):
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Open the file in binary mode and write the response content to it
        with open(filename, 'wb') as file:
            file.write(response.content)
    else:
        print(f"Failed to get image. HTTP response code: {response.status_code}")

# Use the function
get_http_image("http://example.com/path/to/image.jpg", "downloaded_image.jpg")