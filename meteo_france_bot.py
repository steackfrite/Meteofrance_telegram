#!/bin/python3

from dotenv import load_dotenv
from os import getenv
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import Updater

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Let's rock 'n roll!")


def main():
    # Variables
    token: str = ''

    # Loading env file
    load_dotenv('.env')

    ## Bot initilisation ##
    token = getenv('TELEGRAM_BOT_TOKEN') # TODO : A ajouter dans la doc
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher
    ## Bot initilisation ##

    ## Listening to commands ##
    start_handler = CommandHandler('start', start)
    ## Listening to commands ##

    ## Add command to the dispatcher ##
    dispatcher.add_handler(start_handler)
    ## Add command to the dispatcher ##

    # Launch the bot!
    updater.start_polling()

if __name__ == '__main__':
    main()
