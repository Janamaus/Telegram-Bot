from flask import Flask, request
import telegram

# Flask-Server erstellen
app = Flask(__name__)

# Telegram-Bot initialisieren
BOT_TOKEN = "7733972368:AAFl4oyP5S6Zea13GePBgG0ZLwv539qU0kA"
bot = telegram.Bot(token=BOT_TOKEN)

@app.route("/", methods=["POST"])
def webhook():
    try:
        # Telegram-Update empfangen und parsen
        json_data = request.get_json(force=True)
        update = telegram.Update.de_json(json_data, bot)

        # Chat-ID und Nachricht extrahieren
        chat_id = update.message.chat.id
        message = update.message.text

        # Antwort senden
        bot.sendMessage(chat_id=chat_id, text=f"Du hast gesagt: {message}")
        print(f"Nachricht gesendet: {message} an {chat_id}")
    except Exception as e:
        print(f"Fehler: {e}")  # Fehler in den Logs anzeigen
    return "ok"

if __name__ == "__main__":
    app.run(port=5000)
