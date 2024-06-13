from flask import Flask, send_file
import os

app = Flask(__name__)

image_directory = '/home/kin/PycharmProjects/RamiBot/Integrated/Assets/Image Infos'  # Directory containing images

@app.route('/get_image/<image_name>')
def get_image(image_name):
    image_path = os.path.join(image_directory, image_name)
    if os.path.exists(image_path):
        return send_file(image_path, mimetype='image/jpeg')
    else:
        return "Image not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0')
