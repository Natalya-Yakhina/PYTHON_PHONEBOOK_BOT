import logger as log
from settings import TOKEN
import json
from telegram import Bot, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, ConversationHandler


def load():
    global contact
    try:
        with open("contacts.json", "r", encoding="utf-8") as cont:
            contact = json.load(cont)
    except:
        contact = []

SEARCH, END_SEARCH = range(2)

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


def search(update, _):
    text = update.message.text
    reply_keyboard = [['Да', 'Нет']]
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    temp = []
    load()
    for i in contact:
        if text in i['lastname'] or text in i['name'] or text in i['num']:
            temp.append(i)
    for i in temp:
        update.message.reply_text(
            f'{i["id"]+1}. {i["lastname"]} {i["name"]} {i["num"]}\n',
            reply_markup = markup_key)
    update.message.reply_text('Повторить поиск?')
    return END_SEARCH


def end_search(update, _):
    text = update.message.text
    if text == 'Нет':
        return ConversationHandler.END
    elif text == 'Да':
        update.message.reply_text('Введите данные для поиска: ')
        return SEARCH


def message(update, _):
    text = update.message.text
    if text == 'Поиск':
        log.text_in_log('Нажата кнопка "Поиск"')
        update.message.reply_text(
            'Введите данные для поиска')
        return SEARCH


bot = Bot(token = '5783314859:AAH0yxtMbSfflc03SxZaxamMhOZoV_RjKr8')
updater = Updater(token = '5783314859:AAH0yxtMbSfflc03SxZaxamMhOZoV_RjKr8')
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
search_handler = ConversationHandler(entry_points=[MessageHandler(Filters.text, message)],
    states = {SEARCH: [MessageHandler(Filters.text & ~Filters.command, search)],
            END_SEARCH: [MessageHandler(Filters.text & ~Filters.command, end_search)]})
message_handler = MessageHandler(Filters.text, message)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(search_handler)
dispatcher.add_handler(message_handler)

updater.start_polling()
updater.idle()