#!/usr/bin/env python3

'''
Shared methods for the pipeline
    - parse command line arguments
    - load data from file depends on the file extensions
    - translate address to latitude and longitude
    - get route from coordinates using OSRM api
    - plot the route on the map
    - read/save config file
'''

import json
import requests
import pandas as pd
import matplotlib.pyplot as plt
import argparse

class Helper:
    def __init__(self):
        # https://stackoverflow.com/questions/7427101/simple-argparse-example-wanted-1-argument-3-results
        # parse command line arguments
        parser = argparse.ArgumentParser(description='Route generation')
        parser.add_argument('-data', '--data', metavar='', required=True, help='Amenities data file path')
        parser.add_argument('-i', '--input_address', metavar='', required=True, help='Image file path or address')
        parser.add_argument('-o', '--output', metavar='', required=True, help='Output file path')
        parser.add_argument('-d', '--duration', metavar='', help='Duration')
        parser.add_argument('-t', '--point_time', metavar='', help='Time at point')
        parser.add_argument('-hu', '--hungriness', metavar='', help='Hungriness')
        parser.add_argument('-in', '--interestingness', metavar='', help='Interestingness')
        parser.add_argument('-f', '--family_mode', metavar='', help='Family mode')
        self.args = vars(parser.parse_args())


    # Load data from file depends on the file extensions
    def load_data(self, file):
        if file.endswith('.json.gz'):
            data = pd.read_json(file, lines=True)
        elif file.endswith('.csv'):
            data = pd.read_csv(file)
        else:
            raise ValueError("Error - file format")
        return data


    # https://nominatim.org/release-docs/develop/api/Search/
    # translate address to latitude and longitude
    def geo_coding(self, address):
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


    # https://project-osrm.org/docs/v5.5.1/api/#general-options
    # get route from coordinates using OSRM api
    def osrm_route_query(self, coordinates, mode='driving'):
        base_url = f"http://router.project-osrm.org/route/v1/{mode}/"
        coordinates_str = ";".join([",".join(map(str, coord)) for coord in coordinates])
        query_params = {
            "steps": "true",
            "geometries": "geojson",
            "overview": "full"
        }
        
        response = requests.get(base_url + coordinates_str, params=query_params)
        if response.status_code != 200: # unsessful
            print(f"[ERROR]: api call failed with code {response.status_code}")
            return None
        
        return response.json()


    # plot the route on the map
    def visualize_route(self, data, route):
        plt.scatter(data['lon'], data['lat'], s=5)
        route_lat = route['lat'].tolist()
        route_lon = route['lon'].tolist()
        plt.plot(route_lon, route_lat, marker='o', color='r', linestyle='-', markersize=3)
        plt.xlabel('lon')
        plt.ylabel('lat')
        plt.grid(True)
        plt.show()

    # save data into config file
    def save_config(self, data):
        with open('./config.json', 'w') as f:
            json.dump(data, f, indent=4)


    # https://www.geeksforgeeks.org/append-to-json-file-using-python/
    # append key: value pair to config file
    def add_config(self, new_data):
        with open('./config.json', 'r') as f:
            file_data = json.load(f)
        
        file_data.update(new_data)

        with open('./config.json', 'w') as f:
            json.dump(file_data, f, indent=4)

    # read config file
    def read_config(self, variables):
        with open('./config.json') as f:
            config = json.load(f)

        return [config.get(var) for var in variables]