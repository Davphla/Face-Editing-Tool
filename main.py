import cv2
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image

# If required, create a face detection pipeline using MTCNN:
mtcnn = MTCNN(image_size=64, margin=0)

# Create an inception resnet (in eval mode):
resnet = InceptionResnetV1(pretrained='vggface2').eval()


img = Image.open('./images/test.jpg')

# Get cropped and prewhitened image tensor
img_cropped = mtcnn(img, save_path='./images/test_result.jpg')

# Calculate embedding (unsqueeze to add batch dimension)
img_embedding = resnet(img_cropped.unsqueeze(0))

# Or, if using for VGGFace2 classification
resnet.classify = True
img_probs = resnet(img_cropped.unsqueeze(0))