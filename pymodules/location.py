"""
Location information
"""

# Local import
from pymodules import constant as config


class Coordinate(object):
    """
    Coordinate
    """
    region = None
    lat = None
    lat_dir = None
    lon = None
    lon_dir = None

    def __init__(self, x, y):
        self.lat, self.lat_dir = float(x[:-1]), x[-1]
        self.lon, self.lon_dir = float(y[:-1]), y[-1]


class Location(object):
    """
    Location range
    """
    round_off = 6
    cord = None

    def __init__(self, cord):
        self.cord = cord

    def get_range(self, range_buffer=config.LOCATION_BUFFER):
        cord = self.cord
        return {
            'lat': {
                'min': round(cord.lat - range_buffer, self.round_off),
                'max': round(cord.lat + range_buffer, self.round_off),
                'dir': cord.lat_dir
            },
            'lon': {
                'min': round(cord.lon - range_buffer, self.round_off),
                'max': round(cord.lon + range_buffer, self.round_off),
                'dir': cord.lon_dir
            }
        }
