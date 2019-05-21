r"""
This class parse a string and return any types of date.
    - author: Siddiqui Noor
    - created: 9 May, 2019 1:01am
    - since: 1.0
    - ref: https://stackoverflow.com/questions/33145399/python-regex-to-handle-different-types-of-dates
"""
from itertools import tee
from datetime import datetime
import re


class DateParser:

    def __init__(self, token):
        self.token = token
        self.valid_from = datetime(2018, 1, 1)
        self.valid_to = datetime(2030, 1, 1)
        self.default_year = 2019

        self.dt_formats = [
            ['%d', '%m', '%Y'],
            ['%d', '%m', '%y'],
            ['%m', '%d', '%y'],
            ['%d', '%b', '%Y'],
            ['%d', '%B', '%Y'],
            ['%d', '%b'],
            ['%d', '%B'],
            ['%b', '%d'],
            ['%B', '%d'],
            ['%b', '%Y'],
            ['%B', '%Y'],
        ]

    def get_date(self):
        t1, t2, t3 = tee(re.findall(r'\b\w+\b', self.token), 3)
        next(t2, None)
        next(t3, None)
        next(t3, None)
        triples = zip(t1, t2, t3)

        for triple in triples:
            for dt_format in self.dt_formats:
                try:
                    dt = datetime.strptime(' '.join(triple[:len(dt_format)]), ' '.join(dt_format))

                    if '%y' not in dt_format and '%Y' not in dt_format:
                        dt = dt.replace(year=self.default_year)

                    if self.valid_from <= dt <= self.valid_to:
                        return dt.strftime('%d-%m-%Y')

                        for skip in range(1, len(dt_format)):
                            next(triples)
                    break

                except ValueError:
                    pass

    def __del__(self):
        self.token = None
