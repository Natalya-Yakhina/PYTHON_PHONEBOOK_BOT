from bot_token import tok
from controller import main_handler

import logging
from typing import Dict
from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler,CallbackContext

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)
updater = Updater(tok)
dispatcher = updater.dispatcher

dispatcher.add_handler(main_handler)
    
updater.start_polling()
print('server started')
updater.idle()