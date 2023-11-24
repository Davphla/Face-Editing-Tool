from change_face import change_face
from detect_face import detect_face, crop_face
from config import IMAGES_DIR, TEST_IMAGE

test_image_path = IMAGES_DIR + TEST_IMAGE

if __name__ == "__main__":
    
    img, boxes = detect_face(test_image_path)
    # img is the original image
    # boxes is the list of coordinates for each face in the image
    
    # create crops of each face
    crops = crop_face(img, boxes)
    
    # change the emotion of each face
    for crop in crops:
        change_face(crop, 0)
    
    # TODO: stitch the faces back into the original image
    # final_image = stich(img, crops)
    # final_image.show()
    
