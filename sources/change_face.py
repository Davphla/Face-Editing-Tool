import requests
import os
import base64
import json
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv
from config import IMAGES_DIR, TEST_IMAGE

load_dotenv()
api_key = os.getenv('AILAB_API_KEY')

#image_path = IMAGES_DIR + TEST_IMAGE
#output_path = IMAGES_DIR + TEST_IMAGE + '_emoted.jpg'


def base64_to_image(image_data):
    image_bytes = base64.b64decode(image_data)
    return Image.open(BytesIO(image_bytes))
    
    
def change_emotion(image_path, emotion = "big_laugh"):
    
    emotion_codes = {
        "big_laugh": 0,
        "pouting": 1,
        "sad": 2,
        "smile": 3,
        "open_eyes": 100
    }
    
    # Check if the provided emotion name is valid
    if emotion not in emotion_codes:
        print(f"Invalid emotion name: {emotion}. Please choose from {list(emotion_codes.keys())}.")
        return
    
    url = "https://www.ailabapi.com/api/portrait/effects/emotion-editor"
    payload = {'service_choice': f'{emotion_codes[emotion]}'}
    files = [
        ('image_target', ('file', open(image_path, 'rb'), 'application/octet-stream'))
    ]
    headers = {
        'ailabapi-api-key': api_key
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    # Check the status code of the response
    if response.status_code != 200:
        print(f"Request failed with status {response.status_code}")
        return

    # Print the entire response
    # print(response.text)

    try:
        image_data = json.loads(response.text)['data']['image']
    except KeyError:
        print("Key 'data' not found in the response")
        return

    image = base64_to_image(image_data)

    image.save(image_path)


def change_emotion_fake(image_path, emotion = "big_laugh"):
    
    emotion_codes = {
        "big_laugh": 0,
        "pouting": 1,
        "sad": 2,
        "smile": 3,
        "open_eyes": 100
    }
    
    # Check if the provided emotion name is valid
    if emotion not in emotion_codes:
        print(f"Invalid emotion name: {emotion}. Please choose from {list(emotion_codes.keys())}.")
        return
    
    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", 75)
    draw.text((0, 0), emotion, (255, 255, 255), font=font)
    
    img.save(image_path)
