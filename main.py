from telebot import TeleBot
from telebot import types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from requests import get
from json import loads
from googletrans import Translator, LANGCODES
from logging import basicConfig, getLogger, DEBUG


basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=DEBUG)
logger = getLogger(__name__)
TOKEN = '6058507940:AAEAb_bmD0lXXT_a742jKCXlHrYRfaGNsaI'
bot = TeleBot(TOKEN)
API_open_weather = 'c507bcf8971af71b550c3281cad1b275'
translator = Translator(service_urls=['translate.googleapis.com'])
langs_names = list(LANGCODES.keys())


@bot.message_handler(commands=['choose_lang'])
def choose_lang(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [KeyboardButton(language) for language in langs_names]
    for button in buttons:
        markup.add(button)
    bot.send_message(message.chat.id, f'Please choose your language or write in English', reply_markup=markup)


@bot.message_handler(commands=['start', 'menu'])
def start(message):
    username = ''
    if message.from_user.first_name:
        username += message.from_user.first_name
    if message.from_user.last_name:
        username += ' ' + message.from_user.last_name
    username = username.strip()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    weather_button = types.KeyboardButton('🏙 Выбор города')
    weather_location_button = types.KeyboardButton('🗺 Погода по геолокации')
    language_button = types.KeyboardButton('🇺🇸 Выбор языка')
    information_button = types.KeyboardButton('ℹ️ Информация')
    settings_button = types.KeyboardButton('🔧 Настройки')
    donate_button = types.KeyboardButton('💸 Поддержать проект')
    markup.add(weather_button, weather_location_button, language_button, information_button, settings_button, donate_button)
    bot.send_message(message.chat.id,
                     f'Привет, {username}! Я универсальный чат-бот для выдачи информации о '
                     f'погоде.\nВыбери то, что тебе нужно:', reply_markup=markup)




@bot.message_handler(func=lambda message: message.text == 'ℹ️ Информация')
def information(message):
    bot.send_message(message.chat.id, 'Данный бот создан группой разработчиков из России, представлен в более чем сотне языков мира.'
                                      '\nСоздан для выдачи информации о погоде в выбранных пользователями городах.'
                                      '\nНаписан на языке программирования Python c использованием библиотек:\nTelebot, json, requests, googletrans, loggging.')


@bot.message_handler(func=lambda message: message.text == '🏙 Выбор города')
def choose_city(message):
    bot.send_message(message.chat.id, f'Введите название города: ')


@bot.message_handler(func=lambda message: message.text.strip().lower() in langs_names)
def switch_lang(message):
    bot.send_message(message.chat.id, f'Your language: {message.text.strip().lower()}')


@bot.message_handler(func=lambda message: message.text == '💸 Поддержать проект')
def donate(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Поддержать', url = 'https://google.com'))
    bot.send_message(message.chat.id, 'Спасибо, что поддерживаете наш продукт, так мы станем лучше.', reply_markup=markup)
    


@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    result = get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_open_weather}&units=metric')
    if result.status_code == 200:
        data = loads(result.text)
        city = translator.translate(data['name'], src='en', dest='ru').text
        temp = data['main']['temp']
        real_temp = data['main']['feels_like']
        conditions = data['weather'][0]['description']
        pressure = data['main']['pressure']
        humidity = data['main']['humidity']
        bot.reply_to(message, f'Температура в городе {city}: {temp} °C, ощущается как {real_temp} °C\nПогодные условия: '
                              f'{conditions}\nДавление воздуха: {pressure} гПа\nВлажность воздуха: {humidity}%')
        if 'clear sky' in conditions:
            sticker_id = 'CAACAgIAAxkBAAEKWV9lC2QKSuI1rAHW6qA-v9CBnw00iQACOzYAAjVQYUjAUz1pjKjxtjAE'
        elif 'light rain' in conditions:
            sticker_id = 'CAACAgIAAxkBAAEKWS9lC1GI2grIW91nBQc7h4R2Iet8JwACPDcAAjTpUEiCyCmPfMIF2jAE'
        elif 'moderate rain' in conditions:
            sticker_id = 'CAACAgIAAxkBAAEKWTxlC1PpXf-hn28iQriymSDihXzIsAAC90AAAqfUWUilawirv5bpLzAE'
        elif 'heavy intensity rain' in conditions:
            sticker_id = 'CAACAgIAAxkBAAEKWS1lC1EWKMRvJ_pxkL3r3YZItnx28QACMzwAAtaTYEjjYaSA5JG9ZTAE'
        elif 'overcast clouds' in conditions or 'broken clouds' in conditions or 'scattered clouds' in conditions:
            sticker_id = 'CAACAgIAAxkBAAEKWSZlC0iq2_M72eEYRmnqB_tQr92KgQACsjkAAkdbWEhyZFRbA_1pHzAE'
        elif 'mist' in conditions or 'smoke' in conditions:
            sticker_id = 'CAACAgIAAxkBAAEKWFdlCvMgbEyu0ovY3RTLWljNlCQNsgACrTgAAq4lWUjCR7-2E9FdODAE'
        bot.send_sticker(message.chat.id, sticker_id)
    else:
        bot.send_message(message.chat.id, 'Название города некорректно')


@bot.message_handler(content_types=['audio', 'document', 'animation', 'game', 'photo', 'sticker', 'video', 'video_note', 'voice', 'contact', 'venue', 'dice', 'invoice', 'successful_payment', 'connected_website', 'poll', 'passport_data', 'web_app_data'])
def unknown_type(message):
    bot.reply_to(message, 'Я не определил вашу команду\nВведите <u>/start</u>, чтобы продолжить', parse_mode='html')


@bot.message_handler(content_types=['location'])
def location_type(message):
    bot.reply_to(message, 'Я не умею работать с геолокацией\nВведите <u>/start</u>, чтобы продолжить',
                 parse_mode='html')


bot.polling(none_stop=True)
