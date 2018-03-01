import shapefile
import os
import pandas
import folium

basePath = r'C:\Development\base\shape'
fileName = r'national_shapefile_obs.shp'
baseFileName = os.path.join(basePath, fileName)

shpBase = shapefile.Reader(baseFileName)
fieldList = [x[1][0] for x in enumerate(shpBase.fields)]
fieldList.remove('DeletionFlag')

shpList = []

for record in shpBase.iterRecords():
    shpList.append(record)
    
shpFrame = pandas.DataFrame(shpList, columns = fieldList, index = None)
shpFrame[shpFrame['Observed'] == ''] = 0
shpFrame['Observed_Final'] = [float(x) for x in shpFrame['Observed']]
shpFrameMajor = shpFrame[(shpFrame['Status'] == 'major') | (shpFrame['Status'] == 'minor')]
finalFloodGaugeForMap = zip(shpFrameMajor['Latitude'], shpFrameMajor['Longitude'], \
                  shpFrameMajor['Observed_Final'], shpFrameMajor['Waterbody'], shpFrameMajor['State'])


# Initiate folium map
# Note the initial lat/long is centered on the US
floodGaugeMap = folium.Map(location=[37.797897, -96.107031],
                   zoom_start=5,
                   tiles='Stamen Terrain')


for gauge in finalFloodGaugeForMap:
    folium.CircleMarker([gauge[0], gauge[1]],
                        radius = gauge[2] / 10,
                        popup = 'Flood Level: %s, Where: %s, %s' % (gauge[2], gauge[3], gauge[4]),
                        color = '#000000',
                        fill_color = '#000000'
                       ).add_to(floodGaugeMap)