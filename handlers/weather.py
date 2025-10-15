from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, CallbackQueryHandler, filters
from services.weather_api import WeatherService

async def handle_city_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not context.user_data.get('awaiting_city'):
            await update.message.reply_text(
                "Начните общение с команды /start"
            )
            return
        
        city = update.message.text.strip()
        
        if not city:
            await update.message.reply_text("Пожалуйста, введите название города")
            return
        
        if len(city) > 50:
            await update.message.reply_text("Название города слишком длинное. Попробуйте снова.")
            return
        
        await update.message.reply_text("Получаю данные о погоде...")
        
        weather_data, error = WeatherService.get_current_weather(city)
        
        if error:
            await update.message.reply_text(f"Ошибка: {error}\nПопробуйте другой город.")
            context.user_data['awaiting_city'] = False
            return
        
        context.user_data['current_city'] = city
        context.user_data['current_weather'] = weather_data
        context.user_data['awaiting_city'] = False
        
        keyboard = [
            [
                InlineKeyboardButton("📊 Сейчас", callback_data="time_current"),
                InlineKeyboardButton("📅 Сегодня", callback_data="time_today"),
            ],
            [
                InlineKeyboardButton("📆 Завтра", callback_data="time_tomorrow"),
                InlineKeyboardButton("🗓️ 3 дня", callback_data="time_forecast"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            f"Город: {city}. Выберите период времени:",
            reply_markup=reply_markup
        )
        
    except Exception as e:
        await update.message.reply_text("Произошла непредвиденная ошибка. Попробуйте снова.")

async def handle_weather_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        query = update.callback_query
        await query.answer()
        
        city = context.user_data.get('current_city')
        if not city:
            await query.edit_message_text("Город не найден. Начните заново с команды /start")
            return
        
        callback_data = query.data

        if callback_data.startswith('time_'):
            await _handle_time_selection(query, context, callback_data, city)
        elif callback_data in ["description", "temp", "clouds", "wind", "all"]:
            await _handle_weather_detail(query, context, callback_data)
        else:
            await query.edit_message_text("Неизвестная команда")
            
    except Exception as e:
        await query.edit_message_text("Произошла ошибка при обработке запроса")

async def _handle_time_selection(query, context, callback_data, city):
    try:
        if callback_data == "time_current":
            weather_data = context.user_data.get('current_weather')
            if not weather_data:
                weather_data, error = WeatherService.get_current_weather(city)
                if error:
                    await query.edit_message_text(f"Ошибка: {error}")
                    return
                context.user_data['current_weather'] = weather_data
            
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
                [InlineKeyboardButton("◀️ Назад", callback_data="back_to_time")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            temp = int(round(weather_data['main']['temp']))
            desc = weather_data['weather'][0]['description']
            await query.edit_message_text(
                f"Погода в {city} сейчас:\n{temp}°C, {desc}\nВыберите параметр:",
                reply_markup=reply_markup
            )
            
        elif callback_data == "time_today":
            await query.edit_message_text("Получаю прогноз на сегодня...")
            forecast_data, error = WeatherService.get_weather_forecast(city, days=1)
            if error:
                await query.edit_message_text(f"Ошибка: {error}")
                return
                
            text = WeatherService.format_weather_info(forecast_data, "today", is_forecast=True)
            keyboard = [[InlineKeyboardButton("◀️ Назад", callback_data="back_to_time")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text, reply_markup=reply_markup)
            
        elif callback_data == "time_tomorrow":
            await query.edit_message_text("Получаю прогноз на завтра...")
            forecast_data, error = WeatherService.get_weather_forecast(city, days=2)
            if error:
                await query.edit_message_text(f"Ошибка: {error}")
                return
                
            text = WeatherService.format_weather_info(forecast_data, "tomorrow", is_forecast=True)
            keyboard = [[InlineKeyboardButton("◀️ Назад", callback_data="back_to_time")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text, reply_markup=reply_markup)
            
        elif callback_data == "time_forecast":
            await query.edit_message_text("Получаю прогноз на 5 дней...")
            forecast_data, error = WeatherService.get_weather_forecast(city, days=5)
            if error:
                await query.edit_message_text(f"Ошибка: {error}")
                return
                
            text = WeatherService.format_weather_info(forecast_data, "forecast_all", is_forecast=True)
            keyboard = [[InlineKeyboardButton("◀️ Назад", callback_data="back_to_time")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text, reply_markup=reply_markup)
            
        elif callback_data == "back_to_time":
            keyboard = [
                [
                    InlineKeyboardButton("📊 Сейчас", callback_data="time_current"),
                    InlineKeyboardButton("📅 Сегодня", callback_data="time_today"),
                ],
                [
                    InlineKeyboardButton("📆 Завтра", callback_data="time_tomorrow"),
                    InlineKeyboardButton("🗓️ 3 дня", callback_data="time_forecast"),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                f"Город: {city}. Выберите период времени:",
                reply_markup=reply_markup
            )
            
    except Exception as e:
        await query.edit_message_text("Ошибка при получении данных о погоде")

async def _handle_weather_detail(query, context, callback_data):
    try:
        weather_data = context.user_data.get('current_weather')
        if not weather_data:
            await query.edit_message_text("Данные о погоде не найдены. Начните заново командой /start")
            return
        
        text = WeatherService.format_weather_info(weather_data, callback_data)
        keyboard = [[InlineKeyboardButton("◀️ Назад", callback_data="time_current")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)
        
    except Exception as e:
        await query.edit_message_text("Ошибка при форматировании данных о погоде")

weather_input_handler = MessageHandler(
    filters.TEXT & ~filters.COMMAND, 
    handle_city_input
)
weather_button_handler = CallbackQueryHandler(handle_weather_button)
