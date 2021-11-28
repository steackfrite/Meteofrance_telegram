#!/bin/python3

from meteofrance_api import MeteoFranceClient
import sys
#from telegram.ext import Updater, InlineQueryHandler, CommandHandler

class MeteoFrance:
    # meteo: MeteoFranceClient = None

    def __init__(self):
        # Initialisation de la classe meteofrance
        self.meteo = meteofrance_api.MeteoFranceClient()

    def search_city(self, city, self.meteo):
        i = 0

        try:
            print(city)
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

    def get_forecast(self, city, meteo, forecast_choice):
        # Variables
        my_forecast = {}
        i = 0

        print(f'{city}')

        try:
            my_forecast = meteo.get_forecast_for_place(city)
        except:
            print(f'Echec de la récupération du bulletin météo pour {city}')
            return 0
        else:
            if 'heure' in forecast_choice:
                print(f'\nTempérature: {my_forecast.current_forecast["T"]["value"]}')
                print(f'Ressentie: {my_forecast.current_forecast["T"]["windchill"]}')
                print(f'Humidité: {my_forecast.current_forecast["humidity"]}%')
                print(f'Risque de pluie: {my_forecast.current_forecast["rain"]["1h"]}%')
                print(f'Rique de neige: {my_forecast.current_forecast["snow"]["1h"]}%')
                print(f'Ciel: {my_forecast.current_forecast["weather"]["desc"]}')
            elif 'jour' in forecast_choice:
                print(f'\nTempérature:')
                print(f'  * Min: {my_forecast.today_forecast["T"]["min"]}°C')
                print(f'  * Max: {my_forecast.today_forecast["T"]["max"]}°C')
                print(f'\nHumidité:')
                print(f'  * Min: {my_forecast.today_forecast["humidity"]["min"]}%')
                print(f'  * Max: {my_forecast.today_forecast["humidity"]["max"]}%')
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


# def main():
#     # Variables
#     cities = []
#     city_search = ''
#     city_choice = 0
#     city_user = ''
#     forecast_choice = False
#
#     # Initialisation de la classe meteofrance
#     meteo = meteofrance_api.MeteoFranceClient()
#
#     # Gestion des arguments de l'utilisateur
#     if len(sys.argv) == 3:
#         city_search = sys.argv[1]
#     elif len(sys.argv) == 4:
#         city_search = sys.argv[1]
#         city_choice = int(sys.argv[3])
#     else:
#         print(f'Utilisation : python meteo-france.py "ville" "jour ou heure" "choix de la ville (optionel)"')
#         print(f'Exemple : python meteo-france.py lyon jour 0')
#         sys.exit(-1)
#
#     if 'jour' not in sys.argv[2] and 'heure' not in sys.argv[2] and 'semaine' not in sys.argv[2]:
#         print(f'Utilisation : python meteo-france.py "ville" "jour, heure ou semaine" "choix de la ville (optionel)"')
#         print(f'Exemple : python meteo-france.py lyon jour 0')
#         sys.exit(-1)
#     else:
#         forecast_choice = sys.argv[2]
#
#     cities = search_city(city_search, meteo)
#     city_user = cities[city_choice]
#     get_forecast(city_user, meteo, forecast_choice)



if __name__ == '__main__':
    main()
















#space
