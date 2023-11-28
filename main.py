import shutil

from change_face import change_emotion, change_emotion_fake
from detect_face import detect_face, crop_face, stitch, overwrite_image
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
    print(crops_dir)
    # change the emotion of each face
    for crop in crops_dir:
        # apply_mosaic(crop)
        # change_emotion(crop, "big_laugh") # Uses API credits, beware. Replaces image in place.
        change_emotion_fake(crop,
                            "big_laugh")  # Uses fake API. Paints text on face. Replaces image in place. (For testing purposes)

    # Stitch the faces back into the original image
    final_image_dir = stitch(image_path, crops_dir, boxes)

    # Delete crops
    for crop in crops_dir:
        os.remove(crop)

    final_image = Image.open(final_image_dir)
    final_image.show()


# def overwrite_image(infos: list, file_id: str):
#     crops_dir = []
#     boxes = []
#     file_id = file_id + ".png"
#     for x in infos:
#         # first make image path
#         # original image path is upload\file_id
#         crop_dir = f"crop\\{file_id}\\{file_id}_cropped_{x['number']}.png"
#         crops_dir.append(crop_dir)  # append all crops dir
#         number = x["number"]
#         boxes.append(x["box"])
#         change: str = x["change"]
#         if change == "mosaic":
#             apply_mosaic(f"upload\\{file_id}\\{number}.png")
#         else:
#             change_emotion_fake(crop_dir, change)
#     image_path = f"uploads\\{file_id}"
#     final_image_dir = stitch(image_path, crops_dir, boxes)
#     try:
#         # shutil.rmtree() 함수를 사용하여 디렉토리 및 하위 항목 삭제
#         shutil.rmtree(f"crop\\{file_id}")
#         print(f"디렉토리가 삭제되었습니다.")
#     except Exception as e:
#         print(f"디렉토리 삭제 중 오류가 발생했습니다: {e}")
#     # for crop in crops_dir:
#     #     os.remove(crop)
#
#     final_image = Image.open(final_image_dir)
#     final_image.show()


if __name__ == "__main__":
    # make_smile(test_image_path)
    # test_image_path
    # make_smile("images\\threefriends.png")
    infos = [
        {
            "number": 1,
            "box": [
                47.76042175292969,
                126.17083740234375,
                86.21199035644531,
                179.68475341796875
            ],
            "change": "big_laugh"
        }
    ]
    file_id = "096869a7-8dc7-11ee-be22-009337028547"
    overwrite_image(infos, file_id)
'''
infos form
[
{
"number": 1,
"box": [1,4 ,2, 8]
"change": "mosaic, big_laugh, pouting, sad ..."
},
{
"number": 4,
"box": [1, 5, 2, 8]
"change": "mosaic, big_laugh, pouting, sad ..."
}	
]
'''
