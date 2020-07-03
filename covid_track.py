import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import (DAILY, DateFormatter,
                              rrulewrapper, DayLocator,RRuleLocator, drange)
import requests
import time
import os
import datetime

my_region = "West Sussex"
how_far = 30




cases_csv  = "cases.csv"
# deaths_csv = "deaths.csv"
here = os.path.isfile(cases_csv) # and os.path.isfile(deaths_csv)
uptodate = False

if here:
    print ("Checking the file timestamp...")
    time_cases  = os.path.getmtime(cases_csv)
    # time_deaths = os.path.getmtime(deaths_csv)
    today = time.time()
    
    uptodate = abs(time_cases-today)<12*3600 # and abs(time_deaths-today)<12*3600
else:
    print ("Data files aren't here")

if (not uptodate or not here):
    print ("Refreshing the csvs")
    url_cases = "https://coronavirus.data.gov.uk/downloads/csv/coronavirus-cases_latest.csv"
    # url_deaths = "https://coronavirus.data.gov.uk/downloads/csv/coronavirus-deaths_latest.csv"

    raw_cases  = requests.get(url_cases)
    # raw_deaths = requests.get(url_deaths)

    cases_file = open(cases_csv,"w")
    cases_file.write(raw_cases.text)
    cases_file.close()

    # deaths_file = open(deaths_csv, "w")
    # deaths_file.write(raw_deaths.text)
    # deaths_file.close()
else:
    print("Files are up to date!")

cases  = pd.read_csv(cases_csv)
# deaths = pd.read_csv(deaths_csv)

today = datetime.date.today()


region_cases  = cases .loc[lambda cases : cases ['Area name'] == my_region, :]

if (region_cases.shape[0] == 0):
    print (my_region, "wasn't found in the file")
    whatever=dict()
    
    for _, row in cases.iterrows():
        whatever[row['Area name']] = 1

    print ("available regions:")
    for key in sorted(whatever.keys()):
        print (" - "+key)
    exit()
    
# region_deaths = deaths.loc[lambda deaths: deaths['Area name'] == my_region, :]


cases_array  = [None]*how_far
datec_array  = [None]*how_far

for index, row in region_cases.iterrows():
    date = datetime.datetime.strptime(row['Specimen date'], '%Y-%m-%d').date()
    days_ago = (today - date).days
    
    if (days_ago <= how_far):
        
        index = how_far-days_ago
        
        datec_array[index] = mdates.date2num(date)
        cases_array[index] = row['Daily lab-confirmed cases']


loc = DayLocator()
formatter = DateFormatter('%d/%m')

np_cases = np.array(cases_array)

np_cases    = [i for i in np_cases    if i!=None]
datec_array = [i for i in datec_array if i!=None]

fig, ax = plt.subplots()
plt.plot_date(datec_array, np_cases, linestyle='-')
ax.xaxis.set_major_locator(loc)
ax.xaxis.set_major_formatter(formatter)
ax.xaxis.set_tick_params(rotation=90, labelsize=10)
ax.set_xlabel('Date')
ax.set_ylabel('Number of new cases in '+my_region)
plt.grid()
plt.tight_layout()
plt.savefig('covid_cases_'+my_region.replace(" ", "_")+'.png')
plt.show()
