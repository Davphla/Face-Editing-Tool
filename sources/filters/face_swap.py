from PIL import Image

def transpose_image(image):
    new_image = image.copy()
    for x in range(0, image.width):
        for y in range(0, image.height):
            r, g, b = image.getpixel((x, y))
            new_image.putpixel((y, x), (r, g, b))
    return new_image

def apply_face_transpose(image_path):
    image = Image.open(image_path)
    image = transpose_image(image)
    image.save(image_path)
    return image_path
