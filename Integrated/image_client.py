import requests

HOST_IP = 'http://192.168.80.4:5000'
IMAGE_PATH = 'downloaded_image.jpg'  # Define a constant path for the image to prevent storage bloat


def request_image(image):
    """Request an image from the server and save it locally. takes in the image name as a parameter."""
    try:
        response = requests.get(f'{HOST_IP}/get_image/{image}')
        if response.status_code == 200:

            # write to temp file
            with open(IMAGE_PATH, 'wb') as f:
                f.write(response.content)
                print("Image downloaded successfully")
        else:
            print(f"Failed to load image: {response.status_code}")
    except Exception as e:
        print(f"Failed to load image: {e}")

def update_image_source(dt):
    screen_manager.get_screen('client').ids.img.source = IMAGE_PATH
    screen_manager.get_screen('client').ids.img.reload()