#!/usr/bin/env python3

'''
Cleaning the amenity data and assigning weights to each amenity
'''

import numpy as np

from shared_methods import Helper

# read environment variables
helper = Helper()
data_file, family_mode = helper.read_config(["data", "family_mode"])
data = helper.load_data(data_file)

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

# Food is segregrated to prevent overpoweing amenity weights
food_weights = {
    "cafe": 3,
    "fast_food": 2,
    "bbq": 3,
    "restaurant": 6,
    "pub": 5,    # family mode
    "bar": 6,    # family mode
    "bistro": 5,
    "juice_bar": 3,
    "biergarten": 5,    # family mode
    "disused:restaurant": 6,
}

# assign the base weight to different amenity from range (1-10)
base_weights = {
    "cinema": 5,
    "theatre": 5,
    "library": 2,
    "fountain": 1,
    "photo_booth": 4,
    "nightclub": 5,    # family mode
    "tourism": 10,
    "marketplace": 9,
    "clock": 1,
    "gambling": 6,    # family mode
    "townhall": 2,
    "playground": 4,
    "events_venue": 6,
    "internet_cafe": 3,
    "social_centre": 3,
    "Observation Platform": 8,
    "park": 5,
    "casino": 5,    # family mode
    "leisure": 5,
    "shop|clothes": 7
}

# Function to check if a tags has 'historic' or 'tourism' keys
def has_tourism(tags):
    return 'tourism' in tags


# main function
# set to 0 if family friendly is on
adult_only_amenities = ['bar','pub','nightclub', 'gambling', 'casino']
if family_mode:
    for place in adult_only_amenities:
        if place in base_weights:
            base_weights[place] = 0
        if place in food_weights:
            food_weights[place] = 0

# all records that have tourism key in their tag
tourism_data = data[data['tags'].apply(has_tourism)]

# remove records in the filtered_data that has 'bench' or 'Trans Canada Trail Pavillion' in the 'name' column
tourism_data = tourism_data[tourism_data['amenity'] != 'bench']
tourism_data = tourism_data[tourism_data['name'] != 'Trans Canada Trail Pavillion']

# for record in the filtered_data, change its 'amenity' column to 'tourism' and update the main data
data.loc[tourism_data.index, 'amenity'] = 'tourism'

# populate data with weights, remove nonweighted entries, label food places 
data['weight'] = data['amenity'].map({**base_weights, **food_weights})
data = data.dropna(subset=['weight'])
data['food'] = np.where(data['amenity'].isin(food_weights.keys()), 1, 0)
data.reset_index(drop=True, inplace=True)

# If the place has no name, it probably isn't very interesting, weight is halved
data.loc[data['name'].isnull(), 'weight'] //= 2
data = data[data['weight'] != 0]

# drop columns unneeded in route generation
unneeded = ['timestamp', 'tags', 'amenity']
data.drop(columns=unneeded, inplace=True)

data.to_csv('./.pipeline/artifacts/weighted_amenities-vancouver.csv', index=False)
# food_data.to_csv('../artifacts/food_amenities.csv', index=False)
