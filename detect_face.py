# Importing necessary libraries
import io
import json
import shutil
from base64 import encodebytes

from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image, ImageDraw

from change_face import change_emotion_fake
from mosaic import apply_mosaic_section, apply_mosaic
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


def crop_face(file_path, boxes):
    print(file_path)
    # Open the image file
    img = Image.open(file_path)
    filename = img.filename.split(os.path.sep)[-1]
    print(filename)
    extension = img.filename.split('.')[-1]
    if img.mode != 'RGB':
        img = img.convert('RGB')

    crops = []
    if boxes is not None:
        for j, box in enumerate(boxes):
            cropped_img = img.crop(box)
            if not os.path.exists(f"crop/{filename}"):
                os.makedirs(f"crop/{filename}")
            cropped_img_dir = f"crop/{filename}/{filename}_cropped_{j}.{extension}"
            cropped_img.save(cropped_img_dir)
            crops.append(cropped_img_dir)

    # return crops coordinate and saved crop image_dir
    return crops


# draw
def draw_rectangles(image_path, rectangles) -> Image:
    # 이미지 열기
    img = Image.open(image_path)

    # ImageDraw 객체 생성
    draw = ImageDraw.Draw(img)
    rectangles = rectangles.tolist()
    # draw rectangle
    for i, rectangle in enumerate(rectangles):
        # # points [(x1, y1), (x2, y2)] 형태
        # points = [(rectangle[0:2]), (rectangle[2:4])]
        # print(points)
        draw.rectangle(rectangle, outline="red", width=2)

    # save result
    return img


def get_response_image(img: Image, extension):
    # pil_img = Image.open(image_path, mode='r')  # reads the PIL image

    byte_arr = io.BytesIO()
    img.save(byte_arr, format=f'{extension}')  # convert the PIL image to byte array, PNG, JPG
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii')  # encode as base64
    return encoded_img


def stitch(image_path, crops_dir, boxes):
    orig_img = Image.open(image_path)
    for i, box in enumerate(boxes):
        cropped_img = Image.open(crops_dir[i])
        # Ensure the box values are integers
        box = tuple(int(j) for j in box)
        # Resize the cropped image to match the box dimensions
        if cropped_img.size != (box[2] - box[0], box[3] - box[1]):
            cropped_img = cropped_img.resize((box[2] - box[0], box[3] - box[1]))
        orig_img.paste(cropped_img, box)
    if orig_img.mode != 'RGB':
        orig_img = orig_img.convert('RGB')
    orig_img.save(f"{IMAGES_DIR}/final.jpg")
    return f"{IMAGES_DIR}/final.jpg"


def overwrite_image(infos: list, file_id: str):
    crops_dir = []
    boxes = []
    file_id = file_id + ".png"
    for x in infos:
        # first make image path
        # original image path is upload\file_id
        crop_dir = f"crop\\{file_id}\\{file_id}_cropped_{x['number']}.png"
        crops_dir.append(crop_dir)  # append all crops dir
        number = x["number"]
        boxes.append(x["box"])
        change: str = x["change"]
        if change == "mosaic":
            apply_mosaic(f"uploads\\{file_id}")
        else:
            change_emotion_fake(crop_dir, change)
    image_path = f"uploads\\{file_id}"
    final_image_dir = stitch(image_path, crops_dir, boxes)
    try:
        # shutil.rmtree() 함수를 사용하여 디렉토리 및 하위 항목 삭제
        shutil.rmtree(f"crop\\{file_id}")
        print(f"디렉토리가 삭제되었습니다.")
    except Exception as e:
        print(f"디렉토리 삭제 중 오류가 발생했습니다: {e}")
    # for crop in crops_dir:
    #     os.remove(crop)

    final_image = Image.open(final_image_dir)
    final_image.show()
    return {"change": get_response_image(final_image, "png")}

# boxes = detect_face("uploads\Crowd-of-Diverse-People_800x528.jpg")
# img = Image.open("uploads\Crowd-of-Diverse-People_800x528.jpg")
# draw_rectangles(img, boxes).show()

# print(orig_img)
# print(boxes)
# print(boxes)
# print(orig_img.filename)
# print(crop_face(orig_img, boxes))
