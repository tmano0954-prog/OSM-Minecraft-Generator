import anvil

def write_region_file(block_dict, output_folder):
    region = anvil.Region(os.path.join(output_folder, "r.0.0.mca"))
    
    # Fill bedrock and grass base
    for x in range(-64, 64):
        for z in range(-64, 64):
            region.set_block(anvil.Block('minecraft', 'bedrock'), x, 0, z)
            for y in range(1, 64):
                region.set_block(anvil.Block('minecraft', 'dirt'), x, y, z)
            region.set_block(anvil.Block('minecraft', 'grass'), x, 64, z)

    # Place custom block overrides
    for (x, y, z), (block_id, meta) in block_dict.items():
        if -256 <= x < 256 and -256 <= z < 256 and 0 <= y < 256:
            block_name = 'stone'
            if block_id == 159:
                block_name = 'stained_hardened_clay'
            elif block_id == 44:
                block_name = 'stone_slab'
            elif block_id == 95:
                block_name = 'stained_glass'
            elif block_id == 101:
                block_name = 'iron_bars'
            region.set_block(anvil.Block('minecraft', block_name), x, y, z)

    region.save(os.path.join(output_folder, "r.0.0.mca"))
    