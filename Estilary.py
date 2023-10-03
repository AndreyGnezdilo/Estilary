import telebot
from telebot import types
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

user_data = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    if user_id in user_data:
        bot.send_message(message.chat.id, "Рады что Вы с нами! Выберете интересующий Вас пункт меню.")
        show_main_menu(message.chat.id)
    else:
        greet_msg = "Привет! 👋\nСпасибо за покупку в нашем магазине! 🛍️\nДавайте знакомиться! Как вас зовут?"
        bot.send_message(message.chat.id, greet_msg)
        bot.register_next_step_handler(message, handle_name)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    user_id = message.from_user.id
    if user_id in user_data:
        bot.send_message(message.chat.id, "Рады что Вы с нами! Выберете интересующий Вас пункт меню.")
        show_main_menu(message.chat.id)

def handle_name(message):
    user_name = message.text
    user_id = message.from_user.id
    user_data[user_id] = user_name

    bot.send_message(message.chat.id, f"Какое красивое имя, {user_name}! Рады знакомству. 🥳")
    bot.send_message(message.chat.id, "У нас есть для вас подарок - электронная книга. Надеемся, вам понравится! 🎁")
    
    markup_gift = types.InlineKeyboardMarkup()
    btn_gift = types.InlineKeyboardButton("Забрать подарок 🎁", callback_data="get_gift")
    markup_gift.add(btn_gift)
    bot.send_message(message.chat.id, "Нажмите на кнопку ниже, чтобы забрать ваш подарок:", reply_markup=markup_gift)

@bot.callback_query_handler(func=lambda call: call.data == "get_gift")
def send_gift(call):
    with open('/Users/enot/Documents/ESTILARY/Surfing_Illustrated.pdf', 'rb') as book:
        bot.send_document(call.message.chat.id, book)
    
    markup_subscribe = types.InlineKeyboardMarkup()
    btn_subscribe = types.InlineKeyboardButton("Подписаться на канал 🚀", url="https://t.me/+RFGHFlCZT_kwZmNi")
    markup_subscribe.add(btn_subscribe)
    bot.send_message(call.message.chat.id, "Будем рады, если вы подпишитесь на наш телеграм-канал. Там мы публикуем информацию о новых коллекциях и предлагаем эксклюзивные скидки нашим покупателям. 🎉", reply_markup=markup_subscribe)
    
    markup_feedback = types.InlineKeyboardMarkup()
    btn_feedback = types.InlineKeyboardButton("Связаться с менеджером", url="https://t.me/besmartshop_01")
    markup_feedback.add(btn_feedback)
    bot.send_message(call.message.chat.id, "Если у вас есть вопросы по товару, нажмите на соответствующую кнопку:", reply_markup=markup_feedback)

def show_main_menu(chat_id):
    markup = types.InlineKeyboardMarkup()
    btn_gift = types.InlineKeyboardButton("Забрать подарок 🎁", callback_data="get_gift")
    btn_subscribe = types.InlineKeyboardButton("Подписаться на канал 🚀", url="https://t.me/+RFGHFlCZT_kwZmNi")
    btn_feedback = types.InlineKeyboardButton("Связаться с менеджером", url="https://t.me/besmartshop_01")
    markup.add(btn_gift)
    markup.add(btn_subscribe)
    markup.add(btn_feedback)
    bot.send_message(chat_id, "Выберите интересующий вас пункт:", reply_markup=markup)

bot.infinity_polling()
