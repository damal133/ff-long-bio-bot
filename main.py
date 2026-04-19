import telebot
import os

TOKEN = os.getenv("8372491245:AAETENEjfIFMPXKKy-KRrj4X_Bu4AkvThTE")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,"Welcome To Long Bio Bot 🥳")

bot.infinity_polling()
