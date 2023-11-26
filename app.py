import json

import numpy
from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw
from detect_face import *
import os

app = Flask(__name__)
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


@app.route('/upload', methods=['POST'])
def upload():
    # upload type / multipart/form-data
    if 'image' not in request.files:
        return "No file part"

    file = request.files['image']

    if file.filename == '':
        return "No selected file"

    # check file size
    if request.content_length > MAX_CONTENT_LENGTH:
        return "File size exceeds the limit (16MB)."

    # check file extension
    if not allowed_file(file.filename):
        return "Not Allowed file extension"

    if file:
        # upload path
        upload_folder = 'uploads'
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        file_path = os.path.join(upload_folder, file.filename)

        # todo: change something like hash path
        file.save(file_path)
        img, boxes = detect_face(file_path)
        # crop_face(img, boxes)
        return {
            "boxes": json.dumps(boxes.tolist())
        }
        # return send_file(file_path, as_attachment=True)
        # do mosaic or something func
        # mosaic_image_path = apply_mosaic(file_path)

        # 결과 파일을 클라이언트에게 전송
        # return send_file(mosaic_image_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
