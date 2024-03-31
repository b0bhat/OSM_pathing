#!/usr/bin/env python3

'''
Handling input to generate data for the pipeline
'''

import os, requests
import pandas as pd
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from pillow_heif import register_heif_opener

import shared_methods

family_mode = False

# ammenities to exclude
amenities_not_include = [
    "toilets", "place_of_worship", "post_box", "telephone", "school", "bench", "community_centre",
    "waste_basket", "pharmacy", "dentist", "doctors", "post_office", "childcare", "clinic", "recycling",
    "public_bookcase", "university", "dojo", "veterinary", "bicycle_repair_station", "waste_disposal",
    "social_facility", "college", "construction", "post_depot", "nursery", "kindergarten", "conference_centre",
    "shower", "hospital", "trolley_bay", "fire_station", "police", "compressed_air", "family_centre",
    "music_school", "meditation_centre", "scrapyard", "language_school", "courthouse", "prep_school", "healthcare",
    "cram_school", "science", "ATLAS_clean_room", "workshop", "safety", "lobby", "animal_shelter",
    "vacuum_cleaner", "studio", "first_aid", "ranger_station", "storage_rental", "trash", "sanitary_dump_station",
    "housing co-op", "driving_school", "loading_dock", "chiropractor", "monastery", "storage", "payment_terminal",
    "Pharmacy", "waste_transfer_station", "office|financial", "letter_box", "training", "research_institute",
    "fuel", "parking", "parking_entrance", "bicycle_parking", "public_building", "bank", "shelter",
    "car_sharing", "drinking_water", "vending_machine", "parking", "ferry_terminal", "atm", "car_rental",
    "car_wash", "charging_station", "bicycle_rental", "seaplane terminal", "luggage_locker", "bureau_de_change",
    "taxi", "bus_station", "stripclub", "spa", "motorcycle_parking", "water_point", "boat_rental", "smoking_area",
    "EVSE", "car_rep", "watering_place", "lounge", "parking_space", "gym", "atm;bank", "hunting_stand", "money_transfer",
    "motorcycle_rental"
]

# assign manually the base weight to different amenity from range (1-10)

base_weights = {
    "cafe": 3,
    "fast_food": 2,
    "bbq": 3,
    "restaurant": 6,
    "pub": 5,    # family mode
    "cinema": 5,
    "theatre": 5,
    "bar": 6,    # family mode
    "library": 2,
    "fountain": 1,
    "photo_booth": 4,
    "nightclub": 5,    # family mode
    "tourism": 10,
    "marketplace": 9,
    "clock": 1,
    "gambling": 6,    # family mode
    "townhall": 2,
    "bistro": 5,
    "playground": 4,
    "events_venue": 6,
    "juice_bar": 3,
    "internet_cafe": 3,
    "social_centre": 3,
    "disused:restaurant": 6,
    "Observation Platform": 8,
    "park": 5,
    "biergarten": 5,    # family mode
    "casino": 5,    # family mode
    "leisure": 5,
    "shop|clothes": 7
}

# set to 0 if family friendly is on
adult_only_amenities = ['bar','pub','nightclub', 'gambling', 'casino']
if family_mode:
    for place in adult_only_amenities:
        if place in base_weights:
            base_weights[place] = 0

# Function to check if a tags has 'historic' or 'tourism' keys
def has_tourism(tags):
    return 'tourism' in tags

data = shared_methods.load_data(['../artifacts/amenities-vancouver.json.gz'])

# all records that have tourism key in their tag
tourism_data = data[data['tags'].apply(has_tourism)]

# remove records in the filtered_data that has 'bench' or 'Trans Canada Trail Pavillion' in the 'name' column
tourism_data = tourism_data[tourism_data['amenity'] != 'bench']
tourism_data = tourism_data[tourism_data['name'] != 'Trans Canada Trail Pavillion']

# for record in the filtered_data, change its 'amenity' column to 'tourism' and update the main data
data.loc[tourism_data.index, 'amenity'] = 'tourism'

# list with amenities to include
# amenities_include = set(data['amenity'].unique()) - set(amenities_not_include)  - set(food)
amenities_include = set(data['amenity'].unique()) - set(amenities_not_include)

# keep records in data that if the 'amenity' column is in the amenities_include list
data = data[data['amenity'].isin(amenities_include)]

# map the dictionary to the dataset
data['weight'] = data['amenity'].map(base_weights)
data.to_csv('../artifacts/weighted_amenities-vancouver.csv', index=False)
