from enum import Enum

class Shard(Enum):
    '''
        Represents the BASE URL for each respective platform
    '''
    _BASE = 'https://api.pubg.com/'
    PC = "shards/steam/"
    XBOX = "shards/xbox/"
    PLAYSTATION = "shards/psn/"
    KAKAO = "shards/kakao/"
    TOURNAMENT = "shards/tournament/"

    def buildURL(platform):
        if  "pc" == platform.strip().lower():
            return Shard._BASE.value+Shard.PC.value
        elif "xbox" ==  platform.strip().lower():
            return Shard._BASE.value+Shard.XBOX.value
        elif "psn" ==  platform.strip().lower():
            return  Shard._BASE.value+Shard.PLAYSTATION.value
        elif "kakao" ==  platform.strip().lower():
            return  Shard._BASE.value+Shard.KAKAO.value
        elif "tour" ==  platform.strip().lower():
            return  Shard._BASE.value+Shard.TOURNAMENT.value
        else:
            raise ValueError("Platform options:\n1. 'PC'\n2. 'XBOX'\n3. 'PLAYSTATION'\n4. 'KAKAO'\n5. 'TOURNAMENT'")