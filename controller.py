# pip install python-telegram-bot - загрузить библиотеку

from telegram import Update, Bot, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, ConversationHandler
import json
import logger as log

bot = Bot(token='5783314859:AAH0yxtMbSfflc03SxZaxamMhOZoV_RjKr8')
updater = Updater(token='5783314859:AAH0yxtMbSfflc03SxZaxamMhOZoV_RjKr8')
dispatcher = updater.dispatcher

phone_number = {'id': 0, 'lastname': '', 'name': '', 'num': ''}
contact = []

LASTNAME, NAME, NUM = range(3) # константы этапов разговоров 

ALL_CONTACTS, DELETE = range(2)

ALL_FUNCTIONS = '/allcontact -- Список всех контактов\n' \
                '/addcontact-- Добавить контакт\n' \
                '/deletecontact -- Удалить контакт\n' \
                '/findcontact -- Найти контакт\n' \
                '/exporttojson -- Экспорт в json\n' \
                '/importfromjson -- Импорт из json\n '

def start(update, context):
    context.bot.send_message(update.effective_chat.id, 'Добро пожаловать, я Бот-телефонный справочник🤓!\n'
                                                        'Я много чего умею:')
    context.bot.send_message(update.effective_chat.id, ALL_FUNCTIONS)
    log.text_in_log('---ЗАПУСК БОТА---')

def cancel(update, _):
    log.text_in_log('---ВЫХОД---')
    update.message.reply_text('Отмена записи',reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def message(update, context): 
    text = update.message.text
    if text.lower() == 'Привет':
        context.bot.send_message(update.effective_chat.id, 'Добро пожаловать, я Бот-телефонный справочник🤓!\n'
                                                            'Я много чего умею:')
    else:
        context.bot.send_message(update.effective_chat.id, 'Я Вас не понимаю, но могу что-то подскзать. Я много чего умею:')
        context.bot.send_message(update.effective_chat.id, ALL_FUNCTIONS)

def unknown(update, context):
    context.bot.send_message(update.effective_chat.id, 'Такую команду я не знаю. Но вот что я умею:')
    context.bot.send_message(update.effective_chat.id, ALL_FUNCTIONS)

def entry():
    with open("phone_number.json", "w", encoding="utf-8") as tel:
        tel.write(json.dumps(phone_number, ensure_ascii=False))

def load():
    global contact
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
    except:
        contact.append(phone_number)

        with open("contacts.json", "w", encoding="utf-8") as cont:
            cont.write(json.dumps(contact, ensure_ascii=False)) # dumps - сериализировывает obj в строку в формате JSON
        log.text_in_log(
            f"Добавлен контакт: {phone_number['lastname']} {phone_number['name']} {phone_number['num']}")
        contact.append(phone_number)
        with open("contacts.json", "w", encoding="utf-8") as cont:
            cont.write(json.dumps(contact, ensure_ascii=False))
        log.text_in_log(
            f"Добавлен контакт: {phone_number['lastname']} {phone_number['name']} {phone_number['num']}")

def lastname(update, _):
    phone_number['lastname'] = update.message.text
    entry()
    log.text_in_log(f'Введена фамилия: {update.message.text}')
    update.message.reply_text('Введите имя:')
    return NAME

def name(update, _):
    phone_number['name'] = update.message.text
    entry()
    log.text_in_log(f'Введено имя: {update.message.text}')
    update.message.reply_text('Введите номер телефона:')
    return NUM

def num(update, _):
    phone_number['num'] = update.message.text
    entry()
    log.text_in_log(f"Введён номер телефона: {update.message.text}")
    add_contact(phone_number)
    return ConversationHandler.END

def all_contacts(update, _):
    pass

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