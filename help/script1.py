
# coding: utf-8

# # A simple python example

# This script prints and plots an hour of seismic data recorded at the AUAYR station (AUSIS array, network code: S) using a standard FDSN request to access AusPass data.

# Requirements :
# - A working internet connection
# - Python3 (2.7 may also work but not recommended)
# - ObsPy installed. Use a package manager (such as conda or pip) to install all dependencies (numpy, SQLAlchemy, lxml, Cython, future, proj4, matplotlib and cartopy or basemap). For detailed instructions to install ObsPy, go to https://www.obspy.org/. 

# At its simplest, obspy can be used in a manner equivalent to curl or wget (or a web browser!) to grab miniseed data via a single target, similar to pointing to a file
# 
# | Element                        | Signification                                                            |
# |--------------------------------|--------------------------------------------------------------------------|
# | ?                              | marks the end of the website adress serving the data                     |
# | &                              | separates the arguments to select AusPass data                           |
# |http://auspass.edu.au:80/       |Client name (AusPass website serving data on port 80)                   |
# |fdsnws/                         |FSDN Web Services on that client                                          |
# |dataselect/1/                   |Data retrieval services (distinct for station metadata and event metadata)|
# |query                           |Do a download                                                             |
# |net=S1                          |Seismic network "S1" - AUstralian Seismometers In Schools - AUSIS          |
# |sta=AUAYR                       |Station "AUAYR" located at Ayr, Queensland, Australia                     |
# |cha=BH?                         |All broadband channels available starting with "BH" ie. BHE, BHN and BHZ  |
# |start=2018-03-29T20:00:00.000   |Data start time using ISO standard date and time format                   | 
# |end=2018-03-29T20:10:00.000     |Data end time using ISO standard date and time format                 |

# In[1]:
import obspy
st = obspy.read('http://auspass.edu.au:80/fdsnws/dataselect/1/query?net=S1&sta=AUAYR&cha=BH?&start=2018-03-29T20:00:00.000&end=2018-03-29T20:10:00.000')
print(st)
st.plot()

# # However the true utility of this protocol is its use in a modular or object-oriented sense. Let's try again.

# In[2]
import obspy
from obspy.clients.fdsn import Client as FDSN_Client

# # Establish an FDSN connection 
#  User_agent field is not required, but it is polite to include and allows us to contact you in the unlikely event your requests are causing an issue. Your address is not stored or added to any lists.
#  User and password should ONLY be given here if you are requesting restricted data. Restricted data is typically limited to the PI for up to 2 years following its availability here.
#  For access you must either a) wait or b) contact the PI, we are not able to grant access ourselves. 
# In[3]
auspass = FDSN_Client('http://auspass.edu.au:8080',user_agent='email@address.com') #,user='username',password='password')

# # Set request parameters
# In[4]
net = "S1"
station = "AUAYR"
location = "*" #n.b. AusPass data typically has a univeral blank (e.g. '') value for ALL station locations. "*" works just as well. 
channel = "BH*"
time0 = obspy.UTCDateTime(2018,3,29,1,20,10) #1 hour, 20 minutes, and 10 seconds after start of March 29 2018 (UTC) 
time1 = time0 + 60 #60 seconds after time0

# # Pull data from AusPass, and plot 
# (n.b. the commonly used "st" variable is short for "stream", comprising a group of ~similar waveforms clustered together. A "trace" (usually "tr") is one element of a stream array e.g. tr = st[0])
# In[5]
st = auspass.get_waveforms(network=net,station=station,location=location,channel=channel,starttime=time0,endtime=time1)
print(st)
st.plot()

#Network and staton metadata (and response information) can be downloaded from AusPass in a similar manner. This is commonly referred to as "inventory" data (with variable "inv")
# In[6]
inv = auspass.get_stations(network=net,level='channel') #this simply downloads all station information for a network. if you ONLY want station locations, set channel='station'. if you need response information, set channel='response'

#inventory can also be loaded via local file, or alternate formats beyond stationXML such as RESP or DATALESS SEED
# inv = obspy.read_inventory("filename",format='SEED') #or format='RESP', 'STATIONTXT', or...

#optionally you can be more specific, e.g. if you're looking for stations ONLY within a certain date
# In[7]
inv = auspass.get_stations(network=net,starttime=time0,endtime=time1,level='response')
inv.plot(projection='local', color_per_network=True) #can quickly show where these stations are

# You can also search for stations/networks within a certain area
# In[8]
inv = auspass.get_stations(network="*",minlatitude=-23.0, maxlatitude=-22.5, minlongitude=133.0, maxlongitude=134.0) #bounding box
#inv = auspass.get_stations(network="*",latitude=-23.0, latitude=-22.5, minradius=0.1,maxradius=4) #OR, search a radius (in degrees) from a central point

# Like most python codes, references for these functions are accessible just by typing "auspass.get_stations?" or "auspass.get_waveforms?"

# # Finally let's work with this data!

# Filtering is easy, and there are many types and methods to choose from in ObsPy. Here is a simple Butterworth Bandpass between 1-20 Hz

# In[9]
st.filter('bandpass',freqmin=1.0, freqmax=20.0)

#NOTE that this operation is irreversible! So if you want to try a different filter you'll have to re-load your waveform data. 
# In[10]
st_bak = st.copy()
st.filter('bandpass',freqmin=0.1, freqmax=0.4)
st = st_bak.copy() #revert to original 

# Removing instrument response is also very very easy! 
# In[12]
st.remove_response(inventory=inv) #this automatically parses the inventory for the correct network/station/channel response!

# Response information can also be examined and even plotted
# In[13]
#first, filter inventory for the exact response we want
inv0 = inv.select(network=net,station=station)

#response is at the channel level (three subsets down) e.g. inv[network][station][channel]
response = inv0[0][0][0].response
response.plot(min_freq=.001)

# # Some other common operations..
# In[14]
st.trim(starttime=time0,endtime=time1-5) #trims the last 5 seconds off all data in the stream

sub_st = st.slice(starttime=time0,endtime=time1-5) #returns a NEW stream "sub_st" instead, without altering original

st.decimate(factor=2) #performs a literal decimation bt "factor" amount (e.g. 100 Hz > 50 Hz)

st.interpolate(method='quadratic',sampling_rate=10) #interpolate data to a set sampling rate (or via number or samples, or a time range, or...? Performs better than straight decimation when the factor is large)

# The data contained in each trace is equivalent to a numpy array, and all operations in numpy can be performed (e.g. calculating a mean or standard deviation)
# In[15]
import numpy as np
tr = st[0]
std = np.std(tr.data)
mean = np.mean(tr.data)

# Metadata can also be called/printed/altered. It is kept at the "trace" level under "stats"
# In[15]
tr.stats #quickly prints what's available
sr = tr.stats.sampling_rate
delta = tr.stats.delta #the time in seconds per sample (e.g. 1/sr)
start = tr.stats.starttime + 1 #shifts starttime 1 second into the future
tr.stats.station = "NEWSTATIONNAME" #changes station name to whatever you like!
print("station name is now %s, and it now starts at %s" % (tr.stats.station,start))

# # Saving to disk 
# In[16]
inv.write("S1.xml",format='STATIONXML',validate=True) #saves a local copy of inv as a 'STATIONXML', and validates it is structured correctly. Unfortunately you cannote write to RESP or Dataless Seed.

#Saving miniseed data can be a little trickier, and you may have to organise filenames and data depending on what you're trying to do. To simply save the entire stream of data into a singular file, 
# In[17]
st.write("filename.ms",format='MSEED',encoding='STEIM2',reclen=4096)



