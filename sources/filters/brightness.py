from PIL import Image, ImageEnhance

def apply_brightness(image_path, brightness_factor):
   # Open the image file
   image = Image.open(image_path)

   # Create a brightness enhancer
   enhancer = ImageEnhance.Brightness(image)

   # Enhance the brightness of the image
   brightened_image = enhancer.enhance(brightness_factor)

   # Save the brightened image
   brightened_image.save(image_path)

   return image_path
