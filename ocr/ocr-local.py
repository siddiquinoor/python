import glob2
import cv2
import numpy as np
import pytesseract
import sys
from PIL import Image
from date_parser import DateParser
from price_parser import Price

param = sys.argv[1]
#golden_data = {"Date", "Amounts"}
#amounts = {"Total", "HT", "TVA"}

# Tesseract installation path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

# Path of working folder on Disk
src_path = "D:/Projects/python/ocr/receipt/"

def get_string(img_path):
    '''
    # Read image with opencv
    img = cv2.imread(img_path)

    # Convert to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply dilation and erosion to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)

    # Write image after removed noise
    cv2.imwrite(src_path + "removed_noise.png", img)


    #  Apply threshold to get image with only black and white
    #img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    ing = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 31, 2)
    # Write the image after apply opencv to do some ...
    cv2.imwrite(src_path + "final.png", img)
'''
    # Recognize text with tesseract for python
    result = pytesseract.image_to_string(Image.open(img_path), lang="fra")
    #result = pytesseract.image_to_string(Image.open(src_path + "removed_noise.png"), lang="fra")
    #result = pytesseract.image_to_string(Image.open(src_path + "final.png"), lang="fra")

    # Remove template file
    #os.remove(temp)

    return result


def get_date(ocr):
    date_parser = DateParser(ocr)
    found_date = date_parser.get_date()
    return found_date


def get_prices(ocr):
    price = Price(ocr)
    amounts = {"HT": price.get_price(price.ht), "TVA": price.get_price(price.tva), "Total": price.get_price(price.total)}
    return amounts


def test_bulk_image():
    # Path of working folder on Disk
    src_path = "./receipt/"
    images = glob2.glob("./receipt/*.*")

    print('--- Start recognize text from image ---')

    for image in images:
        print("Date for" + image)
        str = get_string(image)
        date = DateParser(str)
        date_found = date.get_date()
        print(date_found)
        print("--------------")

    #file = open(src_path + "01.png.txt", "w")
    #file.write(str)
    #file.close()

    print("------ Done -------")


str_orc = get_string(param)
'''
#tests = """SIRET 552 115 891 00418\nTICKET A CONSERVER\n20180305713721741Z2066\nGare : VELIZY\nClasse: 1 km:0011\nnparyet>VELIZY — RUETIE\nCode tarif:O Tr:6453\nPrix HT ers 8,42\nTVA (20.00%) € : 1,68\nPrix TTC euros : 10,10\nPaiement CARTE BANCAIRE\nXxXXXXXxXXxXxXxx35E9 S\n713000356\n\nDate :05/03/2018 TZtai"""
sentences = str_orc.split('\n')
lists = []
for item in sentences:
    lists.append(item)

print(item)
'''

golden_data = {"Date": get_date(str_orc), "Amounts": get_prices(str_orc)}
print(golden_data)
