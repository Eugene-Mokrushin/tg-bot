import time
import telebot
import config
import requests
import os
from telebot import types

bot = telebot.TeleBot(config.TOKEN)
Access = 'Not in'
Kate_key = 'pass'
Alex_key = 'pass'
test_key = 'pass'
current_folder = os.getcwd()
mixed = None
mixed_1 = None


@bot.message_handler(commands=['start'])
def welcome(message):
    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Ввести ключи")

    markup.add(item1)

    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}!\nЯ - 🤖<b>{1.first_name}</b>🤖\nЯ помогаю автоматезировать задачи, которые выполнял бы <b>мой создатель</b> много часов.\n\nЯ - общительный бот, и не люблю когда меня перебивают. Если я пишу, что я в работе - не нужно меня отвлекать новыми запросами😉".format(
                         message.from_user,
                         bot.get_me()),
                     parse_mode="html", reply_markup=markup)


@bot.message_handler(commands=['button'])
def options_ozon(message):
    if Access == 'In':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Остатки OZON")
        item2 = types.KeyboardButton("Цены OZON")
        item3 = types.KeyboardButton("Обновить DB OZON IDs")
        item4 = types.KeyboardButton("Выйти")
        markup.add(item1, item2, item3, item4)
        bot.send_message(message.chat.id, "Выберите что делать дельше", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Access denied")


def user_input(message):
    if message.text == Kate_key or message.text == Alex_key or message.text == test_key:
        global Access
        Access = 'In'
        bot.send_message(message.chat.id, 'Вход выполнен')
        options_ozon(message)

    elif message.text != Kate_key or message.text != Alex_key or message.text != test_key:
        bot.send_message(message.chat.id, 'Направильный ключ')
    else:
        bot.send_message(message.chat.id, 'Error')


@bot.message_handler(content_types=['text'])
def general(message):
    global Access, mixed, mixed_1
    if message.chat.type == 'private' and Access != 'In':
        if message.text == 'Ввести ключи':
            msg = bot.send_message(message.chat.id, 'Вводите ваш ключ')
            bot.register_next_step_handler(msg, user_input)
        elif message.text == 'Как дела?':
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Хорошо", callback_data='good')
            item2 = types.InlineKeyboardButton("Не очень", callback_data='bad')
            markup.add(item1, item2)
            bot.send_message(message.chat.id, 'Отлично как сам?', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Я не знаю что ответить попробуйте ввести /start')
    elif message.chat.type == 'private' and Access == 'In':
        if message.text == 'Выйти':
            Access = 'Not in'
            welcome(message)
        elif message.text == 'Остатки OZON':
            bot.send_message(message.chat.id,
                             "❗️❗️❗️Внимание❗️❗️❗️\nБот будет отключен на время - <b>30 секунд</b>\nИдет загрузка файла Сток - OZON🔄",
                             parse_mode='html')
            try:
                os.system(f'python {current_folder}/Parse_OZON.py')
                time.sleep(20)
            except requests.exceptions.MissingSchema:
                pass
            try:
                os.system(f'python {current_folder}/CSV_to_XLSX.py')
                time.sleep(4)
                os.system(f'python {current_folder}/Edit_parse_OZON_xlsx.py')
                time.sleep(4)
                bot.send_document(message.chat.id, open(rf'{current_folder}/Ozon_Data.xlsx', 'rb'))
                if os.path.exists(f'{current_folder}/Ozon_Data.csv'):
                    os.remove(f'{current_folder}/Ozon_Data.csv')
                    os.remove(f'{current_folder}/Ozon_Data.xlsx')
                else:
                    pass
            except FileNotFoundError:
                bot.send_message(message.chat.id,
                                 f'ОЗОН позволяет скачаивать файл раз в <b>5️⃣ минут!</b>',
                                 parse_mode='html')

        elif message.text == 'Цены OZON':
            bot.send_message(message.chat.id,
                             "❗️❗️❗️Внимание❗️❗️❗️\nБот будет отключен на время - <b>2 минуты</b>\nИдет загрузка файла Цен - OZON🔄",
                             parse_mode='html')
            try:
                os.system(f'python {current_folder}/Parse_OZON_price.py')
            except requests.exceptions.MissingSchema:
                pass

            try:
                bot.send_document(message.chat.id, open(rf'{current_folder}/Ozon_Data_Price.xlsx', 'rb'))
                if os.path.exists(f'{current_folder}/Ozon_Data_Price.xlsx'):
                    os.remove(f'{current_folder}/Ozon_Data_Price.xlsx')
                else:
                    pass
            except FileNotFoundError:
                bot.send_message(message.chat.id,
                                 f'ОЗОН позволяет скачаивать файл раз в <b>5️⃣ минут!</b>',
                                 parse_mode='html')

        elif message.text == 'Обновить DB OZON IDs':
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Продолжить", callback_data='continue')
            item2 = types.InlineKeyboardButton("Отменить", callback_data='stop')
            markup.add(item1, item2)
            bot.send_message(message.chat.id,
                             'Эта функция нужна для поддержки актуальности SKU для <i>отчета по ценам</i>. Если не нужно обновлять актуальность цен, нажмите <b>"Отмена"</b>',
                             reply_markup=markup, parse_mode='html')


@bot.message_handler(content_types=['text'])
def send_sad_capybara(message):
    sti = open('AnimatedSticker.tgs', 'rb')
    bot.send_sticker(message.chat.id, sti)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'continue':
                bot.send_message(call.message.chat.id,
                                 '❗️❗️❗️Внимание❗️❗️❗️\nБот будет отключен на время - <b>1,5 минуты</b>\nИдет загрузка файла Список SKU - OZON🔄',
                                 parse_mode='html')
                os.system(f'python {current_folder}/Update_DB_ids.py')
                bot.send_message(call.message.chat.id, '<b>Обновление выполнено</b> ✅', parse_mode='html')
            elif call.data == 'stop':
                bot.send_message(call.message.chat.id, '<b>Обновление отменено</b> ❌', parse_mode='html')

            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Хорошо",
                                  reply_markup=None)

            # show alert
            # bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
            #                           text="ЭТО ТЕСТОВОЕ УВЕДОМЛЕНИЕ!!11")

    except Exception as e:
        print(repr(e))


# RUN
bot.polling(none_stop=True)
