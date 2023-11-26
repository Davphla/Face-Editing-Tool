import json

import numpy
from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw
from detect_face import *
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# set 16MB
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# allowed extension
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


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

    print("Got It")
    if file:
        # upload path
        upload_folder = 'uploads'
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        file_path = os.path.join(upload_folder, file.filename)
        # todo: change something like hash path
        file.save(file_path)
        img, boxes = detect_face(file_path)
        print(boxes)

        # img.filename = file_path
        _, images_dir = crop_face(file_path, boxes)

        encoded_img = get_response_image(file_path)
        return {
            "crop_images_dir": images_dir,
            "boxes": boxes.tolist(),
            "Image": encoded_img

        }
        # return send_file(file_path, as_attachment=True)
        # do mosaic or something func
        # mosaic_image_path = apply_mosaic(file_path)

        # 결과 파일을 클라이언트에게 전송
        # return send_file(mosaic_image_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
