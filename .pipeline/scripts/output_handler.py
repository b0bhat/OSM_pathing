#!/usr/bin/env python3

'''
Output dataframe into a GPX file and output nice message to the terminal
'''

from datetime import datetime, timedelta
from shared_methods import Helper

helper = Helper()
output_dir, start_time, distance, duration = helper.read_config(["output", "start_time", "distance", "duration"])
output_file = f"{output_dir}/output.gpx"
weighted_data = helper.load_data('./.pipeline/artifacts/weighted_amenities-vancouver.csv')
route = helper.load_data("./.pipeline/artifacts/route.csv")

OUTPUT_TEMPLATE = (
    'Route generated successfully! 🗺️\n'
    '==> {output_file}\n'
    'You can check the route on https://www.mygpsfiles.com/app/\n'
    'Route informations:\n'
    ' - Total distance: {distance} km\n'
    ' - Total duration: {duration} hours\n'
    ' - Start time: {start_time}\n'
    ' - End time: {end_time}\n'
    'Happy exploring! 🚶'
)

# from exercise3 calc_distance_hint.py
def output_gpx(points, output_file):
    """
    Output a GPX file with latitude and longitude from the points DataFrame.
    """
    from xml.dom.minidom import getDOMImplementation
    def append_trkpt(pt, trkseg, doc):
        trkpt = doc.createElement('trkpt')
        trkpt.setAttribute('lat', '%.8f' % (pt['lat']))
        trkpt.setAttribute('lon', '%.8f' % (pt['lon']))
        trkseg.appendChild(trkpt)

    doc = getDOMImplementation().createDocument(None, 'gpx', None)
    trk = doc.createElement('trk')
    doc.documentElement.appendChild(trk)
    trkseg = doc.createElement('trkseg')
    trk.appendChild(trkseg)

    points.apply(append_trkpt, axis=1, trkseg=trkseg, doc=doc)

    with open(output_file, 'w') as fh:
        doc.writexml(fh, indent=' ')

# helper.visualize_route(weighted_data, route)
output_gpx(route, output_file)

# format the start time
start_time = datetime.strptime(start_time, '%Y:%m:%d %H:%M:%S')
# print(start_time)
# format = '%H:%M' # format with just hours and minutes
format = '%Y-%m-%d %H:%M' # formate with date, hours and minutes
start_time = start_time.strftime(format)
start_time = datetime.strptime(start_time, format)
# print(start_time)
# print(type(start_time))

# print to the terminal nicely
print(OUTPUT_TEMPLATE.format(
       output_file = output_file,
       distance = round(distance/1000, 2),
       duration = round(duration/3600, 2),
       start_time = start_time,
       end_time = start_time + timedelta(hours=duration)
))
