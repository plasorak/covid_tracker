 # covid_tracker
 
I was getting annoyed that I couldn't find a place to see how many COVID cases there are next to me over the last days.
This is quite simple, with the usual python, matplolib... download this file, modify the first 2 lines:
 - `my_region` = whatever county you are interested in,
 - `how_far` = how far back you want to see the data (in days)
 
 And then execute with `python covid_track.py`
 
The script downloads and saves a file (cases.csv) once a day. Also the image is saved.

Finally!

Damn.

Ok because I'm very lazy this is now going to run on a cron job and update the heck out of this picture every day (if that works).

![Oxfordshire](https://github.com/plasorak/covid_tracker/blob/master/covid_cases_Oxfordshire.png?raw=true)
![West Sussex](https://github.com/plasorak/covid_tracker/blob/master/covid_cases_West_Sussex.png?raw=true)
