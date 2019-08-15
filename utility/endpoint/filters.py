#import pythons enum lib
from enum import Enum

class APIFilter(Enum):
    PLAYER_FILTER = 'players?filter[playerNames]='
    MATCH_FILTER = 'matches/$matchID'
    LIFETIME_FILTER = 'players/$accountId/seasons/lifetime'
    SEASON_FILTER = 'players/$accountId/seasons/$seasonID'
    LIST_TOURNAMENTS_FILTER = 'tournaments/'
    TOURNAMENTS_FILTER = 'tournaments/$tourneyID'

    def buildPlayerFilter(_BASE, _PLAYER_NAME):
        return _BASE+APIFilter.PLAYER_FILTER.value+_PLAYER_NAME
    def buildSeasonFilter(_BASE,_SEASON, _PLAYER_ID):
        return _BASE+APIFilter.SEASON_FILTER.value.replace('$accountId', _PLAYER_ID).replace('$seasonID', _SEASON) 
    def buildLifeTimeFilter(_BASE, _PLAYER_ID):
        return _BASE+APIFilter.LIFETIME_FILTER.value.replace('$accountId', _PLAYER_ID)
    def buildTourneyFilter(_TORUNEY_ID):
        return 'https://api.pubg.com/'+APIFilter.TOURNAMENTS_FILTER.value.replace('$tourneyID', _TORUNEY_ID)