from utility.platforms.seasons.season_shards import PCSeasons, PS4Seasons, XBOXSeasons

'''
    MATCH_INTEGER
    - Any integer.
    ----------------------------------------------------------
    PLAYER_GAME_MODE
    - ALL / all (Displays FPP and TPP lifetime stats)
    - FPP / fpp (Displays FPP only lifetime stats)
    - SOLO-FPP / solo-fpp (Displays only solo FPP lifetime stats)
    - DUO-FPP-FPP / duo-fpp (Displays only duo FPP lifetime stats)
    - SQUAD-FPP / squad-fpp (Displays only squad FPP lifetime stats)
    - TPP / tpp (Displays TPP only lifetime stats)
    - DUO / duo (Displays only duo TPP lifetime stats)
    - SOLO / solo (Displays only  solo TPP lifetime stats)
    - SQUAD / squad (Displays only squad TPP lifetime stats)
    ----------------------------------------------------------
    PLAYER_GAME_MODE
    - XBOX / xbox
    - PC / pc
    - PSN / psn
    - KAKAO / kakao
    ----------------------------------------------------------
    PLAYER_NAME
    - The players name you want to lookup
    ----------------------------------------------------------
    SEASON_VAL
    - Platform season

    List of PC/Kakao Seasons, oldest to newest:
        BETA_0 = 'division.bro.official.2017-beta'
        BETA_1 = 'division.bro.official.2017-pre1'
        BETA_2 = 'division.bro.official.2017-pre2'
        BETA_3 = 'division.bro.official.2017-pre3'
        BETA_4 = 'division.bro.official.2017-pre4'
        BETA_5 = 'division.bro.official.2017-pre5'
        BETA_6 = 'division.bro.official.2017-pre6'
        BETA_7 = 'division.bro.official.2017-pre7'
        BETA_8 = 'division.bro.official.2017-pre8'
        BETA_9 = 'division.bro.official.2017-pre9'
        RELEASE_1 ='division.bro.official.2018-01'
        RELEASE_2 ='division.bro.official.2018-02'
        RELEASE_3 ='division.bro.official.2018-03'
        RELEASE_4 ='division.bro.official.2018-04'
        RELEASE_5 ='division.bro.official.2018-05'
        RELEASE_6 ='division.bro.official.2018-06'
        RELEASE_7 ='division.bro.official.2018-07'
        RELEASE_8 ='division.bro.official.2018-08'
        RELEASE_9 ='division.bro.official.2018-09'
        --- games before here need a region
        RELEASE_10 ='division.bro.official.pc-2018-01',
        RELEASE_11 ='division.bro.official.pc-2018-02',
        RELEASE_12 ='division.bro.official.pc-2018-03',
        RELEASE_13 ='division.bro.official.pc-2018-04'
    List of Xbox Seasons:
        RELEASE_1 ='division.bro.official.2018-05'
        RELEASE_2 ='division.bro.official.2018-06'
        RELEASE_3 ='division.bro.official.2018-07'
        RELEASE_4 ='division.bro.official.2018-08'
        --- games before here need a region
        RELEASE_5 ='division.bro.official.xbox-01'
        RELEASE_6 ='division.bro.official.xbox-02'
        RELEASE_7 ='didvision.bro.official.xb-pre1's
    List of Playstation Seasons:
        RELEASE_1 ='division.bro.official.2018-09'
        --- games before here need a region
        RELEASE_2 ='division.bro.official.playstation-01'
        RELEASE_3 ='division.bro.official.playstation-02'
     ----------------------------------------------------------
    SEASON
    - True or False.
'''

PLAYER_NAME = ''
PLAYER_PLATFORM = '' 
MATCH_INTEGER = 0
PLAYER_GAME_MODE = ''
SEASON_VAL = PCSeasons.RELEASE_13