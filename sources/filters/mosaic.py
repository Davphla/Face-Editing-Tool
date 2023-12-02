# Importing necessary library
from PIL import Image


# from config import TILE_SIZE

def apply_tile_average(image, x, y, size):
    tile = image.crop((x, y, x + size, y + size))
    tile = tile.resize((1, 1))
    rgb = tile.getpixel((0, 0))
    image.paste(rgb, (x, y, x + size, y + size))
    return image


def apply_mosaic_section(image, x1, y1, x2, y2):
    tile_size = 20
    for x in range(x1, x2 + tile_size, tile_size):
        for y in range(y1, y2 + tile_size, tile_size):
            apply_tile_average(image, x, y, tile_size)
    return image


def apply_mosaic(image_path):
    image = Image.open(image_path)
    apply_mosaic_section(image, 0, 0, image.width, image.height)
    image.save(image_path)
    return image_path
