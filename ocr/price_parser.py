r"""
This class parse a string and returns amount in any format 2,33 or 2.22.
    - author: Siddiqui Noor
    - created: 10 May, 2019 1:45am
    - since: 1.0
"""
import re


class Price:
    def __init__(self, token):
        self.token = token
        self.ocr_arr = self.token.split("\n")
        self.ht = ["prix ht", "prix ht ei", "ht", "tarif h.t.", "total ht"]
        self.tva = ["tva", "eva", "t.v.a.", "total tua", "total tva"]
        self.total = ["prix ttc", "total", "total ttc", "montant", "hontant du", "amount", "tarif t.t.c"]


    #['Prix TTC euros : 10,10', 'Prix HT ers 8,42', 'TVA (20.00%) € : 1,68']
    def get_price(self, find_word):
        for line in self.ocr_arr:
            line = line.lower()
            found = None
            if any(word in line for word in find_word):
                try:
                    matched = re.search(r'[-+]?\b(?!\d+\s*(?:[,.]\d+)?%)\d+\s*(?:[.,]\d+)?', line)
                    # matched = re.search(r'[-+]?\b(?!\d+(?:[,.]\d+)?%)\d+(?:[.,]\d+)?', line)
                    if matched:
                        found = matched.group()
                    # print(found)
                    # found = re.search('([+-]?([0-9]*[,.])?[0-9]+)', line).group()
                    # found = re.search(r'\d+(?:,\d+)(?!%)', line).group()
                    # found = re.search(r'[-+]?\b(?!\d+(?:[,.]\d+)?%)\d+(?:[.,]\d+)?', line).group()
                except AttributeError:
                    # Not found in the original string
                    found = '0.00'  # apply your error handling

                return found

    def __del__(self):
        self.token = None


'''
data = """SIRET 552 115 891 00418\nTICKET A CONSERVER\n20180305713721741Z2066\nGare : VELIZY\nClasse: 1 km:0011\nnparyet>VELIZY — RUETIE\nCode tarif:O Tr:6453\nPrix HT ers 8,42\nTVA (20.00%) € : 1,68\nPrix TTC euros : 10,10\nPaiement CARTE BANCAIRE\nXxXXXXXxXXxXxXxx35E9 S\n713000356\n\nDate :05/03/2018 TZtai"""

price = Price(data)
print(price.find_line(price.tva))'''
