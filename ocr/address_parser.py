r"""
This class parse a string and returns company title and address.
 - First it will get the title from the first line of the OCR text
 - Then get immidiate 2 lines after title for address
 - It will check the address is correct or not from online
 - If address is not correct then try to get SIRET (Ref: https://en.wikipedia.org/wiki/SIRET_code)
 - Hook into https://www.verif.com to get Title and Address of the company.
    - author: Siddiqui Noor
    - created: 21 May, 2019 10.46 pm
    - since: 1.0
"""
import re
import json


class AddressParser:
    def __init__(self, token):
        self.token = token  # token as ocr
        self.ocr_arr = self.token.split("\n")
        self.siret = ["siret", "no. siret"]

    def get_title(self):
        return self.ocr_arr[0]

    def get_address(self):
        return self.ocr_arr[1] + ", " + self.ocr_arr[2]

    def get_siret(self):
        """
        get only SIREX using [\d+\s]+ Ref: https://regex101.com/r/Jtk8cs/1/
        :return:
        """
        siret = ""
        for line in self.ocr_arr:
            line = line.lower()
            if any(word in line for word in self.siret):
                siret = line
        return siret

    def get_info(self):
        zip_code = ""
        address_one = ""
        title = ""
        siret = self.get_siret()
        for line in self.ocr_arr:
            line = line.lower()
            # print(line)
            try:
                # matched = re.search(r'(?:0[1-9]|[13-8][0-9]|2[ab1-9]|9[0-5])(?:[0-9]{3})?|9[78][1-9](?:[0-9]{2})?', line)  # matches french zip code https://stackoverflow.com/questions/43298661/french-regex-zipcode
                matched = re.search(r'^[0-9]{5}\s', line)  # matches french zip code with five digit and a space after
                if matched:
                    zip_code = line.replace('1', '7', 1)    # replace 1 with 7 like 18320 to 78320
                    break
                else:
                    title = address_one
                    address_one = line
            except AttributeError:
                # Not found in the original string
                zip_code = None  # apply your error handling

        if zip_code == "" and siret == "":  # When ZIP code not found TODO:: use SIRET to get title and address
            return json.dumps({'title': self.get_title(), 'address': self.get_address(), 'siret': siret})
        elif zip_code == "" and siret != "":
            return json.dumps({'title': self.get_title(), 'address': siret, 'siret': siret})
        else:
            return json.dumps({'title': title, 'address': address_one + ", " + zip_code, 'siret': siret})
        # return self.ocr_arr[1] + "\n" + self.ocr_arr[2]

    def __del__(self):
        self.token = None

