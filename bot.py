from flask import Flask, request
import telegram
import json

# Flask-Server erstellen
app = Flask(__name__)

# Telegram-Bot initialisieren
BOT_TOKEN = "DEIN_TELEGRAM_BOT_TOKEN"
bot = telegram.Bot(token=BOT_TOKEN)

# Erinnerungen laden und speichern
def load_memory():
    try:
        with open("memory.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_memory(memory):
    with open("memory.json", "w") as file:
        json.dump(memory, file, indent=4)

memory = load_memory()

@app.route("/", methods=["POST"])
def webhook():
    try:
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        chat_id = str(update.message.chat.id)  # ID als String für JSON-Kompatibilität
        message = update.message.text.strip()

        # **Kommandos**
        if message.lower().startswith("erinnere dich an:"):
            key = message.replace("Erinnere dich an:", "").strip()
            memory[chat_id] = memory.get(chat_id, [])  # Sicherstellen, dass ein Speicher existiert
            memory[chat_id].append(key)
            save_memory(memory)
            response = f"Nova hat sich das gemerkt: {key}"

        elif message.lower() == "was weißt du über mich?":
            user_memory = memory.get(chat_id, [])
            if user_memory:
                response = "Das weiß Nova über dich:\n- " + "\n- ".join(user_memory)
            else:
                response = "Nova hat noch keine Erinnerungen über dich gespeichert."

        else:
            response = f"Nova sagt: Du hast geschrieben: {message}"

        # Antwort senden
        bot.send_message(chat_id=chat_id, text=response)

    except Exception as e:
        print(f"Fehler: {e}")
        return "Fehler", 500
    return "ok"

if __name__ == "__main__":
    app.run(port=5000)
