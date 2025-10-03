import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Stub")


if __name__ == "__main__":
    application = ApplicationBuilder().token("").build()
    handler = CommandHandler("start", start)
    application.add_handler(handler=handler)
    application.run_polling()