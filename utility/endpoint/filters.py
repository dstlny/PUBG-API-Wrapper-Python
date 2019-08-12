#import pythons enum lib
from enum import Enum

class APIFilter(Enum):
    PLAYER_FILTER = 'players?filter[playerNames]='
    MATCH_FILTER = 'matches/'
    LIFETIME_FILTER = 'players/$accountId/seasons/lifetime'
    SEASON_FILTER = 'players/$accountId/seasons/$seasonID'

    def buildPlayerFilter(_BASE, _PLAYER_NAME):
        return _BASE+APIFilter.PLAYER_FILTER.value+_PLAYER_NAME
    def buildSeasonFilter(_BASE,_SEASON, _PLAYER_ID):
        return _BASE+APIFilter.SEASON_FILTER.value.replace('$accountId', _PLAYER_ID).replace('$seasonID', _SEASON) 
    def buildLifeTimeFilter(_BASE, _PLAYER_ID):
        return _BASE+APIFilter.LIFETIME_FILTER.value.replace('$accountId', _PLAYER_ID)