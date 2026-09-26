import math

class Projection:
    def __init__(self, center_lat, center_lon):
        self.center_lat = center_lat
        self.center_lon = center_lon
        self.lat_rad = math.radians(center_lat)

    def latlon_to_block(self, lat, lon):
        delta_lon = lon - self.center_lon
        delta_lat = lat - self.center_lat
        x = delta_lon * 111320.0 * math.cos(self.lat_rad)
        z = -1.0 * (delta_lat * 110540.0)
        return int(round(x)), int(round(z))
        