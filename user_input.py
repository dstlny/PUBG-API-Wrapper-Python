import time
from os import system

from api_interface import API_INTERFACE
from helper.helperFunctions import regionCheck
from config.APIConfig import APIConfig
from config.APISettings import APISettings
from config import user_settings

user_input = input("\n\tPlease select one of the following options:\n\t1 - Lifetime Stats\n\t2 - Season Stats\n\t3 - x Amount of Match Stats\n\tInput choice: ")
user_input = int(user_input)

start_time = time.time()

header = APIConfig(APISettings.API_TOKEN).setupAuth()

if user_input in range(1,4):

    if user_input == 1: ##Lifetime
        system('cls')
        API_INTERFACE.lifetimeStats(user_settings.PLAYER_NAME, user_settings.PLAYER_PLATFORM, header, user_settings.PLAYER_GAME_MODE)
    elif user_input == 2: ##Season
        system('cls')
        regionCheck(user_settings.SEASON_VAL)
        API_INTERFACE.seasonStats(user_settings.PLAYER_NAME, user_settings.PLAYER_PLATFORM, header, user_settings.PLAYER_GAME_MODE, user_settings.SEASON_VAL)
    elif user_input == 3: ##Match stats
        system('cls')
        API_INTERFACE.matchStats(user_settings.PLAYER_NAME, user_settings.PLAYER_PLATFORM, header, user_settings.MATCH_INTEGER)
        
    print("--- took %s seconds ---" % (time.time() - start_time))