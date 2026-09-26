import json, os

def build_signals(block_dict, osm_data, proj):
    schematic_path = os.path.join(os.path.dirname(__file__), '../schematics/signals/yellow_mast_arm.json')
    with open(schematic_path, 'r') as f:
        matrix = json.load(f)

    for element in osm_data.get('elements', []):
        if element.get('type') == 'node' and element.get('tags', {}).get('highway') == 'traffic_signals':
            lat = element['lat']
            lon = element['lon']
            bx, bz = proj.latlon_to_block(lat, lon)
            for b in matrix:
                block_dict[(bx + b['x'], 64 + b['y'], bz + b['z'])] = (b['id'], b['meta'])
                