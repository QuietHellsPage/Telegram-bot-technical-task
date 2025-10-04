from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
После команды /start введите название города, затем выберите параметр погоды из меню.
    """
    await update.message.reply_text(help_text)

help_handler = CommandHandler("help", help_command)
