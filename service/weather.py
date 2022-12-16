import requests
import dataclasses


@dataclasses.dataclass
class WeatherData:
    name: str
    lat: float
    lon: float
    temp: float
    weather: str

    def to_dict(self):
        return dataclasses.asdict(self)


class Weather:
    _API_ID = 'c9430ab9659192f1970c4334ff927cc6'
    _API_URL = "http://api.openweathermap.org/data/2.5/find"

    @classmethod
    def _get_response(cls, city_name: str) -> dict | ValueError:
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
        data = WeatherData(
            name=data['name'],
            lat=data['coord']['lat'],
            lon=data['coord']['lon'],
            temp=data['main']['temp'],
            weather=data['weather'][0]['main']
        )
        return data

    @classmethod
    def get_weather(cls, city_name: str):
        weather_data = cls._get_response(city_name)
        response = cls._make_response(weather_data)
        return response