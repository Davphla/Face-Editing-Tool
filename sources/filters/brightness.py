from PIL import Image, ImageEnhance



def apply_brightness(image_path, brightness_factor):
    # Open the image file
    image = Image.open(image_path)

    for x in range(0, image.width):
        for y in range(0, image.height):
            r, g, b = image.getpixel((x, y))
            r = int(r * brightness_factor)
            g = int(g * brightness_factor)
            b = int(b * brightness_factor)
            image.putpixel((x, y), (r, g, b))

    # Save the brightened image
    image.save(image_path)

    return image_path
