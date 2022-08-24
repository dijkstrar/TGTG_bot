import asyncio
from dotenv import load_dotenv
from telegram.ext import CommandHandler
import os
import telegram
from telegram.ext import Updater

from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import MessageHandler, Filters
import traceback

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
                            text=f"Welcome {update['effective_chat']['first_name']} to TooGoodToGo Checker 🛍️🤑. 👋 I am the TooGoodToGo bot.\
🚨 I will tell you whenever the stock of your favorites changes. \
To login into your TooGoodToGo account run: /register email@example.com \
If you get tired of my spamming you can (temporarily) disable me with: \
/deregister")
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
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"Valid email. Please verify login by clicking the link in your mailbox, using computer (Don't open the email on a phone that has the TooGoodToGo app installed. That won't work.) 📧. Sent a mail to: {email}")
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

def check_if_running(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if chat_id not in TGTG_framework.get_active_ids():
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"An error occurred... 😔 You are NOT registered. Please register via /register 💪 ")
    else:
        try:
            check_result = TGTG_framework.request_offers(chat_id)
            context.bot.send_message(chat_id=update.effective_chat.id, text=f'Still running successfully 💯 {len(check_result)} offers waiting!')
        except Exception as e:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"An error occurred... 😔 maybe you're not registered...! 😵 Please register via /register 💪 \
            {e}, {traceback.format_exc()}")
up_handler = CommandHandler('up', check_if_running)
dispatcher.add_handler(up_handler)


# keep as last.
def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command 😕.")

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

updater.start_polling(poll_interval=3)
