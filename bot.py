from flask import Flask, request
import telegram
import asyncio

# Flask-Server erstellen
app = Flask(__name__)

# Telegram-Bot initialisieren
BOT_TOKEN = "7733972368:AAFl4oyP5S6Zea13GePBgG0ZLwv539qU0kA"
bot = telegram.Bot(token=BOT_TOKEN)

@app.route("/", methods=["POST"])
def webhook():
    try:
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        chat_id = update.message.chat.id
        message = update.message.text

        # Antwort senden - async verwenden
        asyncio.run(send_message(chat_id, message))
    except Exception as e:
        print(f"Fehler: {e}")  # Fehler in den Logs anzeigen
    return "ok"

async def send_message(chat_id, message):
    await bot.send_message(chat_id=chat_id, text=f"Du hast gesagt: {message}")

if __name__ == "__main__":
    app.run(port=5000)
