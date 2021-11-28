#!/bin/python3

from dotenv import load_dotenv
from os import getenv
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater

import meteo_france

# Variable globales
meteofrance_class = meteo_france.MeteoFrance()

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Let's rock 'n roll!")


def echo(update: Update, context: CallbackContext):
    message_01 = 'Envoyez-moi une commande et non pas un message !' # souligner commande
    message_02 = 'Taper /help pour voir la liste des commandes possibles' # souligner /help

    context.bot.send_message(chat_id=update.effective_chat.id, text=message_01)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message_02)

def meteo(update: Update, context: CallbackContext):
    error_01 = 'Utilisation : python meteo-france.py "ville" "jour ou heure" "choix de la ville (optionel)"'
    error_02 = 'Exemple : python meteo-france.py lyon jour 0'
    error = False

    # Gestion des arguments de l'utilisateur
    if len(context.args) == 2:
        city_search = context.args[0]
        forecast_choice = context.args[1]
        city_choice = 0
    elif len(context.args) == 3:
        city_search = context.args[0]
        forecast_choice = context.args[1]
        city_choice = int(context.args[2])
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=error_01)
        context.bot.send_message(chat_id=update.effective_chat.id, text=error_02)
        error = True
        return 0

    if 'jour' not in forecast_choice and 'heure' not in forecast_choice and 'semaine' not in forecast_choice:
        context.bot.send_message(chat_id=update.effective_chat.id, text=error_01)
        context.bot.send_message(chat_id=update.effective_chat.id, text=error_02)
        error = True
        return 0

    cities = meteofrance_class.search_city(city_search, meteo)
    city_user = cities[city_choice]
    meteofrance_class.get_forecast(city_user, meteo, forecast_choice)

def unknown(update: Update, context: CallbackContext):
    message_01 = 'Désolé, je n\'ai pas compris cette commande'
    message_02 = 'Taper /help pour voir la liste des commandes possibles'
    context.bot.send_message(chat_id=update.effective_chat.id, text=message_01)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message_02)

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
    meteo_handler = CommandHandler('meteo', meteo)
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    unknown_handler = MessageHandler(Filters.command, unknown)
    ## Listening to commands ##

    ## Add command to the dispatcher ##
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(meteo_handler)
    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(unknown_handler)
    ## Add command to the dispatcher ##

    # Launch the bot!
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
