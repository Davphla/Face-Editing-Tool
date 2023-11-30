from PIL import Image
import numpy as np

def blur(image_path):
    image = Image.open(image_path)
    img_array = np.array(image)
    
    blurred = np.copy(img_array)
    
    # For each pixel (excluding the borders), calculate the average color of its neighbors
    for i in range(1, img_array.shape[0] - 1):
        for j in range(1, img_array.shape[1] - 1):
            avg_color = img_array[i-1:i+2, j-1:j+2].mean(axis=(0, 1))
            blurred[i, j] = avg_color
    
    # Convert the NumPy array back to a PIL Image
    blurred_image = Image.fromarray(blurred)

    blurred_image.save(image_path)
    return image_path