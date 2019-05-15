import re

my_list = ['Prix TTC euros : 10,10', 'Prix HT euros 8,42', 'TVA (20.00%) euros : 1,68']

for item in my_list:
    found = re.search(
        r'([+-]?(?:[0-9]*[,.])?[0-9]+)(?!(?:%|(?:[+-]?(?:[0-9]*[,.])?[0-9]+)))',
        item
    ).group()
    print(found)
