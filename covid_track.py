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
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--council", type=str, default='Oxfordshire', const=1, nargs='?')
parser.add_argument("--how_far", type=int, default=30, const=1, nargs='?')
parser.add_argument("--force_update", default=0, const=1, nargs='?')
parser.add_argument("--nosplash", default=0, const=1, nargs='?')
args = parser.parse_args()

my_region = args.council
how_far = args.how_far
force_update = args.force_update
splash = not args.nosplash


cases_csv  = "cases.csv"
here = os.path.isfile(cases_csv)
uptodate = False

if here:
    print ("Checking the file timestamp...")
    time_cases  = os.path.getmtime(cases_csv)
    today = time.time()
    
    uptodate = abs(time_cases-today)<12*3600
else:
    print ("Data files aren't here")

    
if (not uptodate or not here or force_update):
    print ("Refreshing the csvs")
    url_cases = "https://coronavirus.data.gov.uk/downloads/csv/coronavirus-cases_latest.csv"

    raw_cases  = requests.get(url_cases)

    cases_file = open(cases_csv,"w")
    cases_file.write(raw_cases.text)
    cases_file.close()

else:
    print("Files are up to date!")

cases  = pd.read_csv(cases_csv)

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

if splash:
    print("displaying")
    plt.show()
else:
    print("not displaying")
