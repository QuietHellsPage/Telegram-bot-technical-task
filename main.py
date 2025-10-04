import logging

import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (ApplicationBuilder, CallbackQueryHandler,
                          CommandHandler, ContextTypes, MessageHandler,
                          filters)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

current_weather_data = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_weather_data
    
    await update.message.reply_text("Введите название города для получения погоды:")
    
    context.user_data['awaiting_status'] = True


async def handle_city_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_weather_data
    
    if context.user_data.get('awaiting_status'):
        city = update.message.text
        link = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347"
        
        request = requests.get(link).json()
        if request.get("cod") != 200:
            await update.message.reply_text("Город не найден. Попробуйте еще раз.")
            return
            
        current_weather_data = request
            
        keyboard = [
            [
                InlineKeyboardButton("Описание", callback_data="description"),
                InlineKeyboardButton("Температура", callback_data="temp"),
            ],
            [
                InlineKeyboardButton("Облачность", callback_data="clouds"),
                InlineKeyboardButton("Ветер", callback_data="wind"),
            ],
            [InlineKeyboardButton("Вся информация", callback_data="all")],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(f"Выберите параметр:", reply_markup=reply_markup)
        context.user_data['awaiting_status'] = False


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_weather_data
    
    query = update.callback_query
    await query.answer()
    
    if not current_weather_data:
        await query.edit_message_text("Данные о погоде не найдены. Начните заново командой /start")
        return
    
    if query.data == "description":
        text = f"Описание: {current_weather_data['weather'][0]['description']}"
    elif query.data == "temp":
        text = f"Температура: {int(round(current_weather_data['main']['temp']))}°C"
    elif query.data == "clouds":
        text = f"Облачность: {current_weather_data['clouds']['all']}%"
    elif query.data == "wind":
        text = f"Ветер: {current_weather_data['wind']['speed']} м/с"
    elif query.data == "all":
        weather_info = current_weather_data
        text = (f"Погода в выбранном городе:\n"
                f"Описание: {weather_info['weather'][0]['description']}\n"
                f"Температура: {int(round(weather_info['main']['temp']))}°C\n"
                f"Ощущается как: {int(round(weather_info['main']['feels_like']))}°C\n"
                f"Влажность: {weather_info['main']['humidity']}%\n"
                f"Давление: {weather_info['main']['pressure']} hPa\n"
                f"Ветер: {weather_info['wind']['speed']} м/с\n"
                f"Облачность: {weather_info['clouds']['all']}%")
    
    await query.edit_message_text(text)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Напишите /start для начала работы с ботом")


def main():
    application = ApplicationBuilder().token("8450155826:AAEqV80Bz3HTAuPmAH6_HKF4Pu9Wk1U44Mk").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_city_input))
    application.add_handler(CallbackQueryHandler(button))
    application.run_polling()


if __name__ == "__main__":
    main()


