from change_face import change_face
from detect_face import detect_face, crop_face, stitch
from config import IMAGES_DIR, TEST_IMAGE
from PIL import Image

test_image_path = IMAGES_DIR + TEST_IMAGE


def make_smile(image_path):
    
    # boxes is the list of coordinates for each face in the image
    boxes = detect_face(image_path)
    
    # create crops of each face, save them to /crop
    _, images_dir_crops = crop_face(image_path, boxes)
    
    # change the emotion of each face
    #for crop in images_dir_crops:
        #change_emotion(crop, 0) # Uses API credits, beware
    
    # Stitch the faces back into the original image
    final_image_dir = stitch(image_path, images_dir_crops, boxes)
    
    final_image = Image.open(final_image_dir)
    final_image.show()


if __name__ == "__main__":
    make_smile(test_image_path)