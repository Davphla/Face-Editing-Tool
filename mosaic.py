from PIL import Image
from config import TILE_SIZE

def get_average_rgb(tile):
    tile = tile.resize((1, 1))
    return tile.getpixel((0, 0))

def get_tile_average_rgb(image, x, y, size):
    image = image.crop((x, y, x + size, y + size))
    return get_average_rgb(image)

def apply_tile_average(image, x, y, size):
    rgb = get_tile_average_rgb(image, x, y, size)
    image.paste(rgb, (x, y, x + size, y + size))
    return image

def apply_mosaic_effect(image):
    width, height = image.size
    for x in range(0, width, TILE_SIZE):
        for y in range(0, height, TILE_SIZE):
            apply_tile_average(image, x, y, TILE_SIZE)
    return image

def apply_mosaic_section(image, x1, y1, x2, y2):
    for x in range(x1, x2, TILE_SIZE):
        for y in range(y1, y2, TILE_SIZE):
            apply_tile_average(image, x, y, TILE_SIZE)
    print("done")
    return image
