import telebot

# Bot-Token
BOT_TOKEN = "7733972368:AAFl4oyP5S6Zea13GePBgG0ZLwv539qU0kA"
bot = telebot.TeleBot(BOT_TOKEN)

# Start-Befehl
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hallo! Ich bin dein persönlicher Assistent. Wie kann ich dir helfen?")

# Allgemeine Antworten
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"Du hast gesagt: {message.text}")

# Starte den Bot
if __name__ == "__main__":
    print("Bot läuft...")
    bot.polling()
  
