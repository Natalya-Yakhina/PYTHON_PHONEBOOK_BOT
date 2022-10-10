# pip install python-telegram-bot - загрузить библиотеку

import logger as log
from settings import TOKEN
import json
import operator

from telegram import Bot, Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, ConversationHandler


bot = Bot(token='5783314859:AAH0yxtMbSfflc03SxZaxamMhOZoV_RjKr8')
updater = Updater(token='5783314859:AAH0yxtMbSfflc03SxZaxamMhOZoV_RjKr8')
dispatcher = updater.dispatcher

phone_number = {'id': 0, 'lastname': '', 'name': '', 'num': ''}
contact = []

LASTNAME, NAME, NUM, SEARCH, END_SEARCH, DEL_CONT, DEl_C, EDIT, EDITOR, EDIT_SURNAME, EDIT_NAME, EDIT_TEL, EDIT_COMMENT= range(13) # константы этапов разговоров 

ALL_FUNCTIONS = '/allcontact -- Список всех контактов\n' \
                '/addcontact-- Добавить контакт\n' \
                '/deletecontact -- Удалить контакт\n' \
                '/findcontact -- Найти контакт\n' \
                '/exporttojson -- Экспорт в json\n' \
                '/importfromjson -- Импорт из json\n '


tel_numb = {"id": 0, "surname": '', "name": '', "tel": '', "comment": ''}
contact = []

def entry():
    with open("phone_number.json", "w", encoding="utf-8") as tel:
        tel.write(json.dumps(phone_number, ensure_ascii=False))
        log.text_in_log('Сохранена телефонная книга')

def load():
    global contact
    log.text_in_log('Загружена телефонная книга')
    try:
        with open("contacts.json", "r", encoding="utf-8") as cont:
            contact = json.load(cont)
    except:
        contact = []

def add_contact(phone_number):
    try:
        load()
        temp = []
        ID = False
        for i in contact:
            temp.append(i["id"])
        while ID == False:
            if phone_number["id"] in temp:
                phone_number["id"] += 1
            else:
                ID = True
        contact.append(phone_number)
        sorted(contact, key=operator.itemgetter('lastname', 'name'))
        with open("contacts.json", "w", encoding="utf-8") as cont:
            cont.write(json.dumps(contact, ensure_ascii=False)) # dumps - сериализировывает obj в строку в формате JSON
        log.text_in_log(
            f"Добавлен контакт: {phone_number['lastname']} {phone_number['name']} {phone_number['num']}")
    except:
        contact.append(phone_number)
        with open("contacts.json", "w", encoding="utf-8") as cont:
            cont.write(json.dumps(contact, ensure_ascii=False))
        log.text_in_log(
            f"Добавлен контакт: {phone_number['lastname']} {phone_number['name']} {phone_number['num']}")

def start(update, context):
    context.bot.send_message(update.effective_chat.id, 'Добро пожаловать, я Бот-телефонный справочник🤓!\n'
                                                        'Я много чего умею:')
    context.bot.send_message(update.effective_chat.id, ALL_FUNCTIONS)
    log.text_in_log('---ЗАПУСК БОТА---')

# def start(update, _):
#     reply_keyboard = [['Создать контакт', 'Изменить контакт'], [
#         'Поиск', 'Все контакты'], ['Удалить все контакты', 'Удалить контакт']]
#     markup_key = ReplyKeyboardMarkup(
#         reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
#     update.message.reply_text(
#         'Слушаю',
#         reply_markup=markup_key,)

def cancel(update, _):
    log.text_in_log('---ВЫХОД---')
    update.message.reply_text('---ОТМЕНА---', reply_markup = ReplyKeyboardRemove())
    start(update, _)
    return ConversationHandler.END


# def message(update, context): 
#     text = update.message.text
#     if text.lower() == 'Привет':
#         context.bot.send_message(update.effective_chat.id, 'Добро пожаловать, я Бот-телефонный справочник🤓!\n'
#                                                             'Я много чего умею:')
#     else:
#         context.bot.send_message(update.effective_chat.id, 'Я Вас не понимаю, но могу что-то подскзать. Я много чего умею:')
#         context.bot.send_message(update.effective_chat.id, ALL_FUNCTIONS)

# def unknown(update, context):
#     context.bot.send_message(update.effective_chat.id, 'Такую команду я не знаю. Но вот что я умею:')
#     context.bot.send_message(update.effective_chat.id, ALL_FUNCTIONS)

def lastname(update, _):
    phone_number['lastname'] = (update.message.text).capitalize()
    entry()
    log.text_in_log(f'Введена фамилия: {update.message.text}')
    update.message.reply_text('Введите имя\n/cancel')
    return NAME

def name(update, _):
    phone_number['name'] = (update.message.text).capitalize()
    entry()
    log.text_in_log(f'Введено имя: {update.message.text}')
    update.message.reply_text('Введите номер телефона:')
    return NUM

def num(update, _):
    load()
    phone_number['num'] = update.message.text
    entry()
    log.text_in_log(f"Введён номер телефона: {update.message.text}")
    add_contact(phone_number)
    start(update, _)
    return ConversationHandler.END

def search(update, _):
    try:
        log.text_in_log('Запущен поиск')
        text = update.message.text
        reply_keyboard = [['Да', 'Нет']]
        markup_key = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
        temp = []
        load()
        for i in contact:
            if text.lower() in i['lastname'].lower() or text in i['name'].lower() or text in i['num']:
                temp.append(i)
        for i in temp:
            update.message.reply_text(
                f'{i["lastname"]} {i["name"]} {i["num"]}\n',
                reply_markup=markup_key,)
        if temp == []:
            update.message.reply_text(
                'Я не нашел такого!', reply_markup=markup_key,)
            log.text_in_log('Поиск не дал результатов')
        update.message.reply_text('Повторить поиск?\n/cancel')
        return END_SEARCH
    except:
        update.message.reply_text(
            'Что-то пошло не так')
        cancel(update, _)

def end_search(update, _): 
    try:
        text = update.message.text
        if text == 'Нет':
            log.text_in_log('Отмена повторного поиска')
            start(update, _)
            return ConversationHandler.END
        elif text == 'Да':
            log.text_in_log('Повторный поиск')
            update.message.reply_text('Введите данные для поиска\n/cancel')
            return SEARCH
    except:
        update.message.reply_text(
            'Что-то пошло не так')
        cancel(update, _)

def all_contacts(update, _):
    load()
    temp = ''
    if contact == []:
        log.text_in_log('Контакты отсуствуют')
        update.message.reply_text('Контакты отсуствуют')
    else:
        for i in contact:
            temp += f'{i["lastname"]} {i["name"]} {i["num"]}\n'
        update.message.reply_text(temp)
        log.text_in_log('Вывод всех контактов телефонной книги')
    start(update, _)


def del_cont(update, _):
    try:
        load()
        text = int(update.message.text) - 1
        temp = {}
        for i in contact:
            if text == i['id']:
                temp = i
        with open("tel_numb.json", "w", encoding="utf-8") as tel:
            tel.write(json.dumps(temp, ensure_ascii=False))
        reply_keyboard = [['Да', 'Нет']]
        markup_key = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
        update.message.reply_text(
            f'Удалить {temp["lastname"]} {temp["name"]}?\n/cancel', reply_markup=markup_key,)
        return DEl_C
    except:
        update.message.reply_text(
            'Что-то пошло не так')
        cancel(update, _)

def del_c(update, _):
    try:
        text = update.message.text
        if text == 'Да':
            load()
            with open("phone_number.json", "r", encoding="utf-8") as tel_n:
                tel_num = json.load(tel_n)
            for i in contact:
                if i == tel_num:
                    contact.remove(i)
            with open("contacts.json", "w", encoding="utf-8") as cont:
                cont.write(json.dumps(contact, ensure_ascii=False))
            log.text_in_log(
                f'Удалён контакт {phone_number["lastname"]} {phone_number["name"]}')
            update.message.reply_text('Готово')
            start(update, _)
        if text == 'Нет':
            cancel(update, _)
        return ConversationHandler.END
    except:
        update.message.reply_text(
            'Что-то пошло не так')
        cancel(update, _)

def editing(update, _):
    pass

def delete(update, _):
    pass

if __name__ == '__main__':
    updater = Updater(token = '5783314859:AAH0yxtMbSfflc03SxZaxamMhOZoV_RjKr8')
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    record_handler = ConversationHandler(
        entry_points = [MessageHandler(Filters.text, message)],
        states = {
            LASTNAME: [MessageHandler(Filters.text & ~Filters.command, lastname)],
            NAME: [MessageHandler(Filters.text & ~Filters.command, name)],
            NUM: [MessageHandler(Filters.text & ~Filters.command, num)]
            },
            fallbacks=[CommandHandler('cancel', cancel)],
    )

    base_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.text, message)],
        states = {
         ALL_CONTACTS: [MessageHandler(Filters.text & ~Filters.command, all_contacts)],
            DELETE: [MessageHandler(Filters.text & ~Filters.command, delete)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    message_handler = MessageHandler(Filters.text, message)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(record_handler)
dispatcher.add_handler(base_handler)
dispatcher.add_handler(message_handler)

print('server_started')

updater.start_polling()
updater.idle()