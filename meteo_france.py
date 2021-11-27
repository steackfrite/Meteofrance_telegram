#!/bin/python3

import meteofrance_api
import sys
#from telegram.ext import Updater, InlineQueryHandler, CommandHandler

def search_city(city, meteo):
    i = 0

    try:
        cities = meteo.search_places(city)
    except:
        print("Echec de la recherche de ville")
        return 0
    else:
        print(f"Liste des villes trouvées pour ce {city} :")
        for city in cities:
            print(f'[{i}] {city}')
            i+=1

        print('\n')

    return cities

def get_forecast(city, meteo, forecast_choice):
    # Variables
    my_forecast = {}
    i = 0

    print(f'{city}')

    try:
        my_forecast = meteo.get_forecast_for_place(city)
    except:
        print(f'Echec de la récupération du bulletin méto pour {city}')
        return 0
    else:
        if 'heure' in forecast_choice:
            print(f'\nTempérature: {my_forecast.current_forecast["T"]["value"]}')
            print(f'Ressentie: {my_forecast.current_forecast["T"]["windchill"]}')
            print(f'Humidité: {my_forecast.current_forecast["humidity"]%}')
            print(f'Risque de pluie: {my_forecast.current_forecast["rain"]["1h"]}%')
            print(f'Rique de neige: {my_forecast.current_forecast["snow"]["1h"]}%')
            print(f'Ciel: {my_forecast.current_forecast["weather"]["desc"]}')
        elif 'jour' in forecast_choice:
            print(f'\nTempérature:')
            print(f'  * Min: {my_forecast.today_forecast["T"]["min"]°C}')
            print(f'  * Max: {my_forecast.today_forecast["T"]["max"]°C}')
            print(f'\nHumidité:')
            print(f'  * Min: {my_forecast.today_forecast["humidity"]["min"]%}')
            print(f'  * Max: {my_forecast.today_forecast["humidity"]["max"]%}')
            print(f'\nCiel: {my_forecast.today_forecast["weather12H"]["desc"]}')
        else:
            for jour in my_forecast.probability_forecast:
                if i < 7 :
                    print(f'Jour {i}:')
                    print(f'Pluie : {jour["rain"]["3h"]}%')
                    print(f'Verglas : {jour["freezing"]}%')
                    print(f'Neige : {jour["snow"]["3h"]}%')
                    i += 1
                else:
                    return 0

    return 0


def main():
    



if __name__ == '__main__':
    main()
















#space
