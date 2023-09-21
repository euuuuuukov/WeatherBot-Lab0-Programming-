import time
from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton,\
    ReplyKeyboardRemove
from requests import get
from json import loads
from googletrans import Translator, LANGCODES
from logging import basicConfig, getLogger, DEBUG
from sqlite3 import connect
import schedule
from schedule import every, repeat, run_pending
from pytz import timezone


basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=DEBUG)
logger = getLogger(__name__)
TOKEN = '6058507940:AAEAb_bmD0lXXT_a742jKCXlHrYRfaGNsaI'
bot = TeleBot(TOKEN)
API_open_weather = 'c507bcf8971af71b550c3281cad1b275'
translator = Translator(service_urls=['translate.googleapis.com'])
langs_names = list(LANGCODES.keys())


# @repeat(every().day.at('15:29', timezone('Europe/Moscow')))
def msg(message):
    bot.send_message(message.chat.id, 'Доброе утро, хотите узнать актуальную погоду?')


def get_weather(message, result):
    if result.status_code == 200:
        data = loads(result.text)
        city = translator.translate(data['name'], src='en', dest='ru').text
        temp = data['main']['temp']
        real_temp = data['main']['feels_like']
        conditions = data['weather'][0]['description']
        pressure = data['main']['pressure']
        humidity = data['main']['humidity']
        bot.reply_to(message,
                     f'Температура в городе {city}: {temp} °C, ощущается как {real_temp} °C\nПогодные условия: '
                     f'{conditions}\nДавление воздуха: {int(pressure/1.333)} мм. рт. столба\nВлажность воздуха: {humidity}%')
        if conditions == 'clear sky':
            sticker_id = 'CAACAgIAAxkBAAEKWV9lC2QKSuI1rAHW6qA-v9CBnw00iQACOzYAAjVQYUjAUz1pjKjxtjAE'
        elif conditions == 'light rain':
            sticker_id = 'CAACAgIAAxkBAAEKWS9lC1GI2grIW91nBQc7h4R2Iet8JwACPDcAAjTpUEiCyCmPfMIF2jAE'
        elif conditions == 'moderate rain':
            sticker_id = 'CAACAgIAAxkBAAEKWTxlC1PpXf-hn28iQriymSDihXzIsAAC90AAAqfUWUilawirv5bpLzAE'
        elif conditions == 'heavy intensity rain':
            sticker_id = 'CAACAgIAAxkBAAEKWS1lC1EWKMRvJ_pxkL3r3YZItnx28QACMzwAAtaTYEjjYaSA5JG9ZTAE'
        elif conditions in ['broken clouds', 'scattered clouds', 'overcast clouds']:
            sticker_id = 'CAACAgIAAxkBAAEKWSZlC0iq2_M72eEYRmnqB_tQr92KgQACsjkAAkdbWEhyZFRbA_1pHzAE'
        elif conditions in ['mist', 'smoke']:
            sticker_id = 'CAACAgIAAxkBAAEKWFdlCvMgbEyu0ovY3RTLWljNlCQNsgACrTgAAq4lWUjCR7-2E9FdODAE'
        bot.send_sticker(message.chat.id, sticker_id)
    else:
        bot.send_message(message.chat.id, 'Название города некорректно')


@bot.message_handler(commands=['start', 'menu'])
def menu(message):
    username = ''
    if message.from_user.first_name:
        username += message.from_user.first_name
    if message.from_user.last_name:
        username += ' ' + message.from_user.last_name
    username = username.strip()
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    weather_button = KeyboardButton('🏙 Выбор города')
    weather_location_button = KeyboardButton('🗺 Погода по геолокации', request_location=True)
    language_button = KeyboardButton('🇺🇸 Выбор языка')
    information_button = KeyboardButton('ℹ️ Информация')
    settings_button = KeyboardButton('🔧 Настройки')
    donate_button = KeyboardButton('💸 Поддержать проект')
    write_button = KeyboardButton('✍️ Написать разработчикам')
    markup.add(weather_button, weather_location_button, language_button, information_button, settings_button,
               donate_button, write_button)
    bot.send_message(message.chat.id,
                     f'Привет, {username}! Я универсальный чат-бот для выдачи информации о погоде.\n'
                     f'Выбери то, что тебе нужно:', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == '🏙 Выбор города')
def choose_city(message):
    bot.send_message(message.chat.id, f'Введите название города: ')


@bot.message_handler(func=lambda message: message.text == '🗺 Погода по геолокации')
def weather_by_location(message):
    pass



@bot.message_handler(func=lambda message: message.text == '🇺🇸 Выбор языка')
def choose_lang(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [KeyboardButton(language) for language in langs_names]
    for button in buttons:
        markup.add(button)
    bot.send_message(message.chat.id, f'Please choose your language or write in English', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'ℹ️ Информация')
def information(message):
    bot.send_message(message.chat.id,
                     'Данный бот создан группой разработчиков из России, представлен в более чем сотне языков мира.\n'
                     'Создан для выдачи информации о погоде в выбранных пользователями городах.\n'
                     'Написан на языке программирования Python c использованием следующих библиотек:\n'
                     'telebot, json, requests, googletrans, logging.')


@bot.message_handler(func=lambda message: message.text == '🔧 Настройки')
def settings(message):
    pass


@bot.message_handler(func=lambda message: message.text == '💸 Поддержать проект')
def donate(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Поддержать', url='https://google.com'))
    bot.send_message(message.chat.id, 'Спасибо, что поддерживаете наш продукт, так мы станем лучше.',
                     reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == '✍️ Написать разработчикам')
def donate(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Написать', url='https://forms.gle/4ET9KWs1Vqh3vZo37'))
    bot.send_message(message.chat.id, 'Мы всегда рады вашим предложениям. Спасибо, что помогаете нам стать лучше!',
                     reply_markup=markup)


@bot.message_handler(func=lambda message: message.text.strip().lower() in langs_names)
def switch_lang(message):
    bot.send_message(message.chat.id, f'Your language: {message.text.strip().lower()}')


@bot.message_handler(content_types=['text'])
def text_type(message):
    city = message.text.strip().lower()
    result = get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_open_weather}&units=metric')
    get_weather(message, result)


@bot.message_handler(content_types=['location'])
def location_type(message):
    location = message.location
    print(location)
    result = get(f'https://api.openweathermap.org/data/2.5/weather?lon={location.longitude}&lat='
                 f'{location.latitude}&appid={API_open_weather}&units=metric')
    get_weather(message, result)


@bot.message_handler(content_types=['audio', 'document', 'animation', 'game', 'photo', 'sticker', 'video', 'video_note', 'voice',
                   'contact', 'venue', 'dice', 'invoice', 'successful_payment', 'connected_website', 'poll',
                   'passport_data', 'web_app_data'])
def unknown_type(message):
    bot.reply_to(message, 'Я не распознал введенные вами данные😢\nВведи /start, чтобы продолжить', parse_mode='html')




bot.polling(none_stop=True)
schedule.every().day.at('15:31', timezone('Europe/Moscow')).do(msg)
while True:
    schedule.run_pending()
    time.sleep(1)
