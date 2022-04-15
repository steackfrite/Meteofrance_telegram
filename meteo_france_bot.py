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
    error_01 = 'Utilisation : /meteo "ville" "jour ou heure" "choix de la ville (optionel)"'
    error_02 = 'Exemple : /meteo lyon jour 0'
    error = False
    i: int = 0
    user_cities: str = ''

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

    ## Search and print city search ##
    cities = meteofrance_class.search_city(city_search)
    for city in cities:
        user_cities += '[' + str(i) + '] - ' + str(city) + '\n'
        i += 1

    context.bot.send_message(chat_id=update.effective_chat.id, text=str(user_cities))
    ## Search and print city search ##

    ## Get and print forecast ##
    city_user = cities[city_choice]
    my_forecast = meteofrance_class.get_forecast(city_user, forecast_choice)

    if 'heure' in forecast_choice:
        temp = 'Température : ' + str(my_forecast.current_forecast["T"]["value"]) + '°C'
        ressentie = '\nRessentie : ' + str(my_forecast.current_forecast["T"]["windchill"]) + '°C'
        humidity = '\nHumidité : ' + str(my_forecast.current_forecast["humidity"]) + '%'
        rain = '\nRisque de pluie : ' + str(my_forecast.current_forecast["rain"]["1h"]) + '%'
        snow = '\nRique de neige : ' + str(my_forecast.current_forecast["snow"]["1h"]) + '%'
        wind = '\nVent : \n' + \
        '   * Vitesse : ' + str(my_forecast.current_forecast["wind"]["speed"]) + '\n' + \
        '   * Direction : ' + str(my_forecast.current_forecast["wind"]["icon"]) + '\n'
        sky = '\nCiel : ' + my_forecast.current_forecast["weather"]["desc"]
        message = temp + ressentie + humidity + rain + snow + wind + sky
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    elif 'jour' in forecast_choice:
        temp = 'Température :\n' + \
        '   * Min : ' + str(my_forecast.today_forecast["T"]["min"]) + '°C\n' +\
        '   * Max : ' + str(my_forecast.today_forecast["T"]["max"]) + '°C\n'
        humidity = '\nHumidité :\n' + \
        '   * Min : ' + str(my_forecast.today_forecast["humidity"]["min"]) + '°C\n' +\
        '   * Max : ' + str(my_forecast.today_forecast["humidity"]["max"]) + '°C\n'

        sky = '\nCiel : ' + my_forecast.today_forecast["weather12H"]["desc"]
        message = temp + humidity + sky
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    else:
        i = 0
        message = ''
        for day in my_forecast.probability_forecast:
            if i < 7 :
                current_day = 'Jour ' + str(i) + ' :'
                if day["rain"]["3h"]:
                    rain = '\nPluie : ' + str(day["rain"]["3h"]) + '%'
                else:
                    rain = '\nPluie : 0%'
                if day["snow"]["3h"]:
                    snow = '\nNeige : ' + str(day["snow"]["3h"]) + '%'
                else:
                    snow = '\nNeige : 0%'
                if day["freezing"]:
                    freeze = '\nVerglas : '+ str(day["freezing"]) + '%\n\n'
                else:
                    freeze = '\nVerglas : 0%\n\n'
                i += 1

                message += current_day + rain + snow + freeze
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    ## Get and print forecast ##

def alert(update: Update, context: CallbackContext):
    # Variables
    departement: str = '00'
    error_01: str = 'Utilisation : /alert "numéro du département"'
    error_02: str = 'Exemple : /alert 69'

    # Gestion des arguments de l'utilisateur
    if len(context.args) == 1:
        departement = context.args[0]
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=error_01)
        context.bot.send_message(chat_id=update.effective_chat.id, text=error_02)
        error = True
        return 0

    ## Get and print alerts
    my_alert = meteofrance_class.get_alert(departement)
    print(f'{my_alert["text_bloc_item"]}')
    for alert in my_alert["text_bloc_item"]:
        if alert["text"]:
            for description in alert["text"]:
                message = description
                context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        else:
            message = "Pas d'alerte en cours"
            context.bot.send_message(chat_id=update.effective_chat.id, text=message)

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
    alert_handler = CommandHandler('alert', alert)
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    unknown_handler = MessageHandler(Filters.command, unknown)
    ## Listening to commands ##

    ## Add command to the dispatcher ##
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(meteo_handler)
    dispatcher.add_handler(alert_handler)
    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(unknown_handler)
    ## Add command to the dispatcher ##

    # Launch the bot!
    updater.start_polling()
    # updater.idle()



if __name__ == '__main__':
    main()
