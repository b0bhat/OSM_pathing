#!/usr/bin/python3

'''
Handling input to generate data for the pipeline
'''

import os, requests
import numpy as np
import sys
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from pillow_heif import register_heif_opener

from shared_methods import Helper

# get input variables
helper = Helper()
data = helper.args['data']
imagefile = helper.args['image']
output = helper.args['output']
max_distance = float(helper.args['distance'])
hungriness = float(helper.args['hungriness'])
interestingness = float(helper.args['interestingness'])
family_mode = helper.args['family_mode']

# reference: https://www.geeksforgeeks.org/how-to-extract-image-metadata-in-python/
def get_metadata(image_file):
  if image_file.endswith(".jpg") or image_file.endswith(".JPG") or image_file.endswith(".jpeg"):
    image = Image.open(image_file)
  elif image_file.endswith(".HEIC"):
    register_heif_opener()
    image = Image.open(image_file)

  # extract exif metadata
  exif_data = {}
  exif_info = image._getexif()

  if not exif_info:
    return None

  for tag, value in exif_info.items():
    decoded = TAGS.get(tag, tag)
    if decoded == "GPSInfo":
      gps_data = {}
      for gps_tag in value:
          sub_decoded = GPSTAGS.get(gps_tag, gps_tag)
          gps_data[sub_decoded] = value[gps_tag]
      exif_data[decoded] = gps_data
    else:
      exif_data[decoded] = value

  return exif_data

# reference: https://stackoverflow.com/questions/19804768/interpreting-gps-info-of-exif-data-from-photo-in-python
def gps_data_to_degree(degrees, minutes, seconds, direction):
  decimal = degrees + minutes / 60 + seconds / 3600
  if direction in ['S', 'W']:
      decimal = -decimal
  return decimal

# get location from image metadata
metadata = get_metadata(imagefile)
latitude = gps_data_to_degree(*metadata['GPSInfo']['GPSLatitude'], metadata['GPSInfo']['GPSLatitudeRef'])
longitude = gps_data_to_degree(*metadata['GPSInfo']['GPSLongitude'], metadata['GPSInfo']['GPSLongitudeRef'])

location = (float(longitude), float(latitude))

# save all input variables to config.json
print(f"""Inputs:
Data                    = {data}
Location of Input Image = {location}
Output Path             = {output}
Max Distance            = {max_distance}
Hungriness              = {hungriness}
Interestingness         = {interestingness}
Family Mode             = {family_mode}
""")

helper.save_config({
  "data": data,
  "location": location,
  "output": output,
  "max_distance": max_distance,
  "hungriness": hungriness,
  "interestingness": interestingness,
  "family_mode": family_mode
})