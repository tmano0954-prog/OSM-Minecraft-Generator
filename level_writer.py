from nbtlib import File, Compound, String, Int, Long, Byte

def write_level_dat(spawn_x, spawn_y, spawn_z, level_name, output_path):
    nbt_data = File({
        'Data': Compound({
            'LevelName': String(level_name),
            'SpawnX': Int(spawn_x),
            'SpawnY': Int(spawn_y),
            'SpawnZ': Int(spawn_z),
            'generatorName': String('flat'),
            'Time': Long(6000),
            'DayTime': Long(6000),
            'version': Int(19133),
            'allowCommands': Byte(1)
        })
    })
    nbt_data.save(output_path, gzipped=True)
    