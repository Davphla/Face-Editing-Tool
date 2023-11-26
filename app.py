import json

import numpy
from flask import Flask, render_template, request, send_file, jsonify
from PIL import Image, ImageDraw
from detect_face import *
import os
import uuid
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# set 16MB
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# allowed extension
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    # check allowed file extension list
    if '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
        return True
    else:
        return False


@app.route('/hello')
def index():
    return "Hello World"


# return cropped image dir and coordinates
@app.route('/upload', methods=['POST'])
def upload():
    # upload type / multipart/form-data
    if 'file' not in request.files:
        return "No file part"
    # print(request.files)
    file = request.files['file']
    # print(file.filename)
    if file.filename == '':
        return "No selected file"

    # check file size
    if request.content_length > MAX_CONTENT_LENGTH:
        return "File size exceeds the limit (16MB)."

    # check file extension
    if not allowed_file(file.filename):
        return "Not Allowed file extension"

    # get extension
    print(file.filename)
    extension = file.filename.split('.')[-1]

    print("Got It")
    if file:
        # upload path
        upload_folder = 'uploads'
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        # set file_id to uuid
        file_id = str(uuid.uuid1())
        file_path = os.path.join(upload_folder, file_id + "." + extension)
        print(file_path)
        file.save(file_path)
        boxes = detect_face(file_path)

        images_dir = crop_face(file_path, boxes)
        encoded_img = get_response_image(draw_rectangles(file_path, boxes), extension)
        return {
            "crop_images_dir": images_dir,
            "boxes": boxes.tolist(),
            "Image": encoded_img,
            "id": file_id
        }


@app.route('/change/<file_id>', methods=['POST'])
def change(file_id: str):
    try:
        # request에서 JSON 데이터 추출
        data = request.get_json()
        print(data)
        # 받은 데이터를 가공하거나 사용
        if data:
            message = data.get('message', 'No message provided')
            return jsonify({"success": True, "message": f"Received message: {message}"})
        else:
            return jsonify({"success": False, "error": "No JSON data received"})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


if __name__ == '__main__':
    app.run(debug=True)
