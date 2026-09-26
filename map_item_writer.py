import os
from nbtlib import File, Compound, Byte, Short, ByteArray

def write_map_dat_files(map_data_dict, output_data_folder):
    os.makedirs(output_data_folder, exist_ok=True)
    for map_id, map_bytes in map_data_dict.items():
        nbt_file = File({
            'data': Compound({
                'scale': Byte(0),
                'dimension': Byte(0),
                'height': Short(128),
                'width': Short(128),
                'colors': ByteArray(map_bytes)
            })
        })
        nbt_file.save(os.path.join(output_data_folder, f"map_{map_id}.dat"), gzipped=True)
        