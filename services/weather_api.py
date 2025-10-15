from datetime import datetime, timedelta

import requests

from config.settings import config


class WeatherService:
    BASE_URL = "https://api.openweathermap.org/data/2.5"

    @classmethod
    def _make_api_request(cls, endpoint, params):
        try:
            response = requests.get(
                f"{cls.BASE_URL}/{endpoint}", params=params, timeout=10
            )
            response.raise_for_status()
            return response.json(), None
        except requests.exceptions.RequestException as e:
            return None, f"Ошибка подключения: {e}"
        except ValueError as e:
            return None, f"Ошибка обработки данных: {e}"
        except Exception as e:
            return None, f"Неизвестная ошибка: {e}"

    @classmethod
    def get_current_weather(cls, city):
        params = {
            "q": city,
            "units": "metric",
            "lang": "ru",
            "appid": config.weather_api_key,
        }

        data, error = cls._make_api_request("weather", params)
        if error:
            return None, error

        if not isinstance(data, dict) or "main" not in data:
            return None, "Некорректный ответ от сервера"

        return data, None

    @classmethod
    def get_weather_forecast(cls, city, days=1):
        params = {
            "q": city,
            "units": "metric",
            "lang": "ru",
            "appid": config.weather_api_key,
            "cnt": days * 8,
        }

        data, error = cls._make_api_request("forecast", params)
        if error:
            return None, error

        if not isinstance(data, dict) or "list" not in data:
            return None, "Некорректный ответ от сервера"

        return data, None

    @staticmethod
    def format_weather_info(weather_data, info_type, is_forecast=False):
        try:
            if is_forecast:
                return WeatherService._format_forecast_info(weather_data, info_type)
            else:
                return WeatherService._format_current_weather_info(
                    weather_data, info_type
                )
        except (KeyError, IndexError, TypeError) as e:
            return f"Ошибка обработки данных: {e}"

    @staticmethod
    def _format_current_weather_info(weather_data, info_type):
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

    @staticmethod
    def _format_forecast_info(forecast_data, info_type):
        forecasts = forecast_data["list"]

        if info_type == "today":
            today_forecasts = [
                f
                for f in forecasts
                if datetime.fromtimestamp(f["dt"]).date() == datetime.now().date()
            ]
            if not today_forecasts:
                return "Нет данных на сегодня"

            result = "Прогноз на сегодня:\n"
            for forecast in today_forecasts:
                time = datetime.fromtimestamp(forecast["dt"]).strftime("%H:%M")
                temp = int(round(forecast["main"]["temp"]))
                desc = forecast["weather"][0]["description"]
                result += f"{time}: {temp}°C, {desc}\n"
            return result

        elif info_type == "tomorrow":
            tomorrow = datetime.now().date() + timedelta(days=1)
            tomorrow_forecasts = [
                f
                for f in forecasts
                if datetime.fromtimestamp(f["dt"]).date() == tomorrow
            ]
            if not tomorrow_forecasts:
                return "Нет данных на завтра"

            result = "Прогноз на завтра:\n"
            for forecast in tomorrow_forecasts:
                time = datetime.fromtimestamp(forecast["dt"]).strftime("%H:%M")
                temp = int(round(forecast["main"]["temp"]))
                desc = forecast["weather"][0]["description"]
                result += f"{time}: {temp}°C, {desc}\n"
            return result

        elif info_type == "forecast_all":
            result = "Прогноз на 3 дня:\n"
            current_date = None

            for forecast in forecasts[:10]:
                forecast_date = datetime.fromtimestamp(forecast["dt"]).strftime("%d.%m")
                forecast_time = datetime.fromtimestamp(forecast["dt"]).strftime("%H:%M")

                if forecast_date != current_date:
                    result += f"\n{forecast_date}:\n"
                    current_date = forecast_date

                temp = int(round(forecast["main"]["temp"]))
                desc = forecast["weather"][0]["description"]
                result += f"  {forecast_time}: {temp}°C, {desc}\n"

            return result
