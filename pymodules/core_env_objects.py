from pymodules.location import Location


class APIDataCall(object):
    """
    Core Env objects
    """
    _instance = None
    _data = None

    def __init__(self, instance):
        if type(self._instance) != type(instance):
            APIDataCall._instance = instance

    @classmethod
    def load_api_data(cls, date, req_loc=True):
        if not APIDataCall._data:
            _, cls._data = cls._instance.fetch_data_by_location(date_min=date, req_loc=req_loc)

    def get_brightest_star(self, cord):
        """
        Method to find brightest star
        :param cord:
        :return:
        """
        maximum = None
        loc_range = Location(cord=cord).get_range()  # default=15

        for x in self._data['data']:
            lat = float(x[3])
            lat_dir = x[4]
            lon = float(x[5])
            lon_dir = x[6]

            if loc_range['lat']['min'] < lat <= loc_range['lat']['max'] and lat_dir == loc_range['lat']['dir'] and \
                    loc_range['lon']['min'] <= lon < loc_range['lon']['max'] and lon_dir == loc_range['lon']['dir']:
                if not maximum:
                    maximum = x
                    continue
                if float(maximum[1]) < float(x[1]):
                    maximum = x

        return maximum
