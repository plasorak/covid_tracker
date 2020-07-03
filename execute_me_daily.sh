#!/bin/bash
current=`pwd`
cd /home/plasorak/Documents/covid_tracker
python3 covid_track.py --council "Oxfordshire" --nosplash
python3 covid_track.py --council "West Sussex" --nosplash
git add covid_cases_Oxfordshire.png covid_cases_West_Sussex.png
git commit -m "update for the ${date}"
git push origin master
cd $current
