from pymodules.core_env_objects import APIDataCall
from pymodules.location import Coordinate
from pymodules.fireball_service_api import NasaFireballAPI
from pymodules.constant import VALID_LAT_DIR, VALID_LON_DIR
from pymodules.logger import logger

def fireball(lat, lon):
    """
    Fireball function to handle
    :param lat:
    :param lon:
    :return:
    """
    cord = Coordinate(lat, lon)
    assert lat[-1] in VALID_LAT_DIR , "Latitude Dir is not valid"
    assert lon[-1] in VALID_LON_DIR, "Longitude Dir is not valid"
    assert 0.00 < float(lat[0:-1]) <= 90.00, "Latitudes not in range from 0 to 90"
    assert 0.00 < float(lon[0:-1]) <= 180.00, "Longitude not in range from 0 to 180"

    obj = APIDataCall(NasaFireballAPI())
    obj.load_api_data(date="2017-01-01", req_loc=True)

    return obj.get_brightest_star(cord)


if __name__ == '__main__':

    response = (
        ('NCR', fireball(lat='28.574389N', lon='77.312638E')),
        ('BOSTON', fireball(lat='42.354558N', lon='71.054254W')),
        ('SAN FRANCISCO', fireball(lat='37.793700N', lon='122.403906W'))
    )

    for location in response:
        logger.info("** BRIGHTEST STAR POINT FOR {location} OFFICE ** : {coordinates}".format(
            location=location[0], coordinates=location[1]))

    m = response[0]
    for key, value in response[1:]:
        if float(m[1][1]) < float(value[1]):
            m = key, value

    logger.info("** BRIGHTEST STAR POINT AMONG THE THREE DELPHIX OFFICE LOCATION ** :"
                "{location} with coordinates as {coordinates}".format(location=m[0],coordinates=m[1]))
