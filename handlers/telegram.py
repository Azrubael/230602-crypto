import telebot
import os
from dotenv import load_dotenv  # $pip3 install python-dotenv


load_dotenv()
# SECURITY WARNING: keep the secret key used in production secret!
API_TOKEN = os.getenv('API_TOKEN')
BOT_NAME = os.getenv('BOT_NAME')


def send_notyfy(message):
    bot = telebot.TeleBot(API_TOKEN)
    bot.send_message(BOT_NAME, message)