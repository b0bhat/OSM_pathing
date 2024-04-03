# ductilebanana
Final project for CMPT-353 for group ductilebanana

## Pipeline Structure
in `.pipeline` folder
- `input_handler.py` -> `data_cleaning.py` -> `generate_route` -> `output_handler.py`

## Config
Adjust the values to your preference:

- `family_mode`: bool, Whether kid-unfriendly places like bars and clubs should be considered.
- `max_distance`: float, Max km for the route. (should be replaced by duration * speed + point_duration instead)
- `interestingness`: float from 1-3, how much you value interesting points: 1: I dont care, 3: Give me more interesting points
- `hungriness`: int from 0 to 10, the number of interest points before you get hungry, 6 -> foodplace every 6 points

need to implement:
- `duration`: How long the trip should be.
- `point_duration`: How long you think you'll spend at each point on average.

## Run
1. install `virtualenv` through
```
pip install --user virtualenv
pip3 install --user virtualenv # if have python3
```
2. 