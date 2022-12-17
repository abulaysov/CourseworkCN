import requests
import dataclasses
from datetime import datetime


@dataclasses.dataclass
class WeatherData:
    """Класс для хранения данных в удобном формате"""
    name: str
    lat: float
    lon: float
    temp: float
    weather: str
    wind_speed: float
    wind_deg: float
    humidity: float
    last_update: str

    def to_dict(self):
        """Метод для преобразования дата-класса в словарь"""
        return dataclasses.asdict(self)


class Weather:
    """Класс для работы с API погоды
    Атрибуты:
        _API_ID - ключ от API, т.к. API приватный
        _API_URL - обычная ссылка для того, чтоб обращаться к нему
    """

    _API_ID = 'c9430ab9659192f1970c4334ff927cc6'
    _API_URL = "http://api.openweathermap.org/data/2.5/find"

    @classmethod
    def _get_response(cls, city_name: str) -> dict | ValueError:
        """Метод для выполнения запроса к API погоды, в случае если город
        не найден, то возбуждается исключение ValueError"""

        r = requests.get(cls._API_URL,
                         params={'q': city_name,
                                 'type': 'like',
                                 'units': 'metric',
                                 'APPID': cls._API_ID})

        data = r.json().get('list')
        if not any(data):
            raise ValueError
        return data[0]

    @classmethod
    def _make_response(cls, data: dict) -> WeatherData:
        """Метод для преобразования словаря в дата-класс"""
        data = WeatherData(
            name=data['name'],
            lat=data['coord']['lat'],
            lon=data['coord']['lon'],
            temp=data['main']['temp'],
            weather=data['weather'][0]['main'],
            wind_speed=data['wind']['speed'],
            wind_deg=data['wind']['deg'],
            humidity=data['main']['humidity'],
            last_update=str(datetime.now())[:19]
        )
        return data

    @classmethod
    def get_weather(cls, city_name: str) -> WeatherData:
        """Метод - который вызывает приватные методы для
        получения данных о погоде и возвращает полученные данные"""
        weather_data = cls._get_response(city_name)
        response = cls._make_response(weather_data)
        return response
