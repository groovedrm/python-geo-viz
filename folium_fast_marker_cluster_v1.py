import folium
import numpy

def retLatLong(sLat, sLong):
    return([sLat + (numpy.random.random() * 2.5), sLong + (numpy.random.random() * 2.5)])

# Create 5 clusters throughout US

# 1 - Smack In Middle
startLat_1 = 37.519578
startLong_1 = -96.634375
clusterData_1 = [retLatLong(startLat_1, startLong_1) for i in range(100000)]

# 2 - California
startLat_2 = 37.620967
startLong_2 = -121.166867
clusterData_2 = [retLatLong(startLat_2, startLong_2) for i in range(100000)]

# 3 - Texas [Houston]
startLat_3 = 29.657258
startLong_3 = -95.854367
clusterData_3 = [retLatLong(startLat_3, startLong_3) for i in range(100000)]

# 4 - NY Metro
startLat_4 = 41.218118
startLong_4 = -74.145382
clusterData_4 = [retLatLong(startLat_4, startLong_4) for i in range(100000)]

# 5 - Miami
startLat_5 = 26.163070
startLong_5 = -80.209835
clusterData_5 = [retLatLong(startLat_5, startLong_5) for i in range(100000)]

# Combine the cluster lists into a single list for consumption in the map
combinedCluster = clusterData_1 + clusterData_2 + clusterData_3 + clusterData_4 + clusterData_5

# Create the map
map = folium.Map(
    location = [startLat, startLong],
    tiles = 'Stamen Toner',
    detect_retina = True, 
    prefer_canvas = True,
    zoom_start = 4
)

# Create the Leaflet cluster and add it to the map
markerCluster = folium.plugins.FastMarkerCluster(combinedCluster).add_to(map)

# Notes:
# 1M points seesm to really test Chrome, have to kill page
# 1M points works in Safari except the points aren't displayed
# 500k points WORKS IN CHROME!

# Output
map

