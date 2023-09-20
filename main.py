from requests import get
from json import loads
from googletrans import Translator


TOKEN = '6058507940:AAEAb_bmD0lXXT_a742jKCXlHrYRfaGNsaI'
bot = TeleBot(TOKEN)
API_open_weather = 'c507bcf8971af71b550c3281cad1b275'
translator = Translator(service_urls=['translate.googleapis.com'])


@bot.message_handler(commands=['start', 'menu'])
def start(message):
    bot.send_message(message.chat.id,
                     f'Привет, {message.from_user.first_name}! Я универсальный чат-бот для выдачи информации о '
                     f'погоде.\nДля выдачи информации о погоде в городе введи его название:')


@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    result = get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_open_weather}&units=metric')
    if result.status_code == 200:
        data = loads(result.text)
        city = translator.translate(data['name'], src='en', dest='ru').text
        bot.reply_to(message, str(data))
        temp = data['main']['temp']
        real_temp = data['main']['feels_like']
        conditions = data['weather'][0]['description']
        pressure = data['main']['pressure']
        humidity = data['main']['humidity']
        bot.reply_to(message, f'Температура в городе {city}: {temp} °C, ощущается как {real_temp} °C\nПогодные условия: '
                              f'{conditions}\nДавление воздуха: {pressure} гПа\nВлажность воздуха: {humidity}%')

        if 'clear sky' in conditions:
            pass
        elif 'overcast clouds' or 'broken clouds' in conditions:
            sticker_id = 'CAACAgIAAxkBAAEKV6hlCq3vKl9aENBE-nV6p3Ux2HfLJQACsjkAAkdbWEhyZFRbA_1pHzAE'
        elif 'light rain' or 'heavy intensity rain' in conditions:
            sticker_id = 'CAACAgIAAxkBAAEKV6dlCq3vSUfbjF7Fbieuz8Kq0uyVdgACPDcAAjTpUEiCyCmPfMIF2jAE'
        elif 'mist' in conditions:
            sticker_id = 'CAACAgIAAxkBAAEKWFdlCvMgbEyu0ovY3RTLWljNlCQNsgACrTgAAq4lWUjCR7-2E9FdODAE'
        bot.send_sticker(message.chat.id, sticker_id)
    else:
        bot.send_message(message.chat.id, 'Название города некорректно')


bot.polling(none_stop=True)
