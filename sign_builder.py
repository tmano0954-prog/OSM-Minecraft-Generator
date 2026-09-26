import json, os
from generator.wikimedia.sign_scraper import fetch_sign_svg
from generator.wikimedia.svg_rasterizer import rasterize_svg_to_png
from generator.wikimedia.palette_quantizer import quantize_image_to_map_bytes

def build_signs(block_dict, map_data_dict, osm_data, proj):
    schematic_path = os.path.join(os.path.dirname(__file__), '../schematics/gantries/cantilever_pole.json')
    with open(schematic_path, 'r') as f:
        matrix = json.load(f)

    map_id_counter = 0
    for element in osm_data.get('elements', []):
        if element.get('type') == 'node' and 'traffic_sign' in element.get('tags', {}):
            lat, lon = element['lat'], element['lon']
            bx, bz = proj.latlon_to_block(lat, lon)
            sign_code = element['tags']['traffic_sign']
            
            for b in matrix:
                block_dict[(bx + b['x'], 64 + b['y'], bz + b['z'])] = (b['id'], b['meta'])
            
            svg_data = fetch_sign_svg(sign_code)
            img = rasterize_svg_to_png(svg_data)
            map_bytes = quantize_image_to_map_bytes(img)
            
            map_data_dict[map_id_counter] = map_bytes
            map_id_counter += 1
            