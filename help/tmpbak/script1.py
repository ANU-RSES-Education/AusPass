
# coding: utf-8

# # A simple python example

# This script prints and plots an hour of seismic data recorded at the AUAYR station (AUSIS array, network code: S) using a standard FDSN request to access AusPass data.

# Requirements :
# - Having a working internet connection
# - Having either Python 2.7, 3.4. 3.5 or 3.6 installed
# - Having the ObsPy module installed. Use a package manager (such as conda or pip) to install all dependencies (numpy, SQLAlchemy, lxml, Cython, future, proj4, matplotlib and cartopy or basemap). For detailed instructions to install ObsPy, go to https://www.obspy.org/. 

# Description of obspy.read( ):
# 
# | Element                        | Signification                                                            |
# |--------------------------------|--------------------------------------------------------------------------|
# | ?                              | marks the end of the website adress serving the data                     |
# | &                              | separates the arguments to select AusPass data                           |
# |http://auspass.edu.au:80/     |Client name (AusPass website serving data on port 80)                   |
# |fdsnws/                         |FSDN Web Services on that client                                          |
# |dataselect/1/                   |Data retrieval services (distinct for station metadata and event metadata)|
# |query                           |Do a download                                                             |
# |net=S                           |Seismic network "S" - AUstralian Seismometers In Schools - AUSIS          |
# |sta=AUAYR                       |Station "AUAYR" located at Ayr, Queensland, Australia                     |
# |cha=BH?                         |All broadband channels available starting with "BH" ie. BHE, BHN and BHZ  |
# |start=2018-03-29T20:00:00.000   |Data start time using ISO standard date and time format                   | 
# |end=2018-03-29T21:00:00.000     |    Data end time using ISO standard date and time format                 |

# In[1]:

import obspy
x = obspy.read('http://auspass.edu.au:80/fdsnws/dataselect/1/query?net=S&sta=AUAYR&cha=BH?&start=2018-03-29T20:00:00.000&end=2018-03-29T21:00:00.000')
print(x)
x.plot()

