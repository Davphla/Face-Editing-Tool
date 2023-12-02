from PIL import Image
import numpy as np

def apply_blur_old(image_path):
    image = Image.open(image_path)
    img_array = np.array(image)
    
    blurred = np.copy(img_array)
    
    # For each pixel (excluding the borders), calculate the average color of its neighbors
    for i in range(1, img_array.shape[0] - 1):
        for j in range(1, img_array.shape[1] - 1):
            avg_color = img_array[i-1:i+2, j-1:j+2].mean(axis=(0, 1))
            blurred[i, j] = avg_color

    # Convert the NumPy array back to a PIL Image
    blurred = blurred.astype('uint8')
    blurred_image = Image.fromarray(blurred)

    blurred_image.save(image_path)
    return image_path

def apply_blur(image_path):
    image = Image.open(image_path)
    img_array = np.array(image)
    
    blurred = np.copy(img_array)
    
    # Define the kernel size (must be an odd number)
    # Kernel size should be proportional to the size of the image
    k = int(img_array.shape[0] / 10)
    if k%2 == 0:
        k += 1
    offset = k // 2

    # For each pixel (excluding the borders), calculate the average color of its neighbors
    for i in range(offset, img_array.shape[0] - offset):
        for j in range(offset, img_array.shape[1] - offset):
            avg_color = img_array[i-offset:i+offset+1, j-offset:j+offset+1].mean(axis=(0, 1))
            blurred[i, j] = avg_color

    # Convert the NumPy array back to a PIL Image
    blurred = blurred.astype('uint8')
    blurred_image = Image.fromarray(blurred)

    blurred_image.save(image_path)
    return image_path