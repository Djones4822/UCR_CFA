import Agency
from AgencyScraper import AgencyScraper
from AgencyDBWriter import AgencyDBWriter
from AgencyScreenWriter import AgencyScreenWriter
import requests
import STATES
from bs4 import BeautifulSoup
import pprint


class PoliceOneScraper(AgencyScraper):
    DOMAIN = 'http://www.policeone.com/law-enforcement-directory/page-{}/'
    ALL_PAGES_RANGE = range(1, 485)

    def scrape(self, page_range=None):
        if page_range is None:
            page_range = PoliceOneScraper.ALL_PAGES_RANGE
        for i in page_range:
            link = self.DOMAIN.format(i)

            req = requests.get(link)
            if req.status_code == requests.codes.ok:
                self.process_page(req.text)

    def process_page(self, page_text):
        soup = BeautifulSoup(page_text, 'html.parser')

        self.writer.write(soup.contents)
