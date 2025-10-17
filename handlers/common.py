from telegram import Update
from telegram.ext import CommandHandler, ContextTypes


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        help_text = """
**Помощь по боту погоды**

**Основные команды:**
/start - Начать работу с ботом
/help - Помощь по использованию бота

**Как использовать:**
1. Нажмите /start
2. Введите название города
3. Выберите период времени:
   - 📊 Сейчас - текущая погода с детальной информацией
   - 📅 Сегодня - прогноз на сегодня по часам
   - 📆 Завтра - прогноз на завтра
   - 🗓️ 2 дня - прогноз на 2 дня

**Для текущей погоды доступны:**
- Описание погоды
- Температура
- Облачность
- Ветер
- Вся информация

Если у Вас возникли проблемы, попробуйте начать заново с /start
        """
        await update.message.reply_text(help_text)
    except Exception as e:
        await update.message.reply_text("Произошла ошибка при показе справки")


help_handler = CommandHandler("help", help_command)
