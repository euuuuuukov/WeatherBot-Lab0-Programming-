from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, Message
from requests import get, Response
from json import loads
from googletrans import Translator, LANGCODES
from logging import basicConfig, getLogger, DEBUG
from gspread import service_account


BOT_ID = '@cool_open_weather_bot'
sheet = service_account(filename='myproject-8ddc1-590114a2c317.json').\
    open_by_key('1Op679hovTIE1s8_OtI-hn9Ve37GKdOUjwQFL_IuCDUA').get_worksheet(0)

basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=DEBUG, filename='log.txt',
            filemode='w')
logger = getLogger(__name__)

TOKEN = '6483555277:AAG12TO9bnABk-XomnisbUgtvcFjtELd2hc'
bot = TeleBot(TOKEN)

API_open_weather = 'c507bcf8971af71b550c3281cad1b275'

translator = Translator(service_urls=['translate.googleapis.com'])
langs_names = list(LANGCODES.keys())


def get_weather(message: Message, result: Response) -> str:
    chat_id = message.chat.id
    lang = sheet.cell(sheet.find(str(chat_id)).row, 2).value
    if result.status_code == 200:
        data = loads(result.text)
        city = data['name']
        temp = round(data['main']['temp'])
        real_temp = round(data['main']['feels_like'])
        conditions = data['weather'][0]['description']
        pressure = round(data['main']['pressure'] * 0.75)
        humidity = data['main']['humidity']
        wind = round(data['wind']['speed'])
        bot.reply_to(message,
                     translator.translate(f'Now in {city}:\n🌡 Temperature: {temp} °C, feels like {real_temp} °C\n'
                                          f'↗️ Wind: {wind} m/s\n🌥 Weather conditions: {conditions}\n'
                                          f'⏲ Pressure: {pressure} millimeters of mercury\n💧 Humidity: {humidity}%',
                                          src='en', dest=lang).text)
        sticker_id = ''
        if conditions == 'clear sky':
            sticker_id = 'CAACAgIAAxkBAAEKWV9lC2QKSuI1rAHW6qA-v9CBnw00iQACOzYAAjVQYUjAUz1pjKjxtjAE'
        elif conditions == 'light rain':
            sticker_id = 'CAACAgIAAxkBAAEKWS9lC1GI2grIW91nBQc7h4R2Iet8JwACPDcAAjTpUEiCyCmPfMIF2jAE'
        elif conditions == 'moderate rain':
            sticker_id = 'CAACAgIAAxkBAAEKWTxlC1PpXf-hn28iQriymSDihXzIsAAC90AAAqfUWUilawirv5bpLzAE'
        elif conditions == 'heavy intensity rain':
            sticker_id = 'CAACAgIAAxkBAAEKWS1lC1EWKMRvJ_pxkL3r3YZItnx28QACMzwAAtaTYEjjYaSA5JG9ZTAE'
        elif conditions in ['broken clouds', 'scattered clouds', 'overcast clouds', 'few clouds']:
            sticker_id = 'CAACAgIAAxkBAAEKWSZlC0iq2_M72eEYRmnqB_tQr92KgQACsjkAAkdbWEhyZFRbA_1pHzAE'
        elif conditions in ['mist', 'smoke']:
            sticker_id = 'CAACAgIAAxkBAAEKWFdlCvMgbEyu0ovY3RTLWljNlCQNsgACrTgAAq4lWUjCR7-2E9FdODAE'
        bot.send_sticker(chat_id, sticker_id)
        return city
    else:
        bot.send_message(chat_id, translator.translate('The city name is incorrect, please enter again:', src='en',
                                                       dest=lang).text)


@bot.message_handler(commands=['start'])
def start(message: Message) -> None:
    username = ''
    if message.from_user.first_name:
        username += message.from_user.first_name
    if message.from_user.last_name:
        username += ' ' + message.from_user.last_name
    username = username.strip()
    chat_id = message.chat.id
    find_chat_id = sheet.find(str(chat_id))
    if not find_chat_id:
        sheet.add_rows(1)
        sheet.update_cell(sheet.row_count, 1, str(chat_id))
        sheet.update_cell(sheet.row_count, 2, 'en')
        lang = 'en'
    else:
        lang = sheet.cell(find_chat_id.row, 2).value
    menu_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    menu_markup.add(KeyboardButton(translator.translate('☁️ Weather in my city', src='en', dest=lang).text),
                    KeyboardButton(translator.translate('🏙 Weather in another city', src='en', dest=lang).text))
    menu_markup.add(KeyboardButton(translator.translate('🔧 Settings', src='en', dest=lang).text),
                    KeyboardButton(translator.translate('✍️ To write to the developers', src='en', dest=lang).text))
    menu_markup.add(KeyboardButton(translator.translate('💸 Support the project', src='en', dest=lang).text))
    bot.send_message(chat_id,
                     f'{translator.translate("Hello", src="en", dest=lang).text}, {username}! '
                     f'{translator.translate("By continuing to use the bot, you", src="en", dest=lang).text} '
                     f'<a href="https://docs.google.com/document/d/1Y8jrM_0F6xaME0gTi3hUVM7O6FSjxAIFiSFuyHFIt2E/edit?'
                     f'usp=sharing">'
                     f'{translator.translate("consent to the processing of personal data", src="en", dest=lang).text}'
                     f'</a>\n\n{translator.translate("Choose what you need:", src="en", dest=lang).text}',
                     reply_markup=menu_markup, parse_mode='HTML')


@bot.message_handler(commands=['menu'])
def menu(message: Message) -> None:
    chat_id = message.chat.id
    lang = sheet.cell(sheet.find(str(chat_id)).row, 2).value
    menu_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    menu_markup.add(KeyboardButton(translator.translate('☁️ Weather in my city', src='en', dest=lang).text),
                    KeyboardButton(translator.translate('🏙 Weather in another city', src='en', dest=lang).text))
    menu_markup.add(KeyboardButton(translator.translate('🔧 Settings', src='en', dest=lang).text),
                    KeyboardButton(translator.translate('✍️ Write to the developers', src='en', dest=lang).text))
    menu_markup.add(KeyboardButton(translator.translate('💸 Support the project', src='en', dest=lang).text))
    bot.send_message(chat_id, translator.translate('You are back to the menu!\nChoose what you need:', src='en',
                                                   dest=lang).text, reply_markup=menu_markup)


@bot.message_handler(func=lambda message: '☁️' in message.text)
def weather_in_my_city(message: Message) -> None:
    chat_id = message.chat.id
    coordinates = sheet.cell(sheet.find(str(chat_id)).row, 3).value
    lang = sheet.cell(sheet.find(str(chat_id)).row, 2).value
    menu_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    menu_markup.add(KeyboardButton(translator.translate('☁️ Weather in my city', src='en', dest=lang).text),
                    KeyboardButton(translator.translate('🏙 Weather in another city', src='en', dest=lang).text))
    menu_markup.add(KeyboardButton(translator.translate('🔧 Settings', src='en', dest=lang).text),
                    KeyboardButton(translator.translate('✍️ Write to the developers', src='en', dest=lang).text))
    menu_markup.add(KeyboardButton(translator.translate('💸 Support the project', src='en', dest=lang).text))
    if not coordinates:
        bot.send_message(chat_id, translator.translate('First you need to remember the city. You can do this in the '
                                                       'settings', src='en', dest=lang).text, reply_markup=menu_markup)
    else:
        result = get(
            f'https://api.openweathermap.org/data/2.5/weather?{coordinates}&appid={API_open_weather}&units=metric')
        get_weather(message, result)


@bot.message_handler(func=lambda message: '🏙' in message.text)
def weather_in_other_city(message: Message) -> None:
    chat_id = message.chat.id
    lang = sheet.cell(sheet.find(str(chat_id)).row, 2).value
    back_to_menu_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    back_to_menu_markup.add(KeyboardButton(translator.translate('📜🔙 Back to menu', src='en', dest=lang).text))
    bot.send_message(chat_id, translator.translate('Enter the name of the city:', src='en', dest=lang).text,
                     reply_markup=back_to_menu_markup)


@bot.message_handler(func=lambda message: '🇺🇸' in message.text)
def choose_lang(message: Message) -> None:
    chat_id = message.chat.id
    lang = sheet.cell(sheet.find(str(chat_id)).row, 2).value
    language_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    language_markup.add(KeyboardButton(translator.translate('🔧🔙 Back to settings', src='en', dest=lang).text))
    for language in langs_names:
        language_markup.add(KeyboardButton(language))
    bot.send_message(chat_id, f'Please choose your language or write in English', reply_markup=language_markup)


@bot.message_handler(func=lambda message: 'ℹ️' in message.text)
def information(message: Message) -> None:
    chat_id = message.chat.id
    lang = sheet.cell(sheet.find(str(chat_id)).row, 2).value
    settings_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    settings_markup.add(KeyboardButton(translator.translate('🗺 Remember the city by geolocation', src='en',
                                                            dest=lang).text, request_location=True))
    settings_markup.add(KeyboardButton(translator.translate('🇺🇸 Language selection', src='en', dest=lang).text),
                        KeyboardButton(translator.translate('ℹ️ Information', src='en', dest=lang).text))
    settings_markup.add(KeyboardButton(translator.translate('📜🔙 Back to menu', src='en', dest=lang).text))
    txt1 = translator.translate('This bot was created by a group of developers from Russia and is represented in more '
                                'than a hundred languages of the world.\nCreated to provide weather information in '
                                'cities selected by users.\nSupports working with user geolocation.\nWritten in the '
                                'Python programming language using the following libraries:', src='en', dest=lang).text
    txt2 = translator.translate('Developers contacts:', src='en', dest=lang).text
    bot.send_message(chat_id, f'{txt1}\ntelebot, json, requests, googletrans, logging.\n\n{txt2}\n<a '
                              f'href="https://t.me/tonnrryyy">Meshcheryakov Daniil</a>\n<a '
                              f'href="https://t.me/t_m_s_o_s_n">Kovalenko Evgeniy</a>\n<a href="https://t.me/yelotfn">'
                              f'Helm Daniil</a>', parse_mode='HTML', reply_markup=settings_markup)


@bot.message_handler(func=lambda message: '🔧' in message.text)
def settings(message: Message) -> None:
    chat_id = message.chat.id
    lang = sheet.cell(sheet.find(str(chat_id)).row, 2).value
    settings_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    settings_markup.add(KeyboardButton(translator.translate('🗺 Remember the city by geolocation', src='en',
                                                            dest=lang).text, request_location=True))
    settings_markup.add(KeyboardButton(translator.translate('🇺🇸 Language selection', src='en', dest=lang).text),
                        KeyboardButton(translator.translate('ℹ️ Information', src='en', dest=lang).text))
    settings_markup.add(KeyboardButton(translator.translate('📜🔙 Back to menu', src='en', dest=lang).text))
    bot.send_message(message.chat.id,
                     translator.translate('Select what you want to configure:', src='en', dest=lang).text,
                     reply_markup=settings_markup)


@bot.message_handler(func=lambda message: '💸' in message.text)
def donate(message: Message) -> None:
    chat_id = message.chat.id
    lang = sheet.cell(sheet.find(str(chat_id)).row, 2).value
    donate_markup = InlineKeyboardMarkup()
    donate_markup.add(InlineKeyboardButton(translator.translate('💸 Support', src='en', dest=lang).text,
                                           url='https://www.donationalerts.com/r/danoff28'))
    bot.send_message(message.chat.id, translator.translate('Thank you for supporting our product. This helps us become '
                                                           'better!', src='en', dest=lang).text,
                     reply_markup=donate_markup)


@bot.message_handler(func=lambda message: '✍️' in message.text)
def write(message: Message) -> None:
    chat_id = message.chat.id
    lang = sheet.cell(sheet.find(str(chat_id)).row, 2).value
    write_markup = InlineKeyboardMarkup()
    write_markup.add(InlineKeyboardButton(translator.translate('✍️ To write', src='en', dest=lang).text,
                                          url='https://forms.gle/4ET9KWs1Vqh3vZo37'))
    bot.send_message(message.chat.id, translator.translate('We are always happy to receive your suggestions. Thank you '
                                                           'for helping us become better!', src='en', dest=lang).text,
                     reply_markup=write_markup)


@bot.message_handler(func=lambda message: '📜🔙' in message.text)
def back_to_menu(message: Message) -> None:
    menu(message)


@bot.message_handler(func=lambda message: '🔧🔙' in message.text)
def back_to_settings(message: Message) -> None:
    settings(message)


@bot.message_handler(func=lambda message: message.text.strip().lower() in langs_names)
def switch_lang(message: Message) -> None:
    chat_id = message.chat.id
    sheet.update_cell(sheet.find(str(chat_id)).row, 2, LANGCODES[message.text])
    lang = sheet.cell(sheet.find(str(chat_id)).row, 2).value
    settings_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    settings_markup.add(KeyboardButton(translator.translate('🗺 To remember the city by geolocation', src='en',
                                                            dest=lang).text, request_location=True))
    settings_markup.add(KeyboardButton(translator.translate('🇺🇸 Language selection', src='en', dest=lang).text),
                        KeyboardButton(translator.translate('ℹ️ Information', src='en', dest=lang).text))
    settings_markup.add(KeyboardButton(translator.translate('📜🔙 Back to menu', src='en', dest=lang).text))
    bot.send_message(chat_id, f'Your language: {message.text.strip().lower()}',
                     reply_markup=settings_markup)


@bot.message_handler(content_types=['text'])
def text_type(message: Message) -> None:
    city = message.text.strip().lower()
    result = get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_open_weather}&units=metric')
    get_weather(message, result)


@bot.message_handler(content_types=['location'])
def location_type(message: Message) -> None:
    location = message.location
    lon, lat = location.longitude, location.latitude
    chat_id = message.chat.id
    sheet.update_cell(sheet.find(str(chat_id)).row, 3, f'lon={lon}&lat={lat}')
    result = get(f'https://api.openweathermap.org/data/2.5/weather?lon={lon}&lat='
                 f'{lat}&appid={API_open_weather}&units=metric')
    lang = sheet.cell(sheet.find(str(chat_id)).row, 2).value
    bot.send_message(message.chat.id,
                     translator.translate(f'We remembered your coordinates: {lon}, {lat}, '
                                          f'{get_weather(message, result)}.\nIf desired, you can always change them in '
                                          f'the same menu item', src='en', dest=lang).text)


@bot.message_handler(content_types=['audio', 'document', 'animation', 'game', 'photo', 'sticker', 'video', 'video_note',
                                    'voice', 'contact', 'venue', 'dice', 'invoice', 'successful_payment',
                                    'connected_website', 'poll', 'passport_data', 'web_app_data'])
def unknown_type(message: Message) -> None:
    chat_id = message.chat.id
    lang = sheet.cell(sheet.find(str(chat_id)).row, 2).value
    bot.send_message(message.chat.id, translator.translate('I did not recognize the data you entered😢', src='en',
                                                           dest=lang).text)


if __name__ == '__main__':
    bot.polling(none_stop=True)
