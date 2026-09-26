PALETTE = [
    (0, 0, 0), (255, 255, 255), (127, 127, 127), (255, 0, 0),
    (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 124, 0)
]

def get_nearest_color_id(r, g, b):
    best_dist = float('inf')
    best_idx = 0
    for idx, (pr, pg, pb) in enumerate(PALETTE):
        dist = (r - pr)**2 + (g - pg)**2 + (b - pb)**2
        if dist < best_dist:
            best_dist = dist
            best_idx = idx
    return best_idx * 4 + 2

def quantize_image_to_map_bytes(image):
    image = image.resize((128, 128))
    data = bytearray()
    for y in range(128):
        for x in range(128):
            r, g, b = image.getpixel((x, y))
            data.append(get_nearest_color_id(r, g, b))
    return data
    