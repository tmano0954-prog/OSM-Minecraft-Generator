import os, zipfile, io, shutil
from flask import Flask, render_template, request, send_file
from generator.osm_fetcher import fetch_osm_data
from generator.projection import Projection
from generator.voxelizer.road_builder import build_roads
from generator.voxelizer.building_builder import build_buildings
from generator.voxelizer.signal_builder import build_signals
from generator.voxelizer.sign_builder import build_signs
from generator.anvil.region_writer import write_region_file
from generator.anvil.level_writer import write_level_dat
from generator.anvil.icon_generator import create_world_icon
from generator.anvil.map_item_writer import write_map_dat_files

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate-world', methods=['POST'])
def generate_world():
    data = request.json
    bbox = data['bbox']
    spawn = data['spawn']
    version = data.get('version', '1.12.2')
    
    center_lat = (bbox[0] + bbox[2]) / 2.0
    center_lon = (bbox[1] + bbox[3]) / 2.0
    proj = Projection(center_lat, center_lon)
    
    osm_data = fetch_osm_data(bbox)
    block_dict = {}
    map_data_dict = {}

    build_roads(block_dict, osm_data, proj)
    build_buildings(block_dict, osm_data, proj)
    build_signals(block_dict, osm_data, proj)
    
    if data.get('renderMapSigns', True):
        build_signs(block_dict, map_data_dict, osm_data, proj)

    temp_dir = os.path.join(os.getcwd(), "temp_world")
    region_dir = os.path.join(temp_dir, "region")
    data_dir = os.path.join(temp_dir, "data")
    os.makedirs(region_dir, exist_ok=True)
    os.makedirs(data_dir, exist_ok=True)

    spawn_x, spawn_z = proj.latlon_to_block(spawn['lat'], spawn['lon'])
    write_level_dat(spawn_x, 65, spawn_z, f"OSM World ({version})", os.path.join(temp_dir, "level.dat"))
    write_region_file(block_dict, region_dir)
    write_map_dat_files(map_data_dict, data_dir)

    if version == '1.12.2':
        create_world_icon(temp_dir)

    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, temp_dir)
                zf.write(full_path, arcname=os.path.join("OSM_World", rel_path))

    shutil.rmtree(temp_dir)
    memory_file.seek(0)
    
    return send_file(
        memory_file,
        mimetype='application/zip',
        as_attachment=True,
        download_name=f'OSM_World_{version}.zip'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    