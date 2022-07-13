# TC CDC - Fatal Injury and Violence Dashboard

**BEWARE:**  The current solution relies on development-grade Flask server, not
suitable for production use. For production use one of
[these receipts](https://flask.palletsprojects.com/en/1.1.x/deploying/)
should be followed.

### Build & Run

To build & run with Docker:
```
$ docker build -t cdc .
$ docker run --rm -p 8050:8050 cdc
```
The server starts at `http://localhost:8050`.

To run without Docker - follow the steps from `Dockerfile`.

### Map View

####
The Map View enables analysis of the percentual change of deaths between
a year and the year before, or between a range of years, in which the
average of each range is considered.

### Table View

####
The Table View display in a table the top increases or decreases in the number of deaths 
for the most recent data year compared to the previous data year, or optionally 
a selected range of years.

### Data View

####
The Data View display will support the ability to upload data (in CSV format) to the app by drag and drop.
User can use from the following option - 
- Use default file for the next run
- Overwrite existing file being used with the new file uploaded and selected from the UI for the next run
- Append new data points to the existing file being used to be picked for the next run

####
Once the file is uploaded before overwriting or appending a set of sanity checks are performed which are - 
- Check if the file exists
- Check if the data file is not empty
- Check if the no of columns is same as the existing file being used
- Check if the dtypes of the columns is same for each columns as the existing file is being used
- If any sanity check step fails the file is removed and user is prompted for the reason of the removal
- user can also see the preview of the existing data in the Preview Tab

#### Caching

If pre populating the cache is desired, run the populate_cache.py file,
it will populate cache with data for the map_view default options
for all years:
```
python populate_cache.py
```
Cache files will be generated in the CACHE_DIR, set in app.py.

In the app.py file, adjust the CACHE_THRESHOLD for a suitable value depending
on the cache needs and disk space available.

Data for comparison between year and last with all filters for County level takes 121Kb
Data for comparison between year and last with all filters for State level takes 3Kb
Data for combined report of intent x max deaths for State level takes 40Kb
Data for combined report of intent x max deaths for County level takes 2.1Mb

#### Metrics  

# HLM 

HLM compares the number of deaths in the user-selected year
with the number deaths within prior user-selected range of comparison years(default 3 years).

Example for 3-years baseline period
```
     2018
2017 2016 2015
```

Example for 6-years baseline period
```
     2018
2017 2016 2015
2014 2013 2012
```

if the ratio of current counts to the mean of the prior totals is greater than historical limits, 
then the current period is considered aberrant and included in top ratings. 

References: 
- http://wwwnc.cdc.gov/EID/article/21/2/14-0098-Techapp1.pdf
- https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4313630/
- https://www.sciencedirect.com/science/article/pii/S1532046417302290


# CUSUM

CUSUM uses the user-selected comparison years with 
the user-selected range of base years to calibrate the mean and expected standard deviation.
The results are ranked by the total calculated value of the requested year.

References: 
- https://en.wikipedia.org/wiki/CUSUM


