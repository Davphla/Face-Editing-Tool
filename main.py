
# https://github.com/timesler/facenet-pytorch

from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image, ImageDraw
from mosaic import apply_mosaic_section

# If required, create a face detection pipeline using MTCNN:
mtcnn = MTCNN(image_size=1024, margin=0)

# Create an inception resnet (in eval mode):
resnet = InceptionResnetV1(pretrained='vggface2').eval()


img = Image.open('./images/test_big.jpg')

# Convert the image to RGB if it's not already in that mode
if img.mode != 'RGB':
    img = img.convert('RGB')

# Get cropped and prewhitened image tensor
boxes, _ = mtcnn.detect(img)

# Create a copy of the original image to draw the boxes on
draw_img = img.copy()
draw = ImageDraw.Draw(draw_img)

# Define box color and thickness
box_color = 'green'
thickness = 2

# Draw the boxes
if boxes is not None:
    for box in boxes:
        # Instead of draw.rectangle, simply apply mosaic filter. 
        # box.toList() contains the coordinates of the box
        #draw.rectangle(box.tolist(), outline=box_color, width=thickness)
        box = box.tolist()
        print(box)
        draw_img = apply_mosaic_section(draw_img, int(box[0]), int(box[1]), int(box[2]), int(box[3]))
# Save and display the image
draw_img.save('./images/test_with_boxes.jpg')
draw_img.show()