import asyncio
from dotenv import load_dotenv
from telegram.ext import CommandHandler
import os
import telegram
from telegram.ext import Updater

from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import MessageHandler, Filters


import re

import TGTG_framework

email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

load_dotenv()

TOKEN = os.getenv('TELEGRAM_TOKEN')
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

#start 
def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, 
                            text=f"Welcome {update['effective_chat']['first_name']} to TooGoodToGo Checker 🛍️🤑. Please discover all commands via /!")
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

#echo
def echo(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Sorry, I did not understand you correctly.. I can only receive commands. Please type / to show all commands.')
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

#register
def register(update: Update, context: CallbackContext):
    if len(context.args)==0:
        context.bot.send_message(chat_id=update.effective_chat.id, text='No email supplied, please try again using /register [e-mail address] 🪄')
    else:
        email = context.args[0]
        if re.fullmatch(email_regex, email):
            context.bot.send_message(chat_id=update.effective_chat.id, text=f'Valid email. Please verify login by clicking the link in your mailbox, using computer (not Phone) 📧. Sent a mail to: {email}')
            TGTG_framework.login(update.effective_chat.id, email)
            context.bot.send_message(chat_id=update.effective_chat.id, text=f'Login Succesful 🔑\nStay Tuned for notifications 🔔')
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text='Invalid email, please try again using /register [e-mail address] 🪄')
register_handler = CommandHandler('register', register)
dispatcher.add_handler(register_handler)

def deregister(update: Update, context: CallbackContext):
    if TGTG_framework.remove_credentials(update.effective_chat.id)>0:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'Succesfully deregistered 👋 You can receive notifications again by using /register command')
        TGTG_framework.remove_sent_offers(update.effective_chat.id)
    else: 
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'You were never registered 🤷. Nothing happened.')
deregister_handler = CommandHandler('deregister', deregister)
dispatcher.add_handler(deregister_handler)




# keep as last.
def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command 😕.")

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

updater.start_polling()