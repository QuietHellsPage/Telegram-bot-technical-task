from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Введите название города для получения погоды:")
    context.user_data['awaiting_city'] = True

start_handler = CommandHandler("start", start_command)
