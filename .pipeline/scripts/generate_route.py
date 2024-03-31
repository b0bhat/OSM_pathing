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

# start_point = (-73.98568, 40.748817)
# end_point = (-73.98739, 40.764352)

# route_data = route_methods.osrm_route_query([start_point, end_point], mode="driving")
# print(route_data)

# need to take weight into account when finding nearest point
def find_closest_points(tree, p_lat, p_lon, k=10, epsilon=0.001):
    p_lat += np.random.uniform(-epsilon, epsilon)
    p_lon += np.random.uniform(-epsilon, epsilon)
    dist, index = tree.query([(p_lat, p_lon)], k=k)
    return index[0], dist[0]

def calculate_route(data, start_point, max_points=10, max_distance=0.5):
    indices = []
    total_distance = 0
    # total_weight = 0
    balltree = BallTree(data[['lat', 'lon']].values, leaf_size = 15, metric='haversine')
    visited = set([])

    for _ in range(max_points):
      if len(visited) == 0:
        current_point = start_point
      else:
        current_point = data.loc[indices[-1]]
      neighbors, distances = find_closest_points(balltree, current_point['lat'], current_point['lon'], k=max_points)
      adjusted_distances = []

      for neighbor, distance in zip(neighbors, distances):
        weight = data.loc[neighbor]['weight']
        distance *= (1-(weight-1)/20)
        adjusted_distances.append(distance)

      adjusted_distances.sort()

      # get a list of neighbors and if a neighbor is not in the list, use it as the next point
      for neighbor, distance in zip(neighbors, adjusted_distances):
        if neighbor not in visited:
            total_distance += distance
            # total_weight += data.loc[neighbor]['weight']
            indices.append(neighbor)
            visited.add(neighbor)
            break
      if total_distance >= max_distance:
        break

    return data.loc[indices], total_distance #, total_weight

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

data = shared_methods.load_data('../artifacts/weighted_amenities-vancouver.csv')

# calculate_route <weighed data> <your test point> <max points in route> <max km in route>
route, total_distance = calculate_route(data, point, 200, 50)

shared_methods.visualize_route(data, route)
