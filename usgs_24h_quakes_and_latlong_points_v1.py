import warnings
warnings.filterwarnings('ignore')

# Libraries
import pandas
import requests
import geojson
import folium
import numpy
from folium import plugins

# Helper functions
def colorCode(colorValue):
    if colorValue < 1.0:
        return '#FADBD8'
    elif colorValue < 2.0:
        return '#F5B7B1'
    elif colorValue < 3.0:
        return '#E6B0AA'
    elif colorValue < 4.0:
        return '#EC7063'
    else:
        return '#B03A2E'
    
def retLatLong(sLat, sLong):
    return([sLat + (numpy.random.random() * 2.5), sLong + (numpy.random.random() * 2.5)])

# ------------------------
# Data Gathering/Creation
# ------------------------
eqJsonLink = r'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson'

# Block to grab the GeoJSON [latest]
resp = requests.get(eqJsonLink, verify = False)
fd = open('all_day.geojson', 'wb')
fd.write(resp.content)
fd.close()

# Import and process json into useful Python object
eqGeoFile = geojson.load(open('all_day.geojson'))
eqGeoFeatureCol = geojson.FeatureCollection(eqGeoFile)

# Make a blank dataframe
names = ['Lat','Long','eventTitle','eventMagnitude','eventPlaceDesc','eventUrl']
eqUSGSDF = pandas.DataFrame(columns = names)
eqUSGSDF['Lat'] = eqUSGSDF['Lat'].astype(float)
eqUSGSDF['Long'] = eqUSGSDF['Long'].astype(float)
eqUSGSDF['eventTitle'] = eqUSGSDF['eventTitle'].astype(str)
eqUSGSDF['eventMagnitude'] = eqUSGSDF['eventMagnitude'].astype(float)
eqUSGSDF['eventPlaceDesc'] = eqUSGSDF['eventPlaceDesc'].astype(str)
eqUSGSDF['eventUrl'] = eqUSGSDF['eventUrl'].astype(str)

# Clusters
# 1 - California Southern
startLat_1 = 34.286565
startLong_1 = -118.561021
clusterData_1 = [retLatLong(startLat_1, startLong_1) for i in range(100000)]

# 2 - California Northern
startLat_2 = 38.063080
startLong_2 = -121.988756
clusterData_2 = [retLatLong(startLat_2, startLong_2) for i in range(100000)]

combinedCluster = clusterData_1 + clusterData_2

# ------------------------
# Begin to work with map library
# ------------------------

# Create map
map = folium.Map(
    location = [37.852995, -120.999986],
    tiles = 'Stamen Terrain',
    detect_retina = True, 
    prefer_canvas = True,
    zoom_start = 4
)

# Add the random point marker cluster first
markerCluster = folium.plugins.FastMarkerCluster(combinedCluster).add_to(map)

# Add USGS quakes to the map

i = 0
for feature in eqGeoFeatureCol['features']:
    # Extract coordinates
    x = feature['geometry']['coordinates'][1]
    y = feature['geometry']['coordinates'][0]
    # In geospatial software, the x is the longitude, y is the latitude
    
    # Extract properties
    title = feature['properties']['title']
    mag = feature['properties']['mag']
    place = feature['properties']['place']
    url = feature['properties']['url']
    evID  = feature['id']

    # Add to frame
    # eqUSGSDF.loc[i] = [x, y, title, mag, place, url]
    # folium.Marker([x, y], popup = title, ).add_to(eqMap)
    folium.CircleMarker([x, y],
                        radius = mag * 10,
                        popup = title,
                        color = '#000000',
                        fill_color = colorCode(mag)
                       ).add_to(map)
    
    # Add to map
    
    # Iterate
    i = i + 1
    
map.save('folium_combined_USGS_RandomCalPoints_v1t.html')