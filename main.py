from change_face import change_emotion, change_emotion_fake
from detect_face import detect_face, crop_face, stitch
from mosaic import apply_mosaic
from config import IMAGES_DIR, TEST_IMAGE
from PIL import Image
import os

test_image_path = IMAGES_DIR + TEST_IMAGE


def make_smile(image_path):
    
    # boxes is the list of coordinates for each face in the image
    boxes = detect_face(image_path)
    
    # create crops of each face, save them to /crop
    crops_dir = crop_face(image_path, boxes)
    
    # change the emotion of each face
    for crop in crops_dir:
        #apply_mosaic(crop)
        #change_emotion(crop, "big_laugh") # Uses API credits, beware. Replaces image in place.
        change_emotion_fake(crop, "big_laugh") # Uses fake API. Paints text on face. Replaces image in place. (For testing purposes)
    
    # Stitch the faces back into the original image
    final_image_dir = stitch(image_path, crops_dir, boxes)
    
    # Delete crops
    for crop in crops_dir:
        os.remove(crop)
    
    final_image = Image.open(final_image_dir)
    final_image.show()


if __name__ == "__main__":
    make_smile(test_image_path)