import sys
import importlib
importlib.reload(sys)
import pytesseract
from PIL import Image


# image = Image.open('test.jpg')
image = Image.open('timg.jpg')
images = Image.open('times.jpg')
imagess = Image.open('tims.jpg')
import sys
import importlib
importlib.reload(sys)
text = pytesseract.image_to_string(image)
# texts = pytesseract.image_to_string(images)
textss = pytesseract.image_to_string(imagess)
print(text) 
print("--------------")
# print(texts)
# print("--------------")
print(textss)  