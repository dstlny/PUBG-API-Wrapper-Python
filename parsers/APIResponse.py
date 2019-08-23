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

    seasonValue = ""
    gameMode = ""
    localPlayerObject = object
    totalKills = 0
    totalAssists = 0
    totalBoosts = 0
    totalHeals = 0
    totalDamage = 0
    totalTeamkills = 0
    totalVehiclesDestroyed = 0
    totalHeadshotKills = 0
    totalWeaponsAcquired = 0
    totalRevives = 0
    totalEnemyDowns = 0
    totalRoundsPlayed  = 0
    totalChickenDinners = 0

    def __init__(self, gameMode, player, **kwargs):
        self.seasonValue = kwargs.get("seasonValue")
        self.gameMode = gameMode
        self.localPlayerObject = player

    def parseJSONSeasonAndLifetimeResponse(self, inputURL):
        
        validGameModes = ['duo', 'squad', 'solo', 'duo-fpp', 'squad-fpp', 'solo-fpp', 'all', 'fpp', 'tpp']

        if self.gameMode.lower() not in validGameModes:
            raise ValueError(f"Value must one of the following: {[x for x in validGameModes]}")

        dataExists = True
        
        apiUserStats = []
        gameModesExcludedInOutput = ['SOLO-FPP','SOLO']
        gameModeTypes = ['tpp', 'fpp', 'all']
        fppOnlyGameModes = ['duo-fpp', 'squad-fpp', 'solo-fpp']
        platformRegions = ['pc-eu', 'pc-as', 'pc-na', 'pc-oc', 'pc-jp', 'pc-krjp', 'pc-ru', 'pc-sa','pc-sea','pc-kakao','psn-as','psn-eu','psn-na','psn-oc', 'xbox-as','xbox-eu','xbox-na','xbox-oc', 'xbox-na']
        platforms = ['steam','xbox','psn', 'kakao']
        allSeasonsForPlatforms = ['division.bro.official.2017-beta','division.bro.official.2017-pre1', 'division.bro.official.2017-pre2', 'division.bro.official.2017-pre3','division.bro.official.2017-pre4','division.bro.official.2017-pre5','division.bro.official.2017-pre6','division.bro.official.2017-pre7','division.bro.official.2017-pre8','division.bro.official.2017-pre9','division.bro.official.2018-01', 'division.bro.official.2018-02','division.bro.official.2018-03','division.bro.official.2018-04','division.bro.official.2018-05','division.bro.official.2018-07','division.bro.official.2018-08','division.bro.official.2018-09','division.bro.official.pc-2018-01', 'division.bro.official.pc-2018-02','division.bro.official.pc-2018-03','division.bro.official.pc-2018-04']

        if self.seasonValue:    
            url = APIFilter.buildSeasonFilter(inputURL, self.seasonValue, self.localPlayerObject.getPlayerID())
            apiUserStats.append(f"\'{self.seasonValue}' stats")
        else:
            url = APIFilter.buildLifeTimeFilter(inputURL, self.localPlayerObject.getPlayerID())
            apiUserStats.append(f"\tLifetime stats for {self.localPlayerObject.playerName} in {self.gameMode.upper()}")

        apiRequest = requests.get(url, headers=self.localPlayerObject.header)

        if apiRequest.status_code == 429:
            rateLimitReached()
            apiRequest = requests.get(url, headers=self.localPlayerObject.header)

        apiRequest.close()
        apiResponse = json.loads(apiRequest.text)
        
        if 'errors' in apiResponse:
            
            if user_settings.GUI:
                playerRegion = self.localPlayerObject.playerRegion
            else:
                playerRegion = input(f"Enter a region, one of the following:\n {[x for x in platformRegions]}\n")

            if playerRegion.lower() not in platformRegions:
                raise ValueError(f"Region isn't correct, it must be one of the following: {[x for x in platformRegions]}\n")
            else:
                for platform in platforms:
                    if platform in url:
                        url = url.replace(platform, playerRegion.lower())
                        apiRequest = requests.get(url, headers=self.localPlayerObject.header)
                        
                        if apiRequest.status_code == 429:
                            rateLimitReached()
                            apiRequest = requests.get(url, headers=self.localPlayerObject.header)
                            
                        apiRequest.close()
                        apiResponse = json.loads(apiRequest.text)
                        break
        
        for apiResponseGameMode in apiResponse['data']['attributes']['gameModeStats']:
        
            if self.gameMode == "all" or self.gameMode == "fpp" and apiResponseGameMode in fppOnlyGameModes or self.gameMode == "tpp" and apiResponseGameMode not in fppOnlyGameModes or  self.gameMode == apiResponseGameMode:
                apiUserStats.append("\t=================================")
                apiUserStats.append(f"\t{apiResponseGameMode.upper()} stats")
                apiUserStats.append(f"\t- Total of {apiResponse['data']['attributes']['gameModeStats'][apiResponseGameMode]['wins']} chicken dinners")
                apiUserStats.append(f"\t- Total of {apiResponse['data']['attributes']['gameModeStats'][apiResponseGameMode]['kills']} kills, with {apiResponse['data']['attributes']['gameModeStats'][apiResponseGameMode]['headshotKills']} being headshots")
                apiUserStats.append(f"\t- Averages {apiResponse['data']['attributes']['gameModeStats'][apiResponseGameMode]['dailyKills']} daily kills")
                apiUserStats.append(f"\t- Has dealt {apiResponse['data']['attributes']['gameModeStats'][apiResponseGameMode]['damageDealt']} damage")
                apiUserStats.append(f"\t- {apiResponse['data']['attributes']['gameModeStats'][apiResponseGameMode]['assists']} kill assists")            
                apiUserStats.append(f"\t- Longest kill of {apiResponse['data']['attributes']['gameModeStats'][apiResponseGameMode]['longestKill']}m")
                apiUserStats.append(f"\t- Highest kill-round of {apiResponse['data']['attributes']['gameModeStats'][apiResponseGameMode]['roundMostKills']} kills")
                
                ##Since SOLO/SOLO-FPP doesn't have team-mates, we can exclude this data.
                if apiResponseGameMode.upper() not in gameModesExcludedInOutput:
                    apiUserStats.append(f"\t- Downed {apiResponse['data']['attributes']['gameModeStats'][apiResponseGameMode]['dBNOs']} players")
                    apiUserStats.append(f"\t- Revived {apiResponse['data']['attributes']['gameModeStats'][apiResponseGameMode]['revives']} team-mates")
                    apiUserStats.append(f"\t- Accidentally killed {apiResponse['data']['attributes']['gameModeStats'][apiResponseGameMode]['teamKills']} team-mates")
                
                ##Makes sure we aren't printing null data about these stats to the console.
                if apiResponse['data']['attributes']['gameModeStats'][apiResponseGameMode]['rankPoints'] != 0 and apiResponse['data']['attributes']['gameModeStats'][apiResponseGameMode]['rankPointsTitle'] != 0:
                    apiUserStats.append(f"\t- Currently sits at {int(apiResponse['data']['attributes']['gameModeStats'][apiResponseGameMode]['rankPoints'])} rankpoints, with Title of {getSeasonRank(apiResponse['data']['attributes']['gameModeStats'][apiResponseGameMode]['rankPoints'])}")
                
                apiUserStats.append(f"\t- {apiResponse['data']['attributes']['gameModeStats'][apiResponseGameMode]['losses']} losses out of {apiResponse['data']['attributes']['gameModeStats'][apiResponseGameMode]['roundsPlayed']} games")
                apiUserStats.append(f"\t- Destroyed {apiResponse['data']['attributes']['gameModeStats'][apiResponseGameMode]['vehicleDestroys']} vehicles")
                apiUserStats.append(f"\t- Acquired {apiResponse['data']['attributes']['gameModeStats'][apiResponseGameMode]['weaponsAcquired']} weapons")
                apiUserStats.append(f"\t- Consumed {apiResponse['data']['attributes']['gameModeStats'][apiResponseGameMode]['boosts']} boosts")
                apiUserStats.append(f"\t- Consumed {apiResponse['data']['attributes']['gameModeStats'][apiResponseGameMode]['heals']} heals")
                apiUserStats.append(f"\t- Swam {apiResponse['data']['attributes']['gameModeStats'][apiResponseGameMode]['swimDistance']}m")

                ## ------------------  Variable Incremantation 
                self.totalWeaponsAcquired += apiResponse['data']['attributes']['gameModeStats'][apiResponseGameMode]['weaponsAcquired']
                self.totalAssists += apiResponse['data']['attributes']['gameModeStats'][apiResponseGameMode]['assists']
                self.totalVehiclesDestroyed += apiResponse['data']['attributes']['gameModeStats'][apiResponseGameMode]['vehicleDestroys']
                self.totalTeamkills += apiResponse['data']['attributes']['gameModeStats'][apiResponseGameMode]['teamKills']
                self.totalRevives += apiResponse['data']['attributes']['gameModeStats'][apiResponseGameMode]['revives']
                self.totalKills += apiResponse['data']['attributes']['gameModeStats'][apiResponseGameMode]['kills']
                self.totalHeadshotKills += apiResponse['data']['attributes']['gameModeStats'][apiResponseGameMode]['headshotKills']
                self.totalRoundsPlayed += apiResponse['data']['attributes']['gameModeStats'][apiResponseGameMode]['roundsPlayed']
                self.totalHeals += apiResponse['data']['attributes']['gameModeStats'][apiResponseGameMode]['heals']
                self.totalDamage += apiResponse['data']['attributes']['gameModeStats'][apiResponseGameMode]['damageDealt']
                self.totalEnemyDowns += apiResponse['data']['attributes']['gameModeStats'][apiResponseGameMode]['dBNOs']
                self.totalBoosts += apiResponse['data']['attributes']['gameModeStats'][apiResponseGameMode]['boosts']
                self.totalAssists += apiResponse['data']['attributes']['gameModeStats'][apiResponseGameMode]['assists']
                self.totalChickenDinners += apiResponse['data']['attributes']['gameModeStats'][apiResponseGameMode]['wins']
                ## Variable Incremantation ------------------ ##

        ## Since the API just returns a blank fucking JSON file for a player which isn't in a season... we have to find some way to differentiate between a player which was around in this season, and not. This is the only way i could find.
        if self.seasonValue and self.totalWeaponsAcquired == 0 and self.totalAssists == 0 and self.totalVehiclesDestroyed  == 0 and self.totalRevives  == 0 and self.totalKills  == 0 and self.totalHeadshotKills == 0 and self.totalHeals  == 0 and self.totalDamage  == 0 and self.totalEnemyDowns  == 0 and self.totalBoosts  == 0 and self.totalAssists == 0:
            seasonStatsNotFound(self.seasonValue, self.localPlayerObject.playerName)
            dataExists = False

        if dataExists:
            if self.seasonValue and user_settings.GUI:
                fileName = f'DATA/{self.seasonValue}-Stats.txt'
            elif not self.seasonValue and user_settings.GUI:
                fileName = f'DATA/Lifetime-{self.localPlayerObject.playerName}-{self.gameMode.upper()}-Stats.txt'
            
            if user_settings.GUI:
                with open(fileName, 'w+', encoding='utf-8') as f:
                    for outputLine in apiUserStats:
                        f.write(outputLine+'\n')

                    if self.gameMode in gameModeTypes:
                        f.write(f"\t=================================\n\t- Total of {self.totalKills} kills\n\t- Total of {self.totalChickenDinners} chicken dinners\n\t- Total of {self.totalHeadshotKills} headshots\n\t- Total of {round(self.totalDamage,2)} damage dealt\n\t- Total of {self.totalAssists} assists\n\t- Total of {self.totalEnemyDowns} player knocks\n\t- Total of {self.totalBoosts} boosts consumed\n\t- Total of {self.totalHeals} heals consumed\n\t- Total of {self.totalTeamkills} team-kills\n\t- Total of {self.totalVehiclesDestroyed} vehicles destroyed\n\t- Total of {self.totalWeaponsAcquired} weapons acquired\n\t- Total of {self.totalRevives} revives\n")
            else:
                print('\n')
                for outputLine in apiUserStats:
                    print(outputLine)
        
                if self.gameMode in gameModeTypes:
                    print(f"\t=================================\n\t- Total of {self.totalKills} kills\n\t- Total of {self.totalChickenDinners} chicken dinners\n\t- Total of {self.totalHeadshotKills} headshots\n\t- Total of {round(self.totalDamage,2)} damage dealt\n\t- Total of {self.totalAssists} assists\n\t- Total of {self.totalEnemyDowns} player knocks\n\t- Total of {self.totalBoosts} boosts consumed\n\t- Total of {self.totalHeals} heals consumed\n\t- Total of {self.totalTeamkills} team-kills\n\t- Total of {self.totalVehiclesDestroyed} vehicles destroyed\n\t- Total of {self.totalWeaponsAcquired} weapons acquired\n\t- Total of {self.totalRevives} revives\n")
                else:
                    print('\n')


