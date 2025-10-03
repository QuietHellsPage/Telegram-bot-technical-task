import logging

from telegram import Update
from telegram.ext import (ApplicationBuilder, CommandHandler, ContextTypes,
                          MessageHandler, filters)

import requests
import json

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Stub")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def show_weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    link = f"https://api.openweathermap.org/data/2.5/weather?q={update.message.text}&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347"
    request = requests.get(link).json()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=request["weather"][0]["description"])


if __name__ == "__main__":
    application = ApplicationBuilder().token("PASTE TOKEN").build()
    handler = CommandHandler("start", start)
    weather_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), show_weather)
    application.add_handler(handler=handler)
    application.add_handler(handler=weather_handler)
    application.run_polling()
