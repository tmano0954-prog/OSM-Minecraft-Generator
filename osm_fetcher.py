import requests

def fetch_osm_data(bbox):
    south, west, north, east = bbox
    overpass_url = "https://overpass-api.de/api/interpreter"
    query = f"""
    [out:json][timeout:90];
    (
      way["highway"]({south},{west},{north},{east});
      way["building"]({south},{west},{north},{east});
      node["highway"="traffic_signals"]({south},{west},{north},{east});
      node["traffic_sign"]({south},{west},{north},{east});
    );
    out body;
    >;
    out skel qt;
    """
    response = requests.post(overpass_url, data={'data': query})
    response.raise_for_status()
    return response.json()
    