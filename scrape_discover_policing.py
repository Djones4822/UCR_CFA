import time
from bs4 import BeautifulSoup
import requests
from STATES import STATES
import csv

class PoliceGatherer():
    DISCOVER_POLICING = 'http://discoverpolicing.org/discover/index.cfm?fa=searchResult&city=&state={}&zip=&radius=&agencyType=&entryEducation=&authorizedFTswornLow=&authorizedFTswornHigh=&populationLow=&populationHigh=&entryAgeMin=&entryAgeMax=&startingSalaryLow=&startingSalaryHigh=&startrow={}'
    STATES = STATES.keys()

    def __init__(self):
        self.disc_pol_dict = {}

    def get_disc_pol_rows(self, state, startrow):
        link = PoliceGatherer.DISCOVER_POLICING
        req = requests.get(link.format(state,startrow))
        if req.status_code == 200:
            html = req.text
        else:
            return None

        soup = BeautifulSoup(html,'html.parser')
        table = soup.find("table", {"id":"srchRslt"})
        tbody = table.find('tbody')
        rows = tbody.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            if len(cols) == 7:
                self.disc_pol_dict[state].append(cols)

    def gather_disc_pol(self):
        link = PoliceGatherer.DISCOVER_POLICING
        states = PoliceGatherer.STATES
        for state in states:
            print('Starting state: {}'.format(state))
            self.disc_pol_dict[state] = []

            req = requests.get(link.format(state,'0'))

            if req.status_code == 200:
                html = req.text
            else:
                continue

            soup = BeautifulSoup(html,'html.parser')
            all_ps = soup.find_all('p')
            last_row = 0
            for p in all_ps:
                if 'result(s)' in p.text:
                    last_row = p.text.split()[0]
            try:
                last_row = int(last_row)
            except:
                pass

            print('number of rows: {}'.format(last_row))

            cur_row = 1
            while cur_row < last_row:
                time.sleep(5)
                self.get_disc_pol_rows(state,cur_row)
                cur_row += 10
                #print("Next:{} through {}".format(cur_row, cur_row+10))
            if len(self.disc_pol_dict[state]) != last_row:
                print("{} Does not equal: {} recorded, {} listed".format(state,len(self.disc_pol_dict[state]),last_row))

            print('waiting...')
            time.sleep(45)
    def write_disc_pol(self):
        filename = 'disc_pol.csv'
        with open(filename, 'w') as f:
            writer = csv.writer(f)
            for state in PoliceGatherer.STATES:
                for row in self.disc_pol_dict[state]:
                    writer.writerow([state]+row)


if __name__ == '__main__':

    gatherer = PoliceGatherer()
    gatherer.gather_disc_pol()
    gatherer.write_disc_pol()