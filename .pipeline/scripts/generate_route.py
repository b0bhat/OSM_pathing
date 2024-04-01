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

hungriness, interestingness, max_distance = shared_methods.read_config(["hungriness", "interestingness", "max_distance"])

# np.random.seed(42)

def find_closest_points(tree, p_lat, p_lon, k=10, epsilon=0.001):
    p_lat += np.random.uniform(-epsilon, epsilon)
    p_lon += np.random.uniform(-epsilon, epsilon)
    dist, index = tree.query([(p_lat, p_lon)], k=k)
    return index[0], dist[0]

from sklearn.neighbors import BallTree

def calculate_route(all_data, start_point, max_points=10, max_distance=0.5):
    indices = []
    visited = set([])
    total_distance = 0 # total straight line distance between points
    # ignore food places
    data = all_data[all_data['food'] == 0].reset_index(drop=True)
    balltree = BallTree(data[['lat', 'lon']].values, leaf_size=15, metric='haversine')
    # food
    food = all_data[all_data['food'] == 1].reset_index(drop=True)
    balltree_food = BallTree(food[['lat', 'lon']].values, leaf_size=15, metric='haversine')

    for i in range(max_points):
        if len(visited) == 0:
            current_point = start_point
        else:
            current_point = all_data.iloc[indices[-1]]

        cur_balltree = balltree
        cur_data = data
        if i % hungriness == 0:
            cur_balltree = balltree_food
            cur_data = food

        # Use balltree to locate next k points
        neighbors, distances = find_closest_points(cur_balltree, current_point['lat'], current_point['lon'], k=20)
        adjusted_distances = []

        # Adjust distances with weights, making more interesting places seem closer for the purpose of sorting
        for neighbor, distance in zip(neighbors, distances):
            weight = cur_data.loc[neighbor]['weight']
            distance *= 1 - (weight - 1) * pow((interestingness / 3), 2)
            adjusted_distances.append((neighbor, distance))

        adjusted_distances.sort(key=lambda x: x[1])

        # From sorted list, check neighbours and if not visited, use as next point
        for neighbor, distance in adjusted_distances:
            if neighbor not in visited:
                total_distance += distance
                lat = cur_data.iloc[neighbor]['lat']
                lon = cur_data.iloc[neighbor]['lon']
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

# calculate_route <data> <start point> <max points in route> <max km in route>
route, total_distance = calculate_route(all_data, point, 100, )
# print(route[['name', 'weight']])
# print(route['weight'].mean())
shared_methods.visualize_route(all_data, route)
