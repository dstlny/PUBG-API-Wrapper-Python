#import pythons requests, json, sys, ps amd datetime lib
import requests, json, sys,  xlsxwriter
from os import path, system
from datetime import datetime
from time import sleep

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

##Import my tools to be used
from helper.helperFunctions import returnMapName, getSeasonRank
from utility.endpoint.filters import APIFilter
from parsers.APIResponse import APIResponse

##Import exceptions that can be defined
from exceptions.rateLimit import rateLimitReached
from exceptions.playerNotFound import playerNotFound
from exceptions.seasonStatsNotFound import seasonStatsNotFound
from exceptions.connectionTimeOut import connectionTimeOut

from config import user_settings

class D(dict):
    def __missing__(self, key):
        self[key] = D()
        return self[key]

class player():
    '''
        1. Describes the Player you want to lookup.

        2. Holds player stats - such as Account ID, Account Name, and a list of recent Match ID's
    '''

    if user_settings.GUI:
    
        def __init__(self, _header, _region):
            self._HEADER = _header
            self.ID = ""
            self.NAME = ""
            self.MATCH_IDS = list()
            self.SEASONS = list()
            self.REGION = _region
    
    else:

        def __init__(self, _header):
            self._HEADER = _header
            self.ID = ""
            self.NAME = ""
            self.MATCH_IDS = list()
            self.SEASONS = list()

    def getAccountID(self, _PLAYER_NAME, _BASE_URL, _NO_MATCHES, _LIFETIME: bool):
        '''
            Grabs the users Account ID based on the API's response from the users name. Sets up the Player object.

            playerName - the players name (case-sensitive)

            _BASE_URL - the API's base URL

            _NO_MATCHES - an integer representing the number of matches that you want to display - which is passed on to processPlayerObject().
            This also seems to be unique per player.

            _LIFETIME - bool representing whether it's a lifetime or seasonal request
        '''
        _PLAYER_URL = APIFilter.buildPlayerFilter(_BASE_URL, _PLAYER_NAME)

        try:
            _PLAYER_REQUEST = requests.get(_PLAYER_URL, headers=self._HEADER)
            _PLAYER_REQUEST.close()     
        except Exception as Excep:
            connectionTimeOut(Excep)

        self.NAME = _PLAYER_NAME
        
        _API_RESPONSE = json.loads(_PLAYER_REQUEST.text)

        if 'errors' in _API_RESPONSE:
            playerNotFound(_PLAYER_NAME)
            return False
        else:
            
            _MATCHES = []

            for _MATCH_ID in _API_RESPONSE['data'][0]['relationships']['matches']['data']:
                if not _LIFETIME and len(_MATCHES) < _NO_MATCHES and _MATCH_ID['id'] is not None:
                    _MATCHES.append(_MATCH_ID['id'])

            self.ID = _API_RESPONSE['data'][0]['id']

            if len(_MATCHES) != 0 and not _LIFETIME:
                self.setMatches(_MATCHES)

            return True

    def seasonStats(self, _BASE_URL, _GAME_MODE, _SEASON):
        '''
            Proccesses and displays the users lifetime stats.

            _API_RESPONSE is the PUBG API's response.

            _NO_MATCHES is an integer representing the number of matches you want to display.

            _SEASON - SEASON ID

        '''

        _local_season = APIResponse(_GAME_MODE, self, _season=_SEASON)
        _local_season.parseJSONSeasonAndLifetimeResponse(_BASE_URL)

    def lifetimeStats(self, _BASE_URL, _GAME_MODE):
        '''
            Proccesses and displays the users lifetime stats.

            _API_RESPONSE is the PUBG API's response.

            _NO_MATCHES is an integer representing the number of matches you want to display.

            _SEASON - SEASON ID

        '''

        _local_season = APIResponse(_GAME_MODE, self)
        _local_season.parseJSONSeasonAndLifetimeResponse(_BASE_URL)


    def setPlayerID(self, identity):
        self.ID = identity

    def getPlayerID(self):
        return self.ID

    def setPlayerName(self, name):
        self.NAME = name

    def getPlayerName(self):
        return self.NAME

    def setMatches(self, matches: list):
        
        if isinstance(matches, list):
            [self.MATCH_IDS.append(x) for x in matches]
        else:
            raise TypeError("Matches must be of type List")

    def getMatches(self):
        return self.MATCH_IDS

    def displayMatches(self, _BASE_URL):
        '''
            Displays a number of matches.
        '''
        
        _DATES = []
        _DAMAGE = []
        _MAP = []
        _GAMEMODE = []
        _WIN = []
        _KILLS = []

        _WIN_COUNT = 0
        _KILL_COUNT = 0
        _DAMAGE_COUNT = 0

        _EXCEL_GRAPH_X_COL = []
        _EXCEL_GRAPH_Y_COL = []

        for _MATCH_ID in self.getMatches():
            
            _URL = _BASE_URL+APIFilter.MATCH_FILTER.value.replace('$matchID', _MATCH_ID)

            _REQUEST = requests.get(_URL, headers=self._HEADER)

            if _REQUEST.status_code == 429:
                rateLimitReached()
                _REQUEST = requests.get(_URL, headers=self._HEADER)
                _REQUEST.close()

            _RESPONSE = json.loads(_REQUEST.text)
            
            if _RESPONSE['data']['attributes']['mapName'] == 'Range_Main':
                continue
            else:
                _JSON_TIME_DATA = datetime.strptime(_RESPONSE['data']['attributes']['createdAt'].replace('Z',''),"%Y-%m-%dT%H:%M:%S")
                _DATES.append(str(_JSON_TIME_DATA.strftime('%m/%d/%Y')))
                _MAP.append(returnMapName(_RESPONSE['data']['attributes']['mapName']))
                _GAMEMODE.append(_RESPONSE['data']['attributes']['gameMode'].upper())
                for _STAT in _RESPONSE['included']:
                    if 'stats' in _STAT['attributes'] and 'playerId' in _STAT['attributes']['stats'] and _STAT['attributes']['stats']['playerId'] == self.getPlayerID():
                        _DAMAGE.append(round(_STAT['attributes']['stats']['damageDealt'],2))
                        _WIN.append(f"{_STAT['attributes']['stats']['winPlace']}/100")
                        _KILLS.append(f"{_STAT['attributes']['stats']['kills']}")
                        break
        
        _EXCEL_GRAPH_Y_COL = set()

        for _WIN_INT, _KILL_INT, _DAMAGE_INT, _DATE  in zip(_WIN, _KILLS, _DAMAGE, _DATES):
            _KILL_COUNT += int(_KILL_INT.replace('kills','').strip())
            _DAMAGE_COUNT += _DAMAGE_INT
            _EXCEL_GRAPH_Y_COL.add(_DATE)
            if _WIN_INT == '1/100':
                _WIN_COUNT += 1

        _LOCAL_KILLS = 0
        
        ##This will be the dataset we use.
        DATE_DICT = D({
            'dates': {

            }
        })

        kill_values = []

        for i, x in enumerate(_DATES):
            
            if i+1 <= len(_DATES)-1:

                if x == _DATES[i+1]:
                    _LOCAL_KILLS += int(_KILLS[i])
                else:
                    DATE_DICT['dates'][x] = _LOCAL_KILLS
                    kill_values.append(_LOCAL_KILLS)
                    _LOCAL_KILLS = 0

            else:
                
                if x == _DATES[len(_DATES)-1]:
                    _LOCAL_KILLS += int(_KILLS[i])
                    DATE_DICT['dates'][x] = _LOCAL_KILLS
                    kill_values.append(_LOCAL_KILLS)
                    _LOCAL_KILLS = 0

        data_start_loc = [0, 0] # xlsxwriter rquires list, no tuple
        data_end_loc = [data_start_loc[0] + len(DATE_DICT['dates'])-1, 0]

        workbook = xlsxwriter.Workbook(f'DATA/{self.NAME}-{len(_MAP)}Matches.xlsx')
        
        chart = workbook.add_chart({
            'type': 'line'
        })
        
        chart.set_y_axis({
            'name': 'Kills per day'
        })
        
        chart.set_x_axis({
            'name': 'Day'
        })
        
        chart.set_title({
            'name': f'Amount of kills from {min(_EXCEL_GRAPH_Y_COL)} - {max(_EXCEL_GRAPH_Y_COL)}'
        })

        worksheet = workbook.add_worksheet()

        # A chart requires data to reference data inside excel
        worksheet.write_column(*data_start_loc, data=reversed(kill_values))
        chart.add_series({
            'values': [worksheet.name] + data_start_loc + data_end_loc,
            'name': "Kills",
        })
        
        worksheet.insert_chart('B1', chart)
        workbook.close()  # Write to file

        if user_settings.GUI: 
        
            _FILENAME = f'DATA/{self.NAME}-{len(_MAP)}Matches.csv'
                
            with open(_FILENAME, 'w+', encoding="utf-8") as f:
                f.write('{},{},{},{},{},{},{}\n'.format('MATCH', 'DATE', 'PLACEMENT', 'MAP', 'MODE', 'DAMAGE', 'KILLS'))
                for i, item in enumerate(zip(_DATES, _WIN, _MAP, _GAMEMODE, _DAMAGE, _KILLS)):
                    f.write('{},{},{},{},{},{},{}\n'.format(i+1, *item))
                f.write(f'\n  Stats for {self.NAME} accross {len(_MAP)} matches\n  - Won {_WIN_COUNT} out of {len(_MAP)} games\n  - Averages {round(_KILL_COUNT / len(_KILLS), 2)} kills per game\n  - Total of {_KILL_COUNT} kills and {round(_DAMAGE_COUNT,2)} damage across {round(len(_KILLS), 2)} matches\n  - Highest kill game of {max(_KILLS)} in {_GAMEMODE[_KILLS.index(max(_KILLS))]}\n')

        else:

            print('\n|-------------------------------------------------------------------------------------------------------------------|\n| {:<5} | {:<15} | {:<15} | {:<15} | {:<15} | {:<15} | {:<15} |'.format('MATCH', 'DATE', 'PLACEMENT', 'MAP', 'MODE', 'DAMAGE', 'KILLS')+'\n|-------------------------------------------------------------------------------------------------------------------|')
            for i, item in enumerate(zip(_DATES, _WIN, _MAP, _GAMEMODE, _DAMAGE, _KILLS)):
                print('| {:<5} | {:<15} | {:<15} | {:<15} | {:<15} | {:<15} | {:<15} |\n|-------------------------------------------------------------------------------------------------------------------|'.format(i+1, *item))
            print('| {:<5} | {:<15} | {:<15} | {:<15} | {:<15} | {:<15} | {:<15} |\n|-------------------------------------------------------------------------------------------------------------------|\n'.format('MATCH', 'DATE', 'PLACEMENT', 'MAP', 'MODE', 'DAMAGE', 'KILLS'))
            print(f'\n  Stats for {self.NAME} accross {len(_MAP)} matches\n  - Won {_WIN_COUNT} out of {len(_MAP)} games\n  - Averages {round(_KILL_COUNT / len(_KILLS), 2)} kills per game\n  - Total of {_KILL_COUNT} kills and {round(_DAMAGE_COUNT,2)} damage across {round(len(_KILLS), 2)} matches\n  - Highest kill game of {max(_KILLS)} in {_GAMEMODE[_KILLS.index(max(_KILLS))]}\n')