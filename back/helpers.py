import json
from service.weather import WeatherData


def make_response(data: WeatherData) -> json.dumps:
    return json.dumps(data.to_dict())
