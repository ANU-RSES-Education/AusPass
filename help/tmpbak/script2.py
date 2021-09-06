# coding: utf-8
# # Load Libraries
# In[1]:
from obspy.clients.fdsn import Client
import obspy
get_ipython().run_line_magic('matplotlib', 'inline')
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
from obspy.geodetics.base import gps2dist_azimuth
from matplotlib.transforms import blended_transform_factory
plt.style.use(['seaborn-poster'])
# # Connect to AusPass FDSN server
# In[2]:
cl = Client('http://auspass.edu.au:80')
# # Download and map stations
# In[3]:
inv = cl.get_stations(network='*',station='*',starttime=obspy.UTCDateTime('1950-01-01'),endtime=obspy.UTCDateTime('2018-03-29T21:35:3'))
inv.plot(projection='local', color_per_network=True)
# # Select the data recorded at AuSIS stations after the PNG earthquakes
# In[4]:
#PNG Event Mw6.9
lat = -5.532
lon = 151.500
# In[10]:
st = cl.get_waveforms('S','*','*','BHZ',obspy.UTCDateTime('2018-03-29T21:25:36'), obspy.UTCDateTime('2018-03-29T21:35:36'), attach_response=True)
inv = cl.get_stations(network='S',station='*',starttime=obspy.UTCDateTime('2018-03-29T21:25:36'),endtime=obspy.UTCDateTime('2018-03-29T21:35:3'))
# # Map ray paths
# In[14]:
fig = plt.figure()
# Define the Cartopy Projection
maxlat = 0.
minlat = -50
maxlon = 190
minlon = 100
lat0 = (maxlat + minlat)/2.0
lon0 = (maxlon + minlon)/2.0
proj_kwargs={}
proj_kwargs['central_latitude'] = lat0
proj_kwargs['central_longitude'] = lon0
proj_kwargs['standard_parallels'] = [lat0,lat0]
proj = ccrs.AlbersEqualArea(**proj_kwargs)
map_ax = fig.add_axes([0.1,0.1,0.8,0.8],projection=proj)
x0, y0 = proj.transform_point(lon0, lat0, proj.as_geodetic())
deg2m_lat = 2 * np.pi * 6371 * 1000 / 360
deg2m_lon = deg2m_lat * np.cos(lat0 / 180 * np.pi)
height = (maxlat - minlat) * deg2m_lat
width = (maxlon - minlon) * deg2m_lon
map_ax.set_xlim(x0 - width / 2, x0 + width / 2)
map_ax.set_ylim(y0 - height / 2, y0 + height / 2)
# Plot the Coastlines
map_ax.coastlines()
# Plot the Parallels and Meridians
map_ax.gridlines()
st.merge()
# Plot the source with a dot
map_ax.scatter(lon, lat, marker="o", s=120, zorder=10,
                color="k", edgecolor="w", transform = proj.as_geodetic())
# Plot the station with data with a triangle, and the path source-reciever
for station in inv[0]:
    if len(st.select(station=station.code))!=0:
        map_ax.scatter(station.longitude, station.latitude, marker="v", s=120, zorder=10,
                 color="k", edgecolor="w", transform = proj.as_geodetic())
        plt.plot([station.longitude, lon], [station.latitude, lat], color='0.8',  transform=ccrs.Geodetic())
        st.select(station=station.code)[0].stats.distance=gps2dist_azimuth(station.latitude, station.longitude, lat, lon, a=6378137.0, f=0.0033528106647474805)[0]
# In[15]:
st.filter(type='bandpass',freqmin=0.1,freqmax=10)
# In[16]:
fig = plt.figure(figsize=(10,10))
st.plot(type='section', plot_dx=500e3, recordlength=10*60,
        time_down=True, linewidth=1, grid_linewidth=.25, show=False, fig=fig)
# Plot customization: Add station labels to offset axis
ax = fig.axes[0]
transform = blended_transform_factory(ax.transData, ax.transAxes)
for tr in st:
    ax.text(tr.stats.distance / 1e3, 1.0, tr.stats.station, rotation=270,
            va="bottom", ha="center", transform=transform, zorder=10)
plt.show()

