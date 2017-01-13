from AgencyScraper import AgencyScraper
import requests
import time
from bs4 import BeautifulSoup


class DiscoverPolicingScraper(AgencyScraper):
    DOMAIN = ("http://discoverpolicing.org/discover/index.cfm?fa=searchResult&"
              "city=&state=&zip=&radius=&agencyType=&entryEducation=&"
              "authorizedFTswornLow=&authorizedFTswornHigh=&populationLow=&"
              "populationHigh=&entryAgeMin=&entryAgeMax=&startingSalaryLow=&"
              "startingSalaryHigh=&startrow={}")
    ALL_ROWS_RANGE = range(1, 17432, 10)

    def scrape(self, start_row_range=None):
        if start_row_range is None:
            start_row_range = DiscoverPolicingScraper.ALL_ROWS_RANGE
        for i in start_row_range:
            link = self.DOMAIN.format(i)
            req = requests.get(link)
            if req.status_code == requests.codes.ok:
                self.process_page(req.text)
            time.sleep(DiscoverPolicingScraper.SLEEP_TIME)

    def process_page(self, page_text):
        soup = BeautifulSoup(page_text, 'html.parser')

        rows = soup.find(id='srchRslt').find('tbody').find_all('tr')

        agencies = []

        for row in rows:
            cols = row.find_all('td', id=lambda x: x != 'currentSearchPage')
            info = tuple(col.text.strip() for col in cols)

            if len(info) == 7:
                agency = {'name': info[0], 'address': info[2],
                          'phone_number': info[3], 'num_officers': info[4],
                          'pop_served': info[5], 'agency_type': info[6]}
                agencies.append(agency)
        self.writer.write(agencies)
