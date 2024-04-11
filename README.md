# ductilebanana
Final project for CMPT-353 for group ductilebanana

Project Topic: OSM, Photos, and Tours

Leveraging data to enhance tourist experiences is a pivotal part of modern tourism strategies. From an image taken at some location, our program plans a tour route through various interest points. Our methodology leverages OSM data and data processing techniques along with user input to generate a compelling route throughout the great Vancouver area.


## Pipeline Structure
in `.pipeline/scripts` folder
- `input_handler.py` -> `data_cleaning.py` -> `generate_route` -> `output_handler.py`

## Input Variables
Adjust the values to your preference:
- `INPUT_LOCATION`: image path or address
- `FAMILY_MODE`: bool, Whether kid-unfriendly places like bars and clubs should be considered.
- `MAX_DISTANCE`: float, Max distance for the route (in km). (should be replaced by duration * speed + point_duration instead)
- `INTERESTINGNESS`: float from 1-3, how much you value interesting points: 1: I dont care, 3: Give me more interesting points
- `HUNGRINESS`: int from 0 to 10, the number of interest points before you get hungry, 6 -> foodplace every 6 points

need to implement:
- `DURATION`: How long the trip should be.
- `POINT_DURATION`: How long you think you'll spend at each point on average.

## Run
1. Install `virtualenv`:
```
pip install --user virtualenv
pip3 install --user virtualenv # if have python3
```
2. Run
```
make run INPUT_LOCATION=<path_to_image> [FAMILY_MODE= MAX_DISTANCE= INTERESTINGESS= HUNGRINESS=] # optional
```
example run:
```
make run INPUT_LOCATION=./images/default_image.jpg
```

## TODO
- Modifying weights for categories
- Optimizing route to prevent backtracking
- Input preference for certain locations or amenity types
- Suggest resteraunts by time like 9am 1pm, 8pm,

## Reference
- [Image Metadata](https://www.geeksforgeeks.org/how-to-extract-image-metadata-in-python/)
- [Handling GPS data](https://stackoverflow.com/questions/19804768/interpreting-gps-info-of-exif-data-from-photo-in-python)
- [Geo Coding](https://nominatim.org/release-docs/develop/api/Search/)
- [OSRM](https://project-osrm.org/docs/v5.5.1/api/#general-options)
- [Parsing commandline argument](https://stackoverflow.com/questions/7427101/simple-argparse-example-wanted-1-argument-3-results)
- [Appending data to json](https://www.geeksforgeeks.org/append-to-json-file-using-python/)