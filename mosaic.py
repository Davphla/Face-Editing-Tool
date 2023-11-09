from PIL import Image

IMAGE_TO_PROCESS = 'assets/car.jpg'
SAVE_DIRECTORY = 'results/'
TILE_SIZE = 20

img = Image.open(IMAGE_TO_PROCESS)


def get_average_rgb(tile):
    tile = tile.resize((1, 1))
    return tile.getpixel((0, 0))

def get_tile_average_rgb(image, x, y, size):
    image = image.crop((x, y, x + size, y + size))
    return get_average_rgb(image)

def apply_mosaic_effect(image):
    width, height = image.size
    for x in range(0, width, TILE_SIZE):
        for y in range(0, height, TILE_SIZE):
            rgb = get_tile_average_rgb(image, x, y, TILE_SIZE)
            image.paste(rgb, (x, y, x + TILE_SIZE, y + TILE_SIZE))
    return image

mosaic_image = apply_mosaic_effect(img)
mosaic_image.save(SAVE_DIRECTORY + 'mosaic.jpg')



