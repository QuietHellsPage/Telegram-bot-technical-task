import logging
from telegram.ext import Application

from config.settings import config
from handlers import (
    start_handler,
    weather_input_handler,
    weather_button_handler,
    help_handler
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def setup_application() -> Application:
    application = Application.builder().token(config.token).build()
    
    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(weather_input_handler)
    application.add_handler(weather_button_handler)
    
    return application

def main() -> None:
    try:
        application = setup_application()
        application.run_polling()
        
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
        raise

if __name__ == "__main__":
    main()
