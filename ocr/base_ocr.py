import io
import sys
import json
from PIL import Image
import base64
import pytesseract
from date_parser import DateParser
from price_parser import Price
from datetime import datetime

try:
    param = sys.argv[1]
except IndexError:
    param = None
src_path = "/python/"


def read_tesseract(img_string=None, ln="fra"):
    """This function usage Tesseract to read image and returs OCR data
    :param the_path: as the actual path of the image
    :param ln: as language of the image i.e. 'eng', 'fra' etc default is 'fra'
    :return: pecial string as OCR data
    """
    imgstring = img_string.split('base64,')[-1].strip()

    pic = io.StringIO()

    image_string = io.BytesIO(base64.b64decode(imgstring))
    image = Image.open(image_string)

    # Overlay on white background, see http://stackoverflow.com/a/7911663/1703216
    # bg = Image.new("RGB", image.size, (255,255,255))
    # bg.paste(image,image)

    # Save the image passed to pytesseract for debugging purposes
    image.save('pic.png')

    # Recognize text with tesseract for python
    try:
        result = pytesseract.image_to_string(image, lang=ln)
    except FileNotFoundError:
        result = None
    return result


def get_date(ocr):
    """Using DateParser this function process given OCR data and returns date
    :param ocr: as eated OCR data from an image
    :return: date
    :raise: need to handle if passing data is empty
    """
    date_parser = DateParser(ocr)
    found_date = date_parser.get_date()
    if found_date is None:
        return datetime.now().strftime('%d-%m-%Y')
    else:
        return found_date


def get_prices(ocr):
    """This function gets eaten OCR data and find Total, TVA, HT then return an object
    :param ocr: eaten OCR data from an image
    :return: object as HT, TVA, Total
    :raise: need to handle empty OCR data
    """
    price = Price(ocr)
    amounts = {"HT": price.get_price(price.ht), "TVA": price.get_price(price.tva), "Total": price.get_price(price.total)}
    return amounts


def get_string(img_string):
    # return read_cv(img_path)
    return read_tesseract(img_string)  # This works for maximum effected result


def get_data(debug=0):
    # str_ocr = get_string(img_string)
    str_ocr = get_string('data: image/png;base64,'+param)
    if str_ocr is not None:
        if debug:
            print(str_ocr)
        # write_file(str_ocr)
        golden_data = {'date': get_date(str_ocr), 'amounts': get_prices(str_ocr)}
        json_data = json.dumps(golden_data)
    else:
        json_data = json.dumps({'error': True, 'message': 'File not found'})

    print(json_data)


# get_data()
print('ok')
# ocr = read_tesseract()
# print(ocr)
