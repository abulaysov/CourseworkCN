import geocoder


class Location:
    """Класс используется для получения текущей геопозиции клиента"""

    def __init__(self, loc='me'):
        """_request_geo - атрибут для получения данных о клиенте
           _current_get - атрибут для получения json формата данных о клиенте"""
        self._request_geo = geocoder.ip(loc)
        self._current_geo = self._request_geo.geojson

    def get_address(self):
        address = self._current_geo['features']
        address = address[0]['properties']['address']
        return address

    def get_city_name(self):
        city = self._current_geo['features']
        city = city[0]['properties']['city']
        return city

    def get_country(self):
        country = self._current_geo['features']
        country = country[0]['properties']['country']
        return country

    def get_ip(self):
        ip = self._current_geo['features']
        ip = ip[0]['properties']['ip']
        return ip

    def get_region(self):
        region = self._current_geo['features']
        region = region[0]['properties']['raw']['region']
        return region

    def get_loc(self):
        loc = self._current_geo['features']
        loc = loc[0]['properties']['raw']['loc']
        return loc

    def get_timezone(self):
        timezone = self._current_geo['features']
        timezone = timezone[0]['properties']['raw']['timezone']
        return timezone
