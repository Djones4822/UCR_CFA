from STATES import STATES as state_dict
import csv, string, requests
from bs4 import BeautifulSoup
from pprint import pprint as pp
import pandas as pd 
#
#IMPLEMENT DATABASE WRITING
#
#

# Dictionary to be overwritten when scraping. Values not found will not change
police_dict = { "Country":"null", "Address 1":"null", "Address 2":"null", "City":"null", "State":"null", "Zip Code":"null", "County":"null", 
                "Phone #":"null", "Fax #":"null", "Department Website":"null", "Type":"null", "Population Served":"null", "Number of Officers":"null" }


class Scraper():
    DOMAIN = 'http://www.policeone.com/{}'
    SEARCH = 'law-enforcement-directory/{}-Agencies/page-{}/'

    def __init__(self):
        self.agencies = {state.replace(' ','-'): [] for state in state_dict.values()}
        self.search_next = True


    def get_page_links(self, state, number):
        search_link = Scraper.DOMAIN.format(Scraper.SEARCH.format(state,number))
        req = requests.get(search_link)
        if req.status_code != 200:
            return None
        #print(req.text)
        soup = BeautifulSoup(req.text, 'html.parser')

        # Check to see if the last page is the same new page
        head = soup.find('head')
        title = head.find('title').text
     
        if 'Page' in title:
            num = title.split()[-1]
            if num == number-1:
                self.search_next = False
                return 1

        links = []
        search_div = soup.find('div', {'id': 'search-results'})
        search_table = search_div
        search_rows = search_table.find_all('tr')[2:-2]   #first 2 are headers, last 2 are footers
        for row in search_rows[:-1]:
            cols = row.find_all('td')
            link = cols[0].find('a').attrs['href']
            links.append(link)

        return links



    def get_agency_details(self, given_link):
        return_info_dict = {}
        link = Scraper.DOMAIN.format(given_link)
        req = requests.get(link)
        if req.status_code != 200:
            return None

        soup = BeautifulSoup(req.text, 'html.parser')
        dep_name_div = soup.find('h1', {'class':'dep-head-text'})

        info = dep_name_div.text
        try: 
            name, local = info.split('-',1)
            police_dict['Name'] = name 
        except ValueError:
            print ("Skipped because of not enough or too many values to unpack")

        return_info_dict = police_dict # Make a copy since we only want to overwrite null values that this dept has info for.
        dep_info_div = soup.find_all('div', {'class':'dep-block-info'}) # should return 2 divs

        for div in dep_info_div:
            alltags = div.findAll(True)
            elements = []
            for tag in alltags:
                if tag.name == 'p':
                    elements.append(tag.text)        

            for elem in elements:
                field, data = elem.split(':',1)
                return_info_dict[field.strip()] = data.strip()

        df = pd.DataFrame(return_info_dict, index=[1]) # df to append to csv
        print (return_info_dict)               
        return df



    def run(self, write_on=False):
        for state in self.agencies.keys():
            i = 1
            self.search_next = True
            while self.search_next:
                links = self.get_page_links(state, i)
                if not links:
                    self.agencies[state].append('ERROR: PAGE {}'.format(i))
                if links == 1:
                    break
                to_write = []
                for link in links:
                    agency_detail = self.get_agency_details(link)
                    with open('policeone.csv', 'a') as csvfile:
                        try:
                            agency_detail.to_csv('policeone.csv', mode='a', header=False)
                        except AttributeError:
                            print("Returns a Nonetype Object")
            
                i += 1


scraper = Scraper()
scraper.run()
csvfile.close()
