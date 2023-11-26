import telebot
from telebot import types
import os

# Получение токена бота из переменной окружения
BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Приветствуем вас! 🎈 Благодарим за доверие и покупку продукции бренда ESTILARY! Мы приготовили для вас подарки — познавательные и увлекательные электронные книги. Уверены, они подарят вам приятные минуты чтения! 📖")
    bot.send_message(message.chat.id, "Надеемся, что вы остались довольны покупкой! Оставьте, пожалуйста, отзыв на Wildberries.")
    send_books(message)

def send_books(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_pdf = types.InlineKeyboardButton("PDF", callback_data='pdf')
    btn_epub = types.InlineKeyboardButton("EPUB", callback_data='epub')
    btn_fb2 = types.InlineKeyboardButton("FB2", callback_data='fb2')
    markup.add(btn_pdf, btn_epub, btn_fb2)

    bot.send_message(message.chat.id, "Выберите формат книги:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    bot.answer_callback_query(callback_query_id=call.id)

    if call.data == 'pdf':
        bot.send_document(call.message.chat.id, 'https://github.com/AndreyGnezdilo/Estilary/raw/main/books/Primachenko_O._Bestselleryisa._K_Sebe_Nejno_Kniga_O_Tom_.a6.pdf')
        bot.send_document(call.message.chat.id, 'https://github.com/AndreyGnezdilo/Estilary/raw/main/books/Rogov_A._Gid_Po_Stilyu.a6.pdf')
    elif call.data == 'epub':
        bot.send_document(call.message.chat.id, 'https://github.com/AndreyGnezdilo/Estilary/raw/main/books/Primachenko_O._Bestselleryisa._K_Sebe_Nejno_Kniga_O_Tom_.epub')
        bot.send_document(call.message.chat.id, 'https://github.com/AndreyGnezdilo/Estilary/raw/main/books/Rogov_A._Gid_Po_Stilyu.epub')
    elif call.data == 'fb2':
        bot.send_document(call.message.chat.id, 'https://github.com/AndreyGnezdilo/Estilary/raw/3ff7aa1dd84a120ade77d72c1bb2888cda6ddf11/books/Primachenko_O._Bestselleryisa._K_Sebe_Nejno_Kniga_O_Tom_.fb2')
        bot.send_document(call.message.chat.id, 'https://github.com/AndreyGnezdilo/Estilary/raw/3ff7aa1dd84a120ade77d72c1bb2888cda6ddf11/books/Rogov_A._Gid_Po_Stilyu.fb2')

    send_contact_option(call.message)

def send_contact_option(message):
    markup = types.InlineKeyboardMarkup()
    contact_button = types.InlineKeyboardButton("Связаться с менеджером", url="https://t.me/YOUR_TELEGRAM_ACCOUNT")
    markup.add(contact_button)
    bot.send_message(message.chat.id, "Если у вас есть какие-либо вопросы - напишите нам", reply_markup=markup)

bot.infinity_polling()
