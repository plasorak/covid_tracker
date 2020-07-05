# covid_tracker
 
I was getting annoyed that I couldn't find a place to see how many COVID cases there are next to me over the last days.
This is quite simple, with the usual python, matplolib... clown this repo and then execute with `python covid_track.py`.

You can give these arguments:
 - `--force_update` = to force updating the csv
 - `--council "West Sussex"` = whatever county you are interested in,
 - `--how_far 30` = how far back you want to see the data (in days)
 - `--nosplash` = so that you only get the file (and don't show the plot on your screen)

The script downloads and saves a file (cases.csv) once a day. Also the image is saved.

Finally!

Damn.

## Results

<a name="plots"/>

OK because I'm very lazy this is now going to run on a cron job and update the heck out of this picture every day (if that works).

![Oxfordshire](https://github.com/plasorak/covid_tracker/blob/master/covid_cases_Oxfordshire.png?raw=true)
![West Sussex](https://github.com/plasorak/covid_tracker/blob/master/covid_cases_West_Sussex.png?raw=true)
