#!/usr/bin/env python3

'''
Output dataframe into a GPX file and display the route on a map
'''

import numpy as np
import pandas as pd
from shared_methods import Helper

helper = Helper()
_, output_dir = helper.read_config(["data", "output"]) # somehow, if I read the output alone, it will return [./output] instead of ./output, when I read it will some other value it will return the correct value
output_file = f"{output_dir}/output.gpx"
weighted_data = helper.load_data('./.pipeline/artifacts/weighted_amenities-vancouver.csv')
route = helper.load_data("./.pipeline/artifacts/route.csv")

OUTPUT_TEMPLATE = (

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
print("You can check the route on https://www.mygpsfiles.com/app/")
output_gpx(route, output_file)
