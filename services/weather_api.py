import requests
from config.settings import config

class WeatherService:
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    @classmethod
    def get_weather_data(cls, city):
        params = {
            "q": city,
            "units": "metric",
            "lang": "ru",
            "appid": config.weather_api_key
        }

        response = requests.get(cls.BASE_URL, params=params)
        data = response.json()

        return data, None
    
    @staticmethod
    def format_weather_info(weather_data, info_type):
        if info_type == "description":
            return f"Описание: {weather_data['weather'][0]['description']}"
        elif info_type == "temp":
            return f"Температура: {int(round(weather_data['main']['temp']))}°C"
        elif info_type == "clouds":
            return f"Облачность: {weather_data['clouds']['all']}%"
        elif info_type == "wind":
            return f"Ветер: {weather_data['wind']['speed']} м/с"
        elif info_type == "all":
            return (
                f"Погода в выбранном городе:\n"
                f"Описание: {weather_data['weather'][0]['description']}\n"
                f"Температура: {int(round(weather_data['main']['temp']))}°C\n"
                f"Ощущается как: {int(round(weather_data['main']['feels_like']))}°C\n"
                f"Влажность: {weather_data['main']['humidity']}%\n"
                f"Давление: {weather_data['main']['pressure']} hPa\n"
                f"Ветер: {weather_data['wind']['speed']} м/с\n"
                f"Облачность: {weather_data['clouds']['all']}%"
            )
