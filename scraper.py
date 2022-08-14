from optparse import Option
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bookformats import Book
import argparse
from bs4 import BeautifulSoup
import pandas as pd

class OddsScraper:

    def __init__(self,book):
        options = Options()
        options.headless = True
        options.add_argument('--window-size=1920,1200')

        self.driver = webdriver.Chrome(options=options, service=Service("./chromedriver"))
        self.book = Book(book)
    
    def scrape_odds(self, url, sport, market):
        self.driver.get(url)
        print(f'Title: {self.driver.title}')
        print(f'URL: {self.driver.current_url}')
        print(type(self.book.get_xpath(sport,market)))
        outright_element = self.driver.find_element("xpath",self.book.get_xpath(sport,market))
        odds_element = outright_element.find_element("xpath", "..").text
        names_element = self.driver.find_element("xpath", self.book.get_xpath(sport,'names')).text
        odds = odds_element.split('\n')
        odds.pop(0)
        names = names_element.split('\n')
        selections = []
        for (name, odd) in zip (names, odds):
            if odd != market:
                selections.append({"Golfer": name, "Odds": odd})
        return selections
    
    def quit(self):
        self.driver.quit()

def main():
    parser = argparse.ArgumentParser(description="CLI commands for odds scraper",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-u', '--url', help="URL of wagers")
    parser.add_argument('-m', '--market', help='wager market')
    parser.add_argument('-s','--sport', help="sport of wagers")
    parser.add_argument('-b', '--book', help='sportsbook')
    args = vars(parser.parse_args())
    print(args)

    scraper = OddsScraper(args['book'])
    # print(scraper.book.xpaths)
    print(scraper.scrape_odds(args['url'],args['sport'],args['market']))

if __name__ == "__main__":
    main()

