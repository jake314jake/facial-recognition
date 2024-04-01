import cv2
import numpy as np

def remove_background(image_path, output_path, threshold=200):
    """
    Remove the background from an image using thresholding.
    
    Parameters:
    - image_path: str, path to the input image.
    - output_path: str, path where the result image will be saved.
    - threshold: int, threshold value used for binary thresholding. Defaults to 200.
    """
    
    image = cv2.imread(image_path)

    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

   
    _, mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)

   
    mask = 255 - mask

  
    kernel = np.ones((5,5),np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

  
    result = cv2.bitwise_and(image, image, mask=mask)

   
    cv2.imwrite(output_path, result)
    


image_path = "/content/baha.jpg"  
output_path = "baha_without_background.jpg" 

remove_background(image_path, output_path, threshold=200)
