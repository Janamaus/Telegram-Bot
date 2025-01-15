from flask import Flask, request
import telegram

app = Flask(__name__)

BOT_TOKEN = "7733972368:AAFl4oyP5S6Zea13GePBgG0ZLwv539qU0kA"
bot = telegram.Bot(token=BOT_TOKEN)

@app.route("/", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    message = update.message.text
    bot.sendMessage(chat_id=chat_id, text=f"Du hast gesagt: {message}")
    return "ok"

if __name__ == "__main__":
    app.run(port=5000)
