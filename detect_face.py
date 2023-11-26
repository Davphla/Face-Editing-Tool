# Importing necessary libraries
import io
import json
from base64 import encodebytes

from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image, ImageDraw
from mosaic import apply_mosaic_section
from config import BOX_COLOR, THICKNESS, IMAGES_DIR, TEST_IMAGE, CROP_DIR

import os

# Initialize MTCNN and InceptionResnetV1
mtcnn = MTCNN(image_size=1024, margin=0)
resnet = InceptionResnetV1(pretrained='vggface2').eval()


def detect_face(image_path):
    # Open the image file
    img = Image.open(image_path)

    # Convert the image to RGB if it's not already in that mode
    if img.mode != 'RGB':
        img = img.convert('RGB')

    # Detect faces in the image
    boxes, _ = mtcnn.detect(img)

    # To draw box on faces  
    # draw = ImageDraw.Draw(img)

    # Apply mosaic to detected faces
    if boxes is not None:
        for box in boxes:
            box = [int(i) for i in box]
            # img = apply_mosaic_section(img, box[0], box[1], box[2], box[3])
            # draw.rectangle(box, outline=BOX_COLOR, width=THICKNESS)

    # Save the processed image
    # output_path = IMAGES_DIR + TEST_IMAGE + '_result.jpg'
    # img.save(output_path)

    return boxes


def crop_face(image_path, boxes):
    # Open the image file
    img = Image.open(image_path)
    filename = img.filename.split(os.path.sep)[-1]
    extension = img.filename.split('.')[-1]
    if img.mode != 'RGB':
        img = img.convert('RGB')

    # =======
    # def crop_face(img_path, boxes):
    #     img = Image.open(img_path)
    #     if img.mode != 'RGB':
    #         img = img.convert('RGB')
    #     filename = os.path.basename(img_path)
    #     extension = os.path.splitext(img_path)[1][1:]
    # >>>>>>> a10b47a1a81ca8f1d4463c69093dc589b73422be
    crops = []
    images_dir = []
    if boxes is not None:
        for j, box in enumerate(boxes):
            cropped_img = img.crop(box)
            if not os.path.exists(f"crop/{filename}"):
                os.makedirs(f"crop/{filename}")
            cropped_img_dir = f"crop/{filename}/{filename}_cropped_{j}.{extension}"
            images_dir.append(cropped_img_dir)
            cropped_img.save(cropped_img_dir)
            crops.append(cropped_img_dir)

    # return crops coordinate and saved crop images_dir
    return crops, images_dir


def draw_rectangles(img: Image, rectangles, output_path):
    # 이미지 열기
    # img = Image.open(image_path)

    # ImageDraw 객체 생성
    draw = ImageDraw.Draw(img)

    # 각 좌표 쌍에 대해 네모 그리기
    for rectangle in rectangles:
        # rectangle은 [(x1, y1), (x2, y2)] 형태
        points = (rectangle[0:2], rectangle[2:4])
        draw.rectangle(points, outline="red", width=2)

    # 결과 이미지 저장
    img.save(output_path)


def get_response_image(image_path):
    pil_img = Image.open(image_path, mode='r')  # reads the PIL image
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='PNG')  # convert the PIL image to byte array
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii')  # encode as base64
    return encoded_img


def stitch_bad(orig_img, crops, boxes):
    orig_img = Image.open(orig_img)
    if orig_img.mode != 'RGB':
        orig_img = orig_img.convert('RGB')
    boxes = boxes.tolist()
    for i, box in enumerate(boxes):
        cropped_img = Image.open(crops[i])
        if cropped_img.mode != 'RGB':
            cropped_img = cropped_img.convert('RGB')
        orig_img.paste(cropped_img, box)
    orig_img.save("images/stitched.jpg")
    return "images/stitched.jpg"


def stitch(image_path, images_dir, boxes):
    orig_img = Image.open(image_path)
    for i, box in enumerate(boxes):
        cropped_img = Image.open(f"{images_dir}/crop_{i}.jpg")
        # Ensure the box values are integers
        box = tuple(int(b) for b in box)
        orig_img.paste(cropped_img, box)
    orig_img.save(f"{images_dir}/final.jpg")
    return f"{images_dir}/final.jpg"

# boxes = detect_face("uploads\Crowd-of-Diverse-People_800x528.jpg")
# print(orig_img)
# print(boxes)
# print(boxes)
# print(orig_img.filename)
# print(crop_face(orig_img, boxes))
