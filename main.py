import telebot

TOKEN = '6058507940:AAEAb_bmD0lXXT_a742jKCXlHrYRfaGNsaI'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'menu'])
def start(message):
    bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.first_name}, я универсальный чат-бот для выдачи информации о погоде.\nДля выдачи информации о погоде в городе введите его название.')

@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()




bot.polling(none_stop=1)
