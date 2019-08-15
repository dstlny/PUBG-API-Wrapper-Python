#import pythons requests, json, sys, ps amd datetime lib
import requests, json, sys
from os import path, system
from datetime import datetime
from time import sleep

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

##Import my tools to be used
from helper.helperFunctions import returnMapName, getSeasonRank
from utility.endpoint.filters import APIFilter

##Import exceptions that can be defined
from exceptions.rateLimit import rateLimitReached
from exceptions.playerNotFound import playerNotFound
from exceptions.seasonStatsNotFound import seasonStatsNotFound
from exceptions.connectionTimeOut import connectionTimeOut

from config import user_settings

class APIResponse():

    _SEASON = ""
    _GAMEMODE = ""
    _LOCAL_PLAYER = object
    _KILLS = 0
    _ASSISTS = 0
    _BOOSTS = 0
    _HEALS = 0
    _DAMAGE = 0
    _TEAMKILLS = 0
    _VEHICLES = 0
    _HEADSHOTS = 0
    _WEAPONS = 0
    _REVIVES = 0
    _DOWNS = 0
    _ROUNDS  = 0
    _WINS = 0

    def __init__(self, _gamemode, player, **kwargs):
        self._SEASON = kwargs.get("_season")
        self._GAMEMODE = _gamemode
        self._LOCAL_PLAYER = player

    def parseJSONSeasonAndLifetimeResponse(self, _BASE_URL):
        
        _VALID = ['duo', 'squad', 'solo', 'duo-fpp', 'squad-fpp', 'solo-fpp', 'all', 'fpp', 'tpp']

        if self._GAMEMODE.lower() not in _VALID:
            raise ValueError(f"Value must one of the following: {[x for x in _VALID]}")

        _STATS = []
        _EXCLUDE_GAME_MODE_STATS = ['SOLO-FPP','SOLO']
        _GAMEMODE_TYPES = ['tpp', 'fpp', 'all']
        _FFP_ONLY = ['duo-fpp', 'squad-fpp', 'solo-fpp']
        _REGIONS = ['pc-eu', 'pc-as', 'pc-na', 'pc-oc', 'pc-jp', 'pc-krjp', 'pc-ru', 'pc-sa','pc-sea','pc-kakao','psn-as','psn-eu','psn-na','psn-oc', 'xbox-as','xbox-eu','xbox-na','xbox-oc', 'xbox-na']
        _PLATFORMS = ['steam','xbox','psn', 'kakao']
        _SEASON_LIST = ['division.bro.official.2017-beta','division.bro.official.2017-pre1', 'division.bro.official.2017-pre2', 'division.bro.official.2017-pre3','division.bro.official.2017-pre4','division.bro.official.2017-pre5','division.bro.official.2017-pre6','division.bro.official.2017-pre7','division.bro.official.2017-pre8','division.bro.official.2017-pre9','division.bro.official.2018-01', 'division.bro.official.2018-02','division.bro.official.2018-03','division.bro.official.2018-04','division.bro.official.2018-05','division.bro.official.2018-07','division.bro.official.2018-08','division.bro.official.2018-09','division.bro.official.pc-2018-01', 'division.bro.official.pc-2018-02','division.bro.official.pc-2018-03','division.bro.official.pc-2018-04']

        if self._SEASON:    
            _URL = APIFilter.buildSeasonFilter(_BASE_URL, self._SEASON, self._LOCAL_PLAYER.getPlayerID())
            _STATS.append(f"\'{self._SEASON}' stats")
        else:
            _URL = APIFilter.buildLifeTimeFilter(_BASE_URL, self._LOCAL_PLAYER.getPlayerID())
            _STATS.append(f"\tLifetime stats for {self._LOCAL_PLAYER.NAME} in {self._GAMEMODE.upper()}")

        _REQUEST = requests.get(_URL, headers=self._LOCAL_PLAYER._HEADER)

        if _REQUEST.status_code == 429:
            rateLimitReached()
            _REQUEST = requests.get(_URL, headers=self._LOCAL_PLAYER._HEADER)

        _REQUEST.close()
        _RESPONSE = json.loads(_REQUEST.text)

        if 'errors' in _RESPONSE:
            
            if user_settings.GUI:
                _USER_REGION = self._LOCAL_PLAYER.REGION
            else:
                _USER_REGION = input(f"Enter a region, one of the following:\n {[x for x in _REGIONS]}\n")

            if _USER_REGION.lower() not in _REGIONS:
                raise ValueError(f"Region isn't correct, it must be one of the following: {[x for x in _REGIONS]}\n")
            else:
                for _PLATFORM in _PLATFORMS:
                    if _PLATFORM in _URL:
                        _URL = _URL.replace(_PLATFORM, _USER_REGION.lower())
                        _REQUEST = requests.get(_URL, headers=self._LOCAL_PLAYER._HEADER)
                        
                        if _REQUEST.status_code == 429:
                            rateLimitReached()
                            _REQUEST = requests.get(_URL, headers=self._LOCAL_PLAYER._HEADER)
                            
                        _REQUEST.close()
                        _RESPONSE = json.loads(_REQUEST.text)
                        break
        
        for _GM in _RESPONSE['data']['attributes']['gameModeStats']:
        
            if self._GAMEMODE == "all" or self._GAMEMODE == "fpp" and _GM in _FFP_ONLY or self._GAMEMODE == "tpp" and _GM not in _FFP_ONLY or  self._GAMEMODE == _GM:
                _STATS.append("\t=================================")
                _STATS.append(f"\t{_GM.upper()} stats")
                _STATS.append(f"\t- Total of {_RESPONSE['data']['attributes']['gameModeStats'][_GM]['wins']} chicken dinners")
                _STATS.append(f"\t- Total of {_RESPONSE['data']['attributes']['gameModeStats'][_GM]['kills']} kills, with {_RESPONSE['data']['attributes']['gameModeStats'][_GM]['headshotKills']} being headshots")
                _STATS.append(f"\t- Averages {_RESPONSE['data']['attributes']['gameModeStats'][_GM]['dailyKills']} daily kills")
                _STATS.append(f"\t- Has dealt {_RESPONSE['data']['attributes']['gameModeStats'][_GM]['damageDealt']} damage")
                _STATS.append(f"\t- {_RESPONSE['data']['attributes']['gameModeStats'][_GM]['assists']} kill assists")            
                _STATS.append(f"\t- Longest kill of {_RESPONSE['data']['attributes']['gameModeStats'][_GM]['longestKill']}m")
                _STATS.append(f"\t- Highest kill-round of {_RESPONSE['data']['attributes']['gameModeStats'][_GM]['roundMostKills']} kills")
                
                ##Since SOLO/SOLO-FPP doesn't have team-mates, we can exclude this data.
                if _GM.upper() not in _EXCLUDE_GAME_MODE_STATS:
                    _STATS.append(f"\t- Downed {_RESPONSE['data']['attributes']['gameModeStats'][_GM]['dBNOs']} players")
                    _STATS.append(f"\t- Revived {_RESPONSE['data']['attributes']['gameModeStats'][_GM]['revives']} team-mates")
                    _STATS.append(f"\t- Accidentally killed {_RESPONSE['data']['attributes']['gameModeStats'][_GM]['teamKills']} team-mates")
                
                ##Makes sure we aren't printing null data about these stats to the console.
                if _RESPONSE['data']['attributes']['gameModeStats'][_GM]['rankPoints'] != 0 and _RESPONSE['data']['attributes']['gameModeStats'][_GM]['rankPointsTitle'] != 0:
                    _STATS.append(f"\t- Currently sits at {int(_RESPONSE['data']['attributes']['gameModeStats'][_GM]['rankPoints'])} rankpoints, with Title of {getSeasonRank(_RESPONSE['data']['attributes']['gameModeStats'][_GM]['rankPoints'])}")
                
                _STATS.append(f"\t- {_RESPONSE['data']['attributes']['gameModeStats'][_GM]['losses']} losses out of {_RESPONSE['data']['attributes']['gameModeStats'][_GM]['roundsPlayed']} games")
                _STATS.append(f"\t- Destroyed {_RESPONSE['data']['attributes']['gameModeStats'][_GM]['vehicleDestroys']} vehicles")
                _STATS.append(f"\t- Acquired {_RESPONSE['data']['attributes']['gameModeStats'][_GM]['weaponsAcquired']} weapons")
                _STATS.append(f"\t- Consumed {_RESPONSE['data']['attributes']['gameModeStats'][_GM]['boosts']} boosts")
                _STATS.append(f"\t- Consumed {_RESPONSE['data']['attributes']['gameModeStats'][_GM]['heals']} heals")
                _STATS.append(f"\t- Swam {_RESPONSE['data']['attributes']['gameModeStats'][_GM]['swimDistance']}m")

                ## ------------------  Variable Incremantation 
                self._WEAPONS += _RESPONSE['data']['attributes']['gameModeStats'][_GM]['weaponsAcquired']
                self._ASSISTS += _RESPONSE['data']['attributes']['gameModeStats'][_GM]['assists']
                self._VEHICLES += _RESPONSE['data']['attributes']['gameModeStats'][_GM]['vehicleDestroys']
                self._TEAMKILLS += _RESPONSE['data']['attributes']['gameModeStats'][_GM]['teamKills']
                self._REVIVES += _RESPONSE['data']['attributes']['gameModeStats'][_GM]['revives']
                self._KILLS += _RESPONSE['data']['attributes']['gameModeStats'][_GM]['kills']
                self._HEADSHOTS += _RESPONSE['data']['attributes']['gameModeStats'][_GM]['headshotKills']
                self._ROUNDS += _RESPONSE['data']['attributes']['gameModeStats'][_GM]['roundsPlayed']
                self._HEALS += _RESPONSE['data']['attributes']['gameModeStats'][_GM]['heals']
                self._DAMAGE += _RESPONSE['data']['attributes']['gameModeStats'][_GM]['damageDealt']
                self._DOWNS += _RESPONSE['data']['attributes']['gameModeStats'][_GM]['dBNOs']
                self._BOOSTS += _RESPONSE['data']['attributes']['gameModeStats'][_GM]['boosts']
                self._ASSISTS += _RESPONSE['data']['attributes']['gameModeStats'][_GM]['assists']
                self._WINS += _RESPONSE['data']['attributes']['gameModeStats'][_GM]['wins']
                ## Variable Incremantation ------------------ ##

        ## Since the API just returns a blank fucking JSON file for a player which isn't in a season... we have to find some way to differentiate between a player which was around in this season, and not. This is the only way i could find.
        if self._SEASON and self._WEAPONS == 0 and self._ASSISTS == 0 and self._VEHICLES  == 0 and self._REVIVES  == 0 and self._KILLS  == 0 and self._HEADSHOTS == 0 and self._HEALS  == 0 and self._DAMAGE  == 0 and self._DOWNS  == 0 and self._BOOSTS  == 0 and self._ASSISTS == 0:
            seasonStatsNotFound(self._SEASON, self._LOCAL_PLAYER.NAME)

        if self._SEASON and user_settings.GUI:
            _FILENAME = f'DATA/{self._SEASON}-Stats.txt'
        elif not self._SEASON and user_settings.GUI:
            _FILENAME = f'DATA/Lifetime-{self._LOCAL_PLAYER.NAME}-{self._GAMEMODE.upper()}-Stats.txt'
        
        if user_settings.GUI:
            with open(_FILENAME, 'w+', encoding='utf-8') as f:
                for _DISPLAY_LINE in _STATS:
                    f.write(_DISPLAY_LINE+'\n')

                if self._GAMEMODE in _GAMEMODE_TYPES:
                    f.write(f"\t=================================\n\t- Total of {self._KILLS} kills\n\t- Total of {self._WINS} chicken dinners\n\t- Total of {self._HEADSHOTS} headshots\n\t- Total of {round(self._DAMAGE,2)} damage dealt\n\t- Total of {self._ASSISTS} assists\n\t- Total of {self._DOWNS} player knocks\n\t- Total of {self._BOOSTS} boosts consumed\n\t- Total of {self._HEALS} heals consumed\n\t- Total of {self._TEAMKILLS} team-kills\n\t- Total of {self._VEHICLES} vehicles destroyed\n\t- Total of {self._WEAPONS} weapons acquired\n\t- Total of {self._REVIVES} revives\n")
        else:
            print('\n')
            for _DISPLAY_LINE in _STATS:
                print(_DISPLAY_LINE)
    
            if self._GAMEMODE in _GAMEMODE_TYPES:
                print(f"\t=================================\n\t- Total of {self._KILLS} kills\n\t- Total of {self._WINS} chicken dinners\n\t- Total of {self._HEADSHOTS} headshots\n\t- Total of {round(self._DAMAGE,2)} damage dealt\n\t- Total of {self._ASSISTS} assists\n\t- Total of {self._DOWNS} player knocks\n\t- Total of {self._BOOSTS} boosts consumed\n\t- Total of {self._HEALS} heals consumed\n\t- Total of {self._TEAMKILLS} team-kills\n\t- Total of {self._VEHICLES} vehicles destroyed\n\t- Total of {self._WEAPONS} weapons acquired\n\t- Total of {self._REVIVES} revives\n")
            else:
                print('\n')


