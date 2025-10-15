from telegram import Update
from telegram.ext import CommandHandler, ContextTypes


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data.clear()
        context.user_data["awaiting_city"] = True

        welcome_text = """
**Добро пожаловать в бот погоды!**

Введите название города на русском или английском языке с большой буквы.


После ввода города вы сможете выбрать период времени и параметры погоды для просмотра.
        """
        await update.message.reply_text(welcome_text)

    except Exception as e:
        await update.message.reply_text("Произошла ошибка при запуске бота")


start_handler = CommandHandler("start", start_command)
