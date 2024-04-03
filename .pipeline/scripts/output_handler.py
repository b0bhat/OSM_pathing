#!/usr/bin/env python3

'''
Output dataframe into a GPX file and display the route on a map
'''

import numpy as np
from shared_methods import Helper

helper = Helper()
output_dir = helper.read_config(["output"])
output_filename = "output.gpx"
weighted_data = helper.load_data('../artifacts/weighted_amenities-vancouver.csv')
route = np.load("../artifacts/route.npy")

OUTPUT_TEMPLATE = (

)

# from exercise3 calc_distance_hint.py
def output_gpx(points, output_filename):
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

    with open(output_filename, 'w') as fh:
        doc.writexml(fh, indent=' ')


helper.visualize_route(weighted_data, route)
output_gpx(route, output_filename)
