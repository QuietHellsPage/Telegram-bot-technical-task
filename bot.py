import logging

from telegram import Update
from telegram.ext import Application, ContextTypes

from config.settings import config
from handlers import (help_handler, start_handler, weather_button_handler,
                      weather_input_handler)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        logger.error(msg="Exception while handling an update:", exc_info=context.error)

        if update and update.effective_message:
            await update.effective_message.reply_text(
                "Произошла непредвиденная ошибка. "
                "Попробуйте выполнить команду еще раз или начните заново с команды /start"
            )
    except Exception as e:
        logger.error(f"Ошибка в обработчике ошибок: {e}")


def setup_application() -> Application:
    application = Application.builder().token(config.token).build()

    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(weather_input_handler)
    application.add_handler(weather_button_handler)

    application.add_error_handler(error_handler)

    return application


def main() -> None:
    logger.info("Начинаю работу...")
    application = setup_application()

    logger.info("Бот в процессе...")
    application.run_polling(drop_pending_updates=True, allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
