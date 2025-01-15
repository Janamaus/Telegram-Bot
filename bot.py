from aiohttp import web
import telegram
from telegram.ext import Application, MessageHandler, filters

BOT_TOKEN = "7733972368:AAFl4oyP5S6Zea13GePBgG0ZLwv539qU0kA"

# Telegram-Bot initialisieren
application = Application.builder().token(BOT_TOKEN).build()

async def handle(request):
    # JSON-Daten vom Telegram-Webhook einlesen
    data = await request.json()
    update = telegram.Update.de_json(data, application.bot)
    await application.update_queue.put(update)
    return web.Response(text="ok")

# Handler hinzufügen
async def echo(update: telegram.Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat.id
    message = update.message.text
    await context.bot.send_message(chat_id=chat_id, text=f"Du hast gesagt: {message}")

application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# Webserver für Telegram-Webhook einrichten
app = web.Application()
app.router.add_post("/", handle)

if __name__ == "__main__":
    web.run_app(app, port=5000)
