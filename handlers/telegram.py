import telebot
from decouple import config  # pip3 install python-decouple


# SECURITY WARNING: keep the secret key used in production secret!
API_TOKEN = config('API_TOKEN')
CHAT_ID = config('CHAT_ID')


def send_notify(message):
    bot = telebot.TeleBot(API_TOKEN)
    bot.send_message(CHAT_ID, message)