import json
from service.weather import WeatherData


def make_response(data: WeatherData) -> json.dumps:
    """Функция используется для преобразования объектов python в json формат,
    для того чтоб передать клиенту"""
    return json.dumps(data.to_dict())
