##Import my tools to be used
from utility.platforms.platform_shards import Shard
from objects.player import player
from utility.endpoint.filters import APIFilter

#import pythons Time lib
import time

class API_INTERFACE():

    def matchStats(playerName: str, platform: str, auth_header, amount: int):
        '''
            Wrapper for a quick breakdown of player stats over a number of matches. 
            Also prints a table including each of these matches out to the console.

            playerName - the players name that you want to produce a quick breakdown of over a number matches (case-sensitive)

            platform - the platform the player is playing on, can be one of the following:
            - XBOX / xbox
            - PC / pc
            - PSN / psn
            - KAKAO / kakao

            auth_header - the header we will use to contact the API.

            amount - amount of matches you want to display. 
            The amount of time the script will take to process the data, scales linearly with this.
        '''
        
        _URL = Shard.buildURL(platform)

        _player_object = player(auth_header)
        _player_object.getAccountID(playerName, _URL, amount, False)
        _player_object.displayMatches(_URL)

    def lifetimeStats(playerName: str, platform: str, auth_header, game_mode):
        '''
            Wrapper for lifetime stats.

            playerName - the players name you want to lookup the lifetime stats of (case-sensitive)

            platform - the platform the player is playing on, can be one of the following:
            - XBOX / xbox
            - PC / pc
            - PSN / psn
            - KAKAO / kakao

            auth_header - the header we will use to contact the API.

            game_mode - the game mode you want to lookup, one of the following:
            - ALL / all (Displays FPP and TPP lifetime stats)
            - FPP / fpp (Displays FPP only lifetime stats)
            - SOLO-FPP / solo-fpp (Displays only solo FPP lifetime stats)
            - DUO-FPP-FPP / duo-fpp (Displays only duo FPP lifetime stats)
            - SQUAD-FPP / squad-fpp (Displays only squad FPP lifetime stats)
            - TPP / tpp (Displays TPP only lifetime stats)
            - DUO / duo (Displays only duo TPP lifetime stats)
            - SOLO / solo (Displays only  solo TPP lifetime stats)
            - SQUAD / squad (Displays only squad TPP lifetime stats)
        '''

        _URL = Shard.buildURL(platform)

        _player_object = player(auth_header)
        _player_object.getAccountID(playerName, _URL, 0, True)
        _player_object.lifetimeStats(_URL, game_mode.lower())

    def seasonStats(playerName: str, platform: str, auth_header, game_mode, _season):
        '''
            Wrapper for lifetime stats.

            playerName - the players name you want to lookup the lifetime stats of (case-sensitive)

            platform - the platform the player is playing on, can be one of the following:
            - XBOX / xbox
            - PC / pc
            - PSN / psn
            - KAKAO / kakao

            auth_header - the header we will use to contact the API.

            game_mode - the game mode you want to lookup, one of the following:
            - ALL / all (Displays FPP and TPP lifetime stats)
            - FPP / fpp (Displays FPP only lifetime stats)
            - SOLO-FPP / solo-fpp (Displays only solo FPP lifetime stats)
            - DUO-FPP-FPP / duo-fpp (Displays only duo FPP lifetime stats)
            - SQUAD-FPP / squad-fpp (Displays only squad FPP lifetime stats)
            - TPP / tpp (Displays TPP only lifetime stats)
            - DUO / duo (Displays only duo TPP lifetime stats)
            - SOLO / solo (Displays only  solo TPP lifetime stats)
            - SQUAD / squad (Displays only squad TPP lifetime stats)
        '''

        _URL = Shard.buildURL(platform)

        _player_object = player(auth_header)
        _player_object.getAccountID(playerName, _URL, 0, True)
        _player_object.seasonStats(_URL, game_mode.lower(), _season)