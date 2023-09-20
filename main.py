import telebot
import requests
import json


TOKEN = '6058507940:AAEAb_bmD0lXXT_a742jKCXlHrYRfaGNsaI'
bot = telebot.TeleBot(TOKEN)
API_open_weather = 'c507bcf8971af71b550c3281cad1b275'

@bot.message_handler(commands=['start', 'menu'])
def start(message):
    bot.send_message(message.chat.id,
                     f'Привет, {message.from_user.first_name}! Я универсальный чат-бот для выдачи информации о '
                     f'погоде.\nДля выдачи информации о погоде в городе введи его название:')


@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    result = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_open_weather}&units=metric')
    if result.status_code == 200:
        data = json.loads(result.text)
        temp = data["main"]["temp"]
        conditions = data["weather"][0]["description"]
        pressure = data["main"]["pressure"]
        humidity = data["main"]["humidity"]
        bot.reply_to(message, f'Температура в городе {city}: {temp} °C\nПогодные условия: {conditions}\nДавление воздуха: {pressure} гПа\nВлажность воздуха: {humidity}%')

        if 'clear sky' in conditions:
            file = open('sunny.png', 'rb')
            bot.send_photo(message.chat.id, file)
        elif 'overcast clouds' or 'broken clouds' in conditions:
            # file = open('clouds.png', 'rb')
            # bot.send_photo(message.chat.id, file)
            bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEKV6hlCq3vKl9aENBE-nV6p3Ux2HfLJQACsjkAAkdbWEhyZFRbA_1pHzAE')
        elif 'light rain' or 'heavy intensity rain' in conditions:
            bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEKV6dlCq3vSUfbjF7Fbieuz8Kq0uyVdgACPDcAAjTpUEiCyCmPfMIF2jAE')
        elif 'mist' in conditions:
            bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEKWFdlCvMgbEyu0ovY3RTLWljNlCQNsgACrTgAAq4lWUjCR7-2E9FdODAE')
    else:
        bot.send_message(message.chat.id, 'Название города некорректно')


bot.polling(none_stop=1)
