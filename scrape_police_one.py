from STATES import STATES as state_dict
import csv, string, requests
from bs4 import BeautifulSoup
from pprint import pprint as pp
#
#IMPLEMENT DATABASE WRITING
#
#

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
        #print(type(head))
        title = head.find('title').text
        #print(title)
        if 'Page' in title:
            num = title.split()[-1]
            if num == number-1:
                self.search_next = False
                return 1

        links = []
        search_div = soup.find('div', {'id': 'search-results'})
        print(type(search_div))
        search_table = search_div
        search_rows = search_table.find_all('tr')[2:-2]   #first 2 are headers, last 2 are footers
        for row in search_rows[:-1]:
            cols = row.find_all('td')
            link = cols[0].attrs['href']
            links.append(link)

        return links

    def get_agency_details(self, given_link):
        return_info_dict = {}
        link = Scraper.DOMAIN.format(given_link)
        req = requests.get(link)
        if req.status_code != 200:
            return None

        soup = BeautifulSoup(req.text, 'html.parser')

        pagecontent = soup.find('div', {'id':'page-content'})
        content = pagecontent.find('div', {'id':'content'})
        main_col = content.find('div',{'id':'main-col'})

        for child in main_col.children:

            classtext = child.attr.get_attr('class')   #Should return 2 divs

            if classtext == 'dep-head-text':           #Get the name of the agency
                info = child.text
                name, local = info.split('-')
                return_info_dict['Name'] = name
            elif classtext == 'dept_info':
                div_info = child.find_all('div', {'class':'dep-block-info'})
                for div in div_info:
                    elements = div.find_all('p')
                    for elem in elements:
                        field, data = elem.split(':')
                        return_info_dict[field.strip()] = data.strip()
        return return_info_dict

    def write(self, write_list):
        with open('policeone.csv', 'w') as csvfile:
            csvwriter = csv.writer()


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
                    self.agencies[state].append(agency_detail)
                    if write_on:
                        to_write.append(agency_detail)
                        pp(agency_detail)
                if to_write:
                    #self.write(to_write)
                    pass

                i += 1

scraper = Scraper()
scraper.run()