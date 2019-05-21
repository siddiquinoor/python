r"""
This file is the core of OCR related all functionality. It usages different custom made classes to process a file.
    - author: Siddiqui Noor
    - created: 15 May, 2019 11:59pm
    - edited: 21 May, 3:45am
    - since: 1.0
"""
import glob2
import cv2
import numpy as np
import pytesseract
import sys
import json
from PIL import Image
from date_parser import DateParser
from price_parser import Price
from address_parser import AddressParser
from datetime import datetime

# Tesseract installation path for Windows only
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

json_data = json.dumps({'error': True, 'code': 1000, 'message': 'Parameter missing!'})
# print(sys.argv[2])


class OCR:
    def __init__(self):
        try:
            self.file = sys.argv[1]  # Must pass as a argument of an actual file with the script call
            self.src_path = "/python/"  # This path is to write converted image into
            # self.src_path = "D:/Projects/python/ocr/receipt/"  # Windows only
        except IndexError:
            self.file = None
            self.json_data = json.dumps({'error': True, 'code': 1001, 'message': 'Parameter missing!'})
            raise ValueError(self.json_data)
        try:
            self.debug = sys.argv[2]  # Second parameter ensures debug mode
        except IndexError:
            self.debug = None

    def __del__(self):
        self.json_data = None
        self.file = None
        self.src_path = None

    def test_bulk_image(self, path):
        """This function reads all images in a given directory, read OCR Data and returns expected value
        :param path: Directory path which contain images
        :return: expected value like date, total, ht, tva etc.
        :raise: need to handle except"""
        images = glob2.glob(path + "/*.*")

        print('--- Start recognize text from image ---')

        for image in images:
            print("Date for" + image)
            str = self.get_string(image)
            date = DateParser(str)
            date_found = date.get_date()
            print(date_found)
            print("--------------")

        print("------ Done -------")

    def test(self):
        """This function is for testing eaten OCR data to get expected value from
        :return: expected value
        """
        tests = """A\
    COFIROUTE “4p

    SIRET 552 115 891 00418

    TICKET A CONSERVER
    201803057137217412066

    Gare : VELIZY
    Classe: 1 km:0011
    Trajet:VELIZY - RUEIL
    Code tarif:0 Tr :6453
    Prix HT ei: 8 ,42
    EVA F20,:00%) € : 1,68
    Prix TTC euros : 10,10
    Paiement CARTE BANCAIRE
    XXXXXXXXXXXX 3569 S
    7113000356

    Date :05/03/2018 17:41"""
        # sentences = tests.split('\n')
        # lists = []
        # for item in sentences:
        #     lists.append(item)
        # print(lists)
        golden_data = {'error': False, 'code': 200, "Date": self.get_date(tests), "Amounts": self.get_prices(tests)}
        print(golden_data)

    def remove_noise(self, img_path):
        """This function gets an image path then remove noises and returns a new image path
        :param img_path: actual path of the image
        :return: returns a new image path
        :raise: need to handle error if file not found
        """
        # Read image with opencv
        img = cv2.imread(img_path)
        file_name = "no_noise.png"
        # Apply dilation and erosion to remove some noise
        kernel = np.ones((1, 1), np.uint8)
        img = cv2.dilate(img, kernel, iterations=1)
        img = cv2.erode(img, kernel, iterations=1)

        # Write image after removed noise
        cv2.imwrite(self.src_path + file_name, img)
        return self.src_path + file_name

    def black_and_white(self, img_path):
        """This function gets an image path then make it black and white and returns a new image path
        :param img_path: as actual path of the image
        :return: a new image path
        :raise: need to handle error if file not found
        """
        # Read image with opencv
        img = cv2.imread(img_path)
        file_name = "bAw.png"
        # Apply threshold to get image with only black and white
        # img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
        img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 31, 2)
        # Write the image after apply opencv to do some ...
        cv2.imwrite(self.src_path + file_name, img)
        return self.src_path + file_name

    # noinspection PyMethodMayBeStatic
    def get_date(self, ocr):
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

    # noinspection PyMethodMayBeStatic
    def get_prices(self, ocr):
        """This function gets eaten OCR data and find Total, TVA, HT then return an object
        :param ocr: eaten OCR data from an image
        :return: object as HT, TVA, Total
        :raise: need to handle empty OCR data
        """
        price = Price(ocr)
        amounts = {"HT": price.get_price(price.ht), "TVA": price.get_price(price.tva),
                   "Total": price.get_price(price.total)}
        return amounts

    def get_title(self, ocr):
        """Using AddressParser this function process given OCR data and returns title
        :param ocr: as eaten OCR data from an image
        :return: title
        :raise: need to handle if passing data is empty
        """
        title = AddressParser(ocr)
        return title.get_title()

    def get_address(self, ocr):
        """Using AddressParser this function process given OCR data and returns address
        :param ocr: as eaten OCR data from an image
        :return: address
        :raise: need to handle if passing data is empty
        """
        address = AddressParser(ocr)
        return address.get_info()

    # noinspection PyMethodMayBeStatic
    def write_file(self, ocr):
        """This function writes OCR data into a file
        :param ocr: as string
        :return: nothing but writes into file
        :raise: file processing exception
        """
        file = open(self.src_path + "01.blah_blah.txt", "w")
        file.write(ocr)
        file.close()

    # noinspection PyMethodMayBeStatic
    def convert_to_gray(self, img_path):
        """This function gets an image path then make it gray and returns the new image path
        :param img_path: as actual path of the image
        :return: a new image path
        :raise: need to handle error if file not found
        """
        # Read image with opencv
        img = cv2.imread(img_path)
        file_name = "gray.png"
        # Convert to gray
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(self.src_path + file_name, img)
        return self.src_path + file_name

    # noinspection PyMethodMayBeStatic
    def read_cv(self, the_path, ln="fra"):
        """This function usage OpenCV2 to read images in various format and returns eaten OCR data
        :param the_path: as the actual path of the image
        :param ln: as language of the image i.e. 'eng', 'fra' etc default is 'fra'
        :return: special string as OCR data
        """
        img_path = self.convert_to_gray(the_path)
        # img_path = remove_noise(path) # Same result as gray
        # img_path = black_and_white(the_path) # not working
        result = pytesseract.image_to_string(Image.open(img_path), lang=ln)
        return result

    # noinspection PyMethodMayBeStatic
    def read_tesseract(self, the_path, ln="fra"):
        """This function usage Tesseract to read image and returs OCR data
        :param the_path: as the actual path of the image
        :param ln: as language of the image i.e. 'eng', 'fra' etc default is 'fra'
        :return: pecial string as OCR data
        """
        # Recognize text with tesseract for python
        # print("The path: " + the_path)
        try:
            result = pytesseract.image_to_string(Image.open(the_path), lang=ln, config='--psm 6')
            data = json.dumps({'error': False, 'code': 200,  'ocr': result})
        except FileNotFoundError:
            data = json.dumps({'error': True, 'code': 1002,  'message': 'File Not found!'})  # TODO:: Can pass json data then need to check error = False in get_data
        except AttributeError:
            data = json.dumps({'error': True, 'code': 1003, 'message': 'Invalid file can not be read!'})
        # in all cases return data
        return data

    def get_string(self, img_path):
        # return read_cv(img_path)
        return self.read_tesseract(img_path)  # This works for maximum effected result

    # noinspection PyMethodMayBeStatic
    def get_data(self):
        str_ocr = self.get_string(self.file)
        data = json.loads(str_ocr)
        if data['error']:
            self.json_data = json.dumps({'error': True, 'code': data['code'], 'message': data['message']})
        else:
            if data['ocr'] is not None:
                if self.debug is not None:
                    # print("The debug: " + data['ocr'])
                    self.json_data = json.dumps({'error': False, 'code': 200,  'message': data['ocr']})
                    self.write_file(data['ocr'])
                else:
                    addresses = json.loads(self.get_address(data['ocr']))
                    golden_data = {'error': False, 'code': 200, 'title': addresses['title'], 'address': addresses['address'], 'siret': addresses['siret'], 'date': self.get_date(data['ocr']), 'amounts': self.get_prices(data['ocr']), 'ocr': data['ocr']}
                    self.json_data = json.dumps(golden_data)
            else:
                self.json_data = json.dumps({'error': True, 'code': 1005,  'message': 'Failed to process OCR!'})
        # in all cases return the JSON data
        return self.json_data


try:
    ocr = OCR()
except ValueError:
    print(json_data)
else:
    j_data = ocr.get_data()
    print(j_data)
    # test()
