import requests
import os
import base64
import json
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv
from config import IMAGES_DIR, TEST_IMAGE

load_dotenv()
api_key = os.getenv('AILAB_API_KEY')
# For you guys to test, the API key is: '9rpKeyTLQIdVNc3foJk6TvHhFhBbw2UaPPgWizixwjZ5SZgauKtdHrq4mCl8eAcl'
# I have 160 free credits left, and each API call costs 8 credits. Just keep that in mind hahaha
# After those are over, we can buy 2000 credits for 12 dollars,
# which should be good enough for the class, when we present our work.

image_path = IMAGES_DIR + TEST_IMAGE
output_path = IMAGES_DIR + TEST_IMAGE + '_result.jpg'


def base64_to_image(image_data):
    image_bytes = base64.b64decode(image_data)
    return Image.open(BytesIO(image_bytes))
    
    
def make_smile(image_path):
    
    url = "https://www.ailabapi.com/api/portrait/effects/emotion-editor"
    payload = {'service_choice': '0'}
    files = [
    ('image_target', ('file', open(image_path, 'rb'), 'application/octet-stream'))
    ]
    headers = {
    'ailabapi-api-key': api_key
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    image_data = json.loads(response.text)['data']['image']

    image = base64_to_image(image_data)
    
    image.save(output_path)
    image.show()

make_smile(image_path)
