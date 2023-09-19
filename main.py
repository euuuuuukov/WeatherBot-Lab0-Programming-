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


bot.polling(none_stop=1)
