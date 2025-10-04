from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, CallbackQueryHandler, filters
from services.weather_api import WeatherService

async def handle_city_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get('awaiting_city'):
        return
    
    city = update.message.text
    weather_data, error = WeatherService.get_weather_data(city)
    
    if error:
        await update.message.reply_text(f"Ошибка: {error}")
        return
    
    context.user_data['current_weather'] = weather_data
    context.user_data['awaiting_city'] = False
    
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

    await update.message.reply_text(f"Погода для {city}. Выберите параметр:", reply_markup=reply_markup)

async def handle_weather_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    weather_data = context.user_data.get('current_weather')
    if not weather_data:
        await query.edit_message_text("Данные о погоде не найдены. Начните заново командой /start")
        return
    
    text = WeatherService.format_weather_info(weather_data, query.data)
    await query.edit_message_text(text)

weather_input_handler = MessageHandler(
    filters.TEXT & ~filters.COMMAND, 
    handle_city_input
)
weather_button_handler = CallbackQueryHandler(handle_weather_button)
