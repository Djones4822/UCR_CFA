'''
This scraper is for this website: https://www.searchquarry.com/police-and-sheriff-department-finder/
'''

import requests
import csv
from bs4 import BeautifulSoup

url = 'https://www.searchquarry.com/police-and-sheriff-department-finder/'
resp = requests.get(url).text

soup = BeautifulSoup(resp)
states = soup.find(id='stateList').findAll('li')

headers = ['state', 'department_name', 'address', 'phone', 'site']
master = []

for s in states:
    state_name = s.find('a').text.title()
    link = s.find('a')['href']

    print('Currently on', state_name)
    state_page = BeautifulSoup(requests.get(link).text)

    table = state_page.select('.datagrid > table')
    rows = table[0].findAll('tr')[1:]

    for row in rows:
        cells = [c.text.strip() for c in row.findAll('td')]
        cells.insert(0, state_name)
        master.append(cells)

with open('output.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(master)
