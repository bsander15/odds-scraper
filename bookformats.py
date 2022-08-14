import json
from logging import error

class Book:

    def __init__(self, book):
        try:
            f = open(f'{book}.json')
            self.xpaths = json.load(f)
        except:
            print('book not currently supported')
            

    def get_xpath(self,sport, type):
        try:
            if type != 'names':
                xpath = self.xpaths[sport]['market'].replace('MARKET',type)
            else:
                xpath = self.xpaths[sport][type]
            return xpath
        except:
            if not self.xpaths:
                error('use book child instance')
            else:
                error('sport not supported')
    





