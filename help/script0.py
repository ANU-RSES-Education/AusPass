# Load Libraries
from obspy.clients.fdsn import Client
import obspy
# Connect to AusPass FDSN server
cl = Client('http://auspass.edu.au:80')
# Get waveform data from the Bilby experiment (arguments of the "get_waveforms" function are: network, station, location, channel, starttime, endtime in that order)
st = cl.get_waveforms('6F','*','*','BHZ',obspy.UTCDateTime('2009-09-29T17:50:00'), obspy.UTCDateTime('2009-09-29T18:50:00'), attach_response=True)
# Remove a linear trend in the waveform data
st.detrend(type='linear')
# Taper the trace
st.taper(0.05,type='hann')
# Convert raw data into a displacement (in meters) : apply a bandpass filter and deconvolve instrumental response
st.remove_response(output="DISP",pre_filt=(0.01,0.05,10,15))
# Plot the 10 first traces
st[0:10].plot(outfile='samoa.png')
