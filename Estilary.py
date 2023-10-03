import telebot
from telebot import types
import os  # Добавьте этот импорт

# Получите токен из переменной окружения
BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Устанавливаем команды для бота
bot.set_my_commands([
    types.BotCommand("start", "Запустить бота")
])

# Создаем словарь для хранения данных пользователей
user_data = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    # Проверяем, есть ли информация о пользователе в словаре
    if user_id in user_data:
        user_name = user_data[user_id]['name']
        bot.send_message(chat_id, f"Добро пожаловать снова, {user_name}!")
        bot.send_message(chat_id, "Если у Вас есть вопросы по товару, обращайтесь в телеграмм @besmartshop_01.")
    else:
        bot.reply_to(message, "Здравствуйте!\n\nСпасибо за доверие к нашему бренду! Давайте знакомиться! Как вас зовут?")
        bot.register_next_step_handler(message, handle_name)

def handle_name(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_name = message.text.strip()
    user_data[user_id] = {'name': user_name, 'contact': None}
    
    # Отправляем персонализированное приветствие с именем пользователя
    bot.send_message(chat_id, f"Очень приятно, {user_name}. У нас есть для вас подарок.")
    bot.send_message(chat_id, "Мы не хотим быть одними из тех, кто отправляет пользователям сообщения, которых они не ожидают, поэтому, просим Вашего разрешения, чтобы вы поделились контактами с нами, "
                              "чтобы в будущем мы могли радовать вас специальными предложениями.\n\nЕсли вы не против поделиться номером телефона нажмите Поделиться номером телефона.\n\nЕсли вы готовы разрешить делиться с Вами специальными предложениями только через телеграмм нажмите Только телеграмм")
    request_contact_or_permission(chat_id)

def request_contact_or_permission(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item1 = types.KeyboardButton("Поделиться номером телефона", request_contact=True)
    item2 = types.KeyboardButton("Только Телеграмм")
    markup.add(item1, item2)
    bot.send_message(chat_id, "Пожалуйста, выберите один из вариантов ниже:",
                     reply_markup=markup)

@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_contact = message.contact.phone_number
    user_nickname = message.from_user.username
    
    # Обновляем данные пользователя
    user_data[user_id]['contact'] = user_contact
    
    # Записываем данные в текстовый файл
    with open('contacts.txt', 'a') as file:
        file.write(f"User ID: {user_id}, User Name: {user_data[user_id]['name']}, "
                   f"Phone Number: {user_contact}, User Nickname: {user_nickname}\n")
    
    # Отправляем PDF-файл
    with open('/Users/enot/Documents/ESTILARY/Surfing_Illustrated.pdf', 'rb') as pdf_file:
        bot.send_document(chat_id, pdf_file)
    
    # Отправляем сообщение благодарности
    bot.send_message(chat_id, "Спасибо, что Вы с нами, надеемся Вам будет интересно!")

@bot.message_handler(func=lambda message: message.text == "Только Телеграмм")
def handle_permission(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_nickname = message.from_user.username
    
    # Записываем никнейм пользователя в текстовый файл
    with open('contacts.txt', 'a') as file:
        file.write(f"User ID: {user_id}, User Name: {user_data[user_id]['name']}, "
                   f"User Nickname: {user_nickname}\n")
    
    # Отправляем PDF-файл
    with open('/Users/enot/Documents/ESTILARY/Surfing_Illustrated.pdf', 'rb') as pdf_file:
        bot.send_document(chat_id, pdf_file)
    
    # Отправляем сообщение благодарности
    bot.send_message(chat_id, "Спасибо, что Вы с нами, надеемся Вам будет интересно!")

# Запускаем бота
bot.infinity_polling()
