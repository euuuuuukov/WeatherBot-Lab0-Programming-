import telebot
import requests
import json


TOKEN = '6058507940:AAEAb_bmD0lXXT_a742jKCXlHrYRfaGNsaI'
bot = telebot.TeleBot(TOKEN)
API_open_weather = 'c507bcf8971af71b550c3281cad1b275'

=======
from telebot import TeleBot

token = '6058507940:AAEAb_bmD0lXXT_a742jKCXlHrYRfaGNsaI'
bot = TeleBot(token)


@bot.message_handler(commands=['start', 'menu'])
def start(message):
    bot.send_message(message.chat.id,
                     f'Привет, {message.from_user.first_name}! Я универсальный чат-бот для выдачи информации о '
                     f'погоде.\nДля выдачи информации о погоде в городе введи его название:')


@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    result = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_open_weather}&units=metric')
    data = json.loads(result.text)
    temp = {data["main"]["temp"]
    bot.reply_to(message, f'Текущая температура в городе {city}: {temp} °C')


bot.polling(none_stop=1)
