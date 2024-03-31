'''
Shared methods for routing
'''
import requests
import pandas as pd
import matplotlib.pyplot as plt

def load_data(file):
    if file.endswith('.json.gz'):
        data = pd.read_json(file, lines=True)
    elif file.endswith('.csv'):
        data = pd.read_csv(file)
    else:
        raise ValueError("Error - file format")
    return data

# https://nominatim.org/release-docs/develop/api/Search/
def geo_coding(address):
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

def visualize_route(data, route):
    data = load_data('../artifacts/weighted_amenities-vancouver.csv')
    plt.scatter(data['lon'], data['lat'], s=5)
    route_lat = route['lat'].tolist()
    route_lon = route['lon'].tolist()
    plt.plot(route_lon, route_lat, marker='o', color='r', linestyle='-', markersize=3)
    plt.xlabel('lon')
    plt.ylabel('lat')
    plt.grid(True)
    plt.show()