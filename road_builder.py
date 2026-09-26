def rasterize_line(x0, z0, x1, z1):
    points = []
    dx = abs(x1 - x0)
    dz = abs(z1 - z0)
    sx = 1 if x0 < x1 else -1
    sz = 1 if z0 < z1 else -1
    err = dx - dz
    while True:
        points.append((x0, z0))
        if x0 == x1 and z0 == z1:
            break
        e2 = 2 * err
        if e2 > -dz:
            err -= dz
            x0 += sx
        if e2 < dx:
            err += dx
            z0 += sz
    return points

def build_roads(block_dict, osm_data, proj):
    node_map = {n['id']: (n['lat'], n['lon']) for n in osm_data.get('elements', []) if n['type'] == 'node'}
    for element in osm_data.get('elements', []):
        if element.get('type') == 'way' and 'highway' in element.get('tags', {}):
            nodes = element.get('nodes', [])
            for i in range(len(nodes) - 1):
                if nodes[i] in node_map and nodes[i+1] in node_map:
                    lat1, lon1 = node_map[nodes[i]]
                    lat2, lon2 = node_map[nodes[i+1]]
                    x0, z0 = proj.latlon_to_block(lat1, lon1)
                    x1, z1 = proj.latlon_to_block(lat2, lon2)
                    points = rasterize_line(x0, z0, x1, z1)
                    for px, pz in points:
                        for dx in range(-3, 4):
                            for dz in range(-3, 4):
                                block_dict[(px + dx, 64, pz + dz)] = (159, 9)
                        for dx in range(-4, 5):
                            if abs(dx) == 4:
                                block_dict[(px + dx, 65, pz)] = (44, 0)
                                