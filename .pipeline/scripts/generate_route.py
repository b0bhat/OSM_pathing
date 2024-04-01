#!/usr/bin/env python3

'''
Generating Route given the start location and amenities data set
'''

import requests
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from geopy.distance import geodesic
from sklearn.neighbors import BallTree

import shared_methods

# How many places to vist until you get hungry
hungriness = 10

# interesting point weight factor, from 1 (dont care) to 10 (only want interesting)
interestingness = 5

# comment this out unless testing
# np.random.seed(42)

def find_closest_points(tree, p_lat, p_lon, k=10, epsilon=0.001):
    p_lat += np.random.uniform(-epsilon, epsilon)
    p_lon += np.random.uniform(-epsilon, epsilon)
    dist, index = tree.query([(p_lat, p_lon)], k=k)
    return index[0], dist[0]

from sklearn.neighbors import BallTree

def calculate_route(all_data, start_point, max_points=10, max_distance=0.5):
    indices = []
    total_distance = 0
    data = all_data[all_data['food'] == 0].reset_index(drop=True)
    balltree = BallTree(data[['lat', 'lon']].values, leaf_size=15, metric='haversine')
    visited = set([])

    for i in range(max_points):
        if len(visited) == 0:
            current_point = start_point
        else:
            current_point = all_data.iloc[indices[-1]]

        neighbors, distances = find_closest_points(balltree, current_point['lat'], current_point['lon'], k=max_points)
        adjusted_distances = []
        for neighbor, distance in zip(neighbors, distances):
            weight = data.loc[neighbor]['weight']
            distance *= (1 - (weight - 1) / (20/interestingness))
            adjusted_distances.append((neighbor, distance))

        adjusted_distances.sort(key=lambda x: x[1])

        # Get a list of neighbors and if a neighbor is not in the list, use it as the next point
        for neighbor, distance in adjusted_distances:
            if neighbor not in visited:
                total_distance += distance
                lat = data.iloc[neighbor]['lat']
                lon = data.iloc[neighbor]['lon']
                all_data_index = all_data.query("lat == @lat & lon == @lon").index[0]
                indices.append(all_data_index)
                visited.add(neighbor)
                break
        if total_distance >= max_distance:
            break

    return all_data.iloc[indices], total_distance


def stitch_route(route):
    stitched_route = pd.DataFrame(columns=['lon', 'lat'])
    for i in range(len(route) - 1):
        point1 = (route.iloc[i]['lon'], route.iloc[i]['lat'])
        point2 = (route.iloc[i+1]['lon'], route.iloc[i+1]['lat'])
        route_raw = shared_methods.osrm_route_query([point1, point2])
        route_coords = route_raw['routes'][0]['geometry']['coordinates']
        route_df = pd.DataFrame(route_coords, columns=['lon', 'lat'])
        stitched_route = pd.concat([stitched_route, route_df], ignore_index=True)

    return stitched_route

location = np.load('../artifacts/location.npy')
point = pd.Series({'lat': location[1], 'lon': location[0]})

all_data = shared_methods.load_data('../artifacts/weighted_amenities-vancouver.csv')
# all_data = all_data[all_data['food'] == 0].reset_index()


# calculate_route <weighed data> <your test point> <max points in route> <max km in route>
route, total_distance = calculate_route(all_data, point, 15, 5)
print(route[['name', 'weight']])
shared_methods.visualize_route(all_data, route)
