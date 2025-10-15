import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

@dataclass
class BotConfig:
    token: str = os.getenv("BOT_TOKEN")
    weather_api_key: str = os.getenv("WEATHER_API_KEY")

    @classmethod
    def validate(cls):
        if not cls.token:
            raise ValueError("TOKEN not found")
        if not cls.weather_api_key:
            raise ValueError("WEATHER_API_KEY not found")
        return cls()
config = BotConfig.validate()
