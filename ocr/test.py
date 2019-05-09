from PIL import Image
import pytesseract
im = Image.open("receipt/01.png")
text = pytesseract.image_to_string(im, lang="eng")
print(text)
