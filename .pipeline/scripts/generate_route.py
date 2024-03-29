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

# https://project-osrm.org/docs/v5.5.1/api/#general-options
def osrm_route_query(coordinates, mode='driving'):
    base_url = f"http://router.project-osrm.org/route/v1/{mode}/"
    coordinates_str = ";".join([",".join(map(str, coord)) for coord in coordinates])
    query_params = {
        "steps": "true",
        "geometries": "geojson",
        "overview": "full"
    }
    response = requests.get(base_url + coordinates_str, params=query_params)
    return response.json()

start_point = (-73.98568, 40.748817)
end_point = (-73.98739, 40.764352)


route_data = osrm_route_query([start_point, end_point], mode="driving")
print(route_data)

# need to take weight into account when finding nearest point
def find_closest_points(tree, p_lat, p_lon, k=10, epsilon=0.001):
    p_lat += np.random.uniform(-epsilon, epsilon)
    p_lon += np.random.uniform(-epsilon, epsilon)
    dist, index = tree.query([(p_lat, p_lon)], k=k)
    return index[0], dist[0]

def calculate_route(data, starting_point_index, max_points=10, max_distance=0.5):
    indices = [starting_point_index]
    total_distance = 0
    total_weight = 0
    balltree = BallTree(data[['lat', 'lon']].values, leaf_size = 15, metric='haversine')
    visited = set([starting_point_index])

    for _ in range(max_points):
      current_point = data.loc[indices[-1]]
      neighbors, distances = find_closest_points(balltree, current_point['lat'], current_point['lon'], k=max_points)
      adjusted_distances = []

      for neighbor, distance in zip(neighbors, distances):
        weight = neighbor.loc[neighbor]['weight']
        distance *= (1-(weight-1)/20)
        adjusted_distances.append(distance)

      adjusted_distances.sort()

      # get a list of neighbors and if a neighbor is not in the list, use it as the next point
      for neighbor, distance in zip(neighbors, adjusted_distances):
        if neighbor not in visited:
            total_distance += distance
            total_weight += data.loc[neighbor]['weight']
            indices.append(neighbor)
            visited.add(neighbor)
            break
      if total_distance >= max_distance:
        break

    # accounts for weighting
    # for _ in range(max_points):
    #   current_point = data.loc[indices[-1]]
    #   neighbors, distances = find_closest_points(balltree, current_point['lat'], current_point['lon'], k=max_points)
    #   # get a list of neighbors and if a neighbor is not in the list, use it as the next point
    #   max_weight = 0
    #   max_neighbor = 0
    #   max_neighbor_distance = 0
    #   for neighbor, distance in zip(neighbors, distances):
    #     if neighbor not in visited:
    #       weight = data.loc[neighbor]['weight']
    #       if weight > max_weight:
    #           max_weight = weight
    #           max_neighbor = neighbor
    #           max_neighbor_distance = distance

    #   total_distance += max_neighbor_distance
    #   total_weight += max_weight
    #   indices.append(max_neighbor)
    #   visited.add(max_neighbor)
    #   if total_distance >= max_distance:
    #     break

    return data.loc[indices], total_distance, total_weight

def stitch_route(route):
    stitched_route = pd.DataFrame(columns=['lon', 'lat'])
    for i in range(len(route) - 1):
        point1 = (route.iloc[i]['lon'], route.iloc[i]['lat'])
        point2 = (route.iloc[i+1]['lon'], route.iloc[i+1]['lat'])
        route_raw = osrm_route_query([point1, point2])
        route_coords = route_raw['routes'][0]['geometry']['coordinates']
        route_df = pd.DataFrame(route_coords, columns=['lon', 'lat'])
        stitched_route = pd.concat([stitched_route, route_df], ignore_index=True)

    return stitched_route