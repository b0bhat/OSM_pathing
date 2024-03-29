#!/usr/bin/env python3

'''
Handling input to generate data for the pipeline
'''

import os, requests
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from pillow_heif import register_heif_opener

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

  print(decimal)
  return decimal

# https://nominatim.org/release-docs/develop/api/Search/
def geo_coding(address):
    base_url = f"https://nominatim.openstreetmap.org/search?"
    params = {
        "q": address,
        "format": "json"
    }
    headers = {
        "User-Agent": "cmpt353project"
    }
    response = requests.get(base_url, params=params, headers=headers)
    if response.status_code == 200: # successful
      result   = response.json()
      latitude  = result[0]['lat']
      longitude = result[0]['lon']
    else:
      print(f"[ERROR]: api call failed with code {response.status_code}")
      return None

    return (float(longitude), float(latitude))
