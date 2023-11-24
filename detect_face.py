# Importing necessary libraries
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image, ImageDraw
from mosaic import apply_mosaic_section
from config import BOX_COLOR, THICKNESS, IMAGES_DIR, TEST_IMAGE, CROP_DIR

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
    
    return img, boxes


def crop_face(img: Image, boxes):
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    crops = []
    if boxes is not None:
        for j, box in enumerate(boxes):
            box = [int(i) for i in box]
            cropped_img = img.crop(box)
            cropped_img_dir = CROP_DIR + TEST_IMAGE + f'_cropped_{j}.jpg'
            cropped_img.save(cropped_img_dir)
            crops.append(cropped_img_dir)
            
        
    return crops