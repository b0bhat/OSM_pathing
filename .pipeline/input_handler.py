import pandas as pd

# load the data for amenities-vancouver.json.gz
data = pd.read_json('./osm/amenities-vancouver.json.gz', lines=True)

# what are all unique values in the amenity column
#print(data['amenity'].unique())

amenities_not_include  = ["clock", "toilets", "place_of_worship", "post_box", "telephone", "school", "bench", "community_centre", "waste_basket", "pharmacy", "dentist", "doctors", "post_office", "childcare", "clinic", "recycling", "public_bookcase", "university", "dojo", "veterinary", "bicycle_repair_station", "waste_disposal", "social_facility", "college", "construction", "post_depot", "nursery", "kindergarten", "conference_centre", "shower", "hospital", "trolley_bay", "fire_station", "police", "compressed_air", "family_centre", "music_school", "shelter", "meditation_centre", "scrapyard", "language_school", "courthouse", "prep_school", "healthcare", "cram_school", "science", "ATLAS_clean_room", "workshop", "safety", "lobby", "animal_shelter", "vacuum_cleaner", "studio", "first_aid", "ranger_station", "storage_rental", "trash", "sanitary_dump_station", "housing co-op", "driving_school", "loading_dock", "chiropractor", "monastery", "storage", "payment_terminal", "Pharmacy", "waste_transfer_station", "office|financial", "letter_box", "training", "research_institute"]

# the 'tags' column is a dictionary, if tags' key is 'historic' or 'tourism', then set the record's amenity to the 'historic' or 'tourism'

# Function to check if a tags has 'historic' or 'tourism' keys
def has_tourism(tags):
    return 'tourism' in tags

filtered_data = data[data['tags'].apply(has_tourism)]
# print(filtered_data)

# remove records in the filtered_data that has 'bench' or 'Trans Canada Trail Pavillion' in the 'name' column
filtered_data = filtered_data[filtered_data['amenity'] != 'bench']
filtered_data = filtered_data[filtered_data['name'] != 'Trans Canada Trail Pavillion']

# for record in the filtered_data, change its 'amenity' column to 'tourism' and update the main data
data.loc[filtered_data.index, 'amenity'] = 'tourism'


amenities_include = set(data['amenity'].unique()) - set(amenities_not_include)

# keep records in data that if the 'amenity' column is in the amenities_include list
data = data[data['amenity'].isin(amenities_include)]
data.to_csv('amenities-vancouver-included.csv', index=False)