# ductilebanana
Final project for CMPT-353 for group ductilebanana

## Project Topic: OSM, Photos, and Tours

Given an image or an starting address, this will generate a tour route output as gpx file.
The user can choose from several options to customize their route.

## Pipeline Structure
in `.pipeline/scripts` folder
- `input_handler.py` -> `data_cleaning.py` -> `generate_route` -> `output_handler.py`

## Input Variables
Adjust the values to your preference:
- `IMAGE`: the path to your image
- `FAMILY_MODE`: bool, True if less family-friendly places like bars and clubs should be removed.
- `INTERESTINGNESS`: float from 1-3, how much you value interesting points: 1: I dont care, 3: Give me more interesting points
- `HUNGRINESS`: int from 0 to 10, the number of interest points before you get hungry, 6 -> foodplace every 6 points
- `DURATION`: float, how long the trip should be, in hours.
- `POINT_DURATION`: float, how long you think you'll spend at each point on average, in hours.

## How to Run
1. Install `virtualenv`:
```
pip install --user virtualenv
pip3 install --user virtualenv # if have python3
```
2. Run `make run`:
```
make run IMAGE=<path_to_image> [FAMILY_MODE= MAX_DISTANCE= INTERESTINGESS= HUNGRINESS=] # optional
```
### Example runs:
```
make run                                # this will use default settings
make run IMAGE=./images/marinedr.jpg    # this will use marinedr.jpg as start
make run DURATION=3 FAMILY_MODE=5       # A 5 hour family trip
make run HUNGRINESS=2                   # I want lots of food
```

## Reference
- [Image Metadata](https://www.geeksforgeeks.org/how-to-extract-image-metadata-in-python/)
- [Handling GPS data](https://stackoverflow.com/questions/19804768/interpreting-gps-info-of-exif-data-from-photo-in-python)
- [Geo Coding](https://nominatim.org/release-docs/develop/api/Search/)
- [OSRM](https://project-osrm.org/docs/v5.5.1/api/#general-options)
