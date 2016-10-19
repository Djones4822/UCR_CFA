import csv
import pandas as pd 
import numpy as np 

columns = ['Agency Name','Department','X','Address','Phone Number', 'Number of Officers', 'Population Served','Agency Type']
csv_file = 'disc_pol.csv'
police_dataDF = pd.read_csv(csv_file)
police_dataDF.columns = columns
police_dataDF = police_dataDF.drop('X',1)

"""
police_dataDF = police_dataDF.dropna(how='any')
police_dataDF.to_csv('disc_polcleaned.csv')
"""

print police_dataDF.head()
print police_dataDF.count()