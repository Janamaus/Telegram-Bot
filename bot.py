from flask import Flask, request
import telegram
import json

# Flask-Server erstellen
app = Flask(__name__)

# Telegram-Bot initialisieren
BOT_TOKEN = "7733972368:AAFl4oyP5S6Zea13GePBgG0ZLwv539qU0kA"
bot = telegram.Bot(token=BOT_TOKEN)

# Speicher für Erinnerungen (vorerst in einer Datei)
def load_memory():
    try:
        with open("memory.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_memory(memory):
    with open("memory.json", "w") as file:
        json.dump(memory, file)

memory = load_memory()

@app.route("/", methods=["POST"])
def webhook():
    try:
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        chat_id = update.message.chat.id
        message = update.message.text

        # Erinnerungen speichern oder abrufen
        if message.startswith("Erinnere dich an:"):
            key = message.replace("Erinnere dich an:", "").strip()
            memory[chat_id] = key
            save_memory(memory)
            bot.send_message(chat_id=chat_id, text=f"Ich habe mir das gemerkt: {key}")
        elif message == "Was weißt du über mich?":
            key = memory.get(chat_id, "Ich habe noch keine Erinnerungen für dich.")
            bot.send_message(chat_id=chat_id, text=f"Ich weiß über dich: {key}")
        else:
            bot.send_message(chat_id=chat_id, text=f"Du hast gesagt: {message}")

    except Exception as e:
        print(f"Fehler: {e}")
        return "Fehler", 500
    return "ok"

if __name__ == "__main__":
    app.run(port=5000)
