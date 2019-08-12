from utility.platforms.seasons.season_shards import PCSeasons, PS4Seasons, XBOXSeasons

'''
    MATCH_INTEGER
    - Any integer.
    ----------------------------------------------------------
    PLAYER_NAME
    - The players name you want to lookup
    ----------------------------------------------------------
    GUI
    - True or False
      - If True, program will be executed as a GUI.
      - If False, will be executed as a Console Application.
    ----------------------------------------------------------
    MATCH_INTEGER
    - Any integer.
    ----------------------------------------------------------
    PLAYER_PLATFORM
    1. XBOX
    2. PSN
    or 
    3. PC
    ----------------------------------------------------------
    SEASON_VAL
    - A valid season for a valid platform
    ----------------------------------------------------------
    
'''

GUI = True

PLAYER_NAME = ''
MATCH_INTEGER = 0
PLAYER_PLATFORM = ''
PLAYER_GAME_MODE = ''
SEASON_VAL = PCSeasons.RELEASE_13.value

_PYTHON_FILE_CONTENTS = r"""import time
from os import system

from api_interface import API_INTERFACE
from helper.helperFunctions import regionCheck
from config.APIConfig import APIConfig
from config.APISettings import APISettings
from config import user_settings

user_input = input("\n\tPlease select one of the following options:\n\t1 - Lifetime Stats\n\t2 - Season Stats\n\t3 - x Amount of Match Stats\n\tInput choice: ")
user_input = int(user_input)

start_time = time.time()

_HEADER = APIConfig(APISettings.API_TOKEN).setupAuth()

if user_input in range(1,4):

    if user_input == 1: ##Lifetime
        system('cls')
        API_INTERFACE.lifetimeStats(user_settings.PLAYER_NAME, user_settings.PLAYER_PLATFORM, _HEADER, user_settings.PLAYER_GAME_MODE)
    elif user_input == 2: ##Season
        system('cls')
        regionCheck(user_settings.SEASON_VAL)
        API_INTERFACE.seasonStats(user_settings.PLAYER_NAME, user_settings.PLAYER_PLATFORM, _HEADER, user_settings.PLAYER_GAME_MODE, user_settings.SEASON_VAL)
    elif user_input == 3: ##Match stats
        system('cls')
        API_INTERFACE.matchStats(user_settings.PLAYER_NAME, user_settings.PLAYER_PLATFORM, _HEADER, user_settings.MATCH_INTEGER)
        
    print("--- took %s seconds ---" % (time.time() - start_time))"""