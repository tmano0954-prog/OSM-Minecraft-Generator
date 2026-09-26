def build_buildings(block_dict, osm_data, proj):
    node_map = {n['id']: (n['lat'], n['lon']) for n in osm_data.get('elements', []) if n['type'] == 'node'}
    for element in osm_data.get('elements', []):
        if element.get('type') == 'way' and 'building' in element.get('tags', {}):
            nodes = element.get('nodes', [])
            building_coords = []
            for nid in nodes:
                if nid in node_map:
                    lat, lon = node_map[nid]
                    building_coords.append(proj.latlon_to_block(lat, lon))
            
            levels = int(element.get('tags', {}).get('building:levels', 2))
            height_blocks = max(4, levels * 3)

            for i in range(len(building_coords) - 1):
                x0, z0 = building_coords[i]
                x1, z1 = building_coords[i+1]
                dx = abs(x1 - x0)
                dz = abs(z1 - z0)
                sx = 1 if x0 < x1 else -1
                sz = 1 if z0 < z1 else -1
                err = dx - dz
                cx, cz = x0, z0
                while True:
                    for h in range(1, height_blocks + 1):
                        block_type = (95, 0) if h % 3 == 2 else (159, 8)
                        block_dict[(cx, 64 + h, cz)] = block_type
                    if cx == x1 and cz == z1:
                        break
                    e2 = 2 * err
                    if e2 > -dz:
                        err -= dz
                        cx += sx
                    if e2 < dx:
                        err += dx
                        cz += sz
                        