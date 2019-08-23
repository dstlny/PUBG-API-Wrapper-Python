# import pythons requests, json, sys, ps amd datetime lib
from config import user_settings
from exceptions.connectionTimeOut import connectionTimeOut
from exceptions.seasonStatsNotFound import seasonStatsNotFound
from exceptions.playerNotFound import playerNotFound
from exceptions.rateLimit import rateLimitReached
from parsers.APIResponse import APIResponse
from utility.endpoint.filters import APIFilter
from helper.helperFunctions import returnMapName, getSeasonRank
import requests, json, sys, xlsxwriter

from os import(
    path, 
    system
)

from datetime import datetime
from time import sleep

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

# Import my tools to be used

# Import exceptions that can be defined


class D(dict):
    def __missing__(self, key):
        self[key] = D()
        return self[key]


class player():
    '''
        1. Describes the Player you want to lookup.

        2. Holds player stats - such as Account playerID, Account Name, and a list of recent Match playerID's
    '''

    if user_settings.GUI:

        def __init__(self, inputHeader, inputRegion):
            self.header = inputHeader
            self.playerID = ""
            self.playerName = ""
            self.matchIDS = list()
            self.seasonValues = list()
            self.playerRegion = inputRegion

    else:

        def __init__(self, inputHeader):
            self.header = inputHeader
            self.playerID = ""
            self.playerName = ""
            self.matchIDS = list()
            self.seasonValues = list()

    def getAccountID(self, inputPlayerName, inputURL, inputNoOfMatches, lifeTimeOrNot: bool):
        '''
            Grabs the users Account playerID based on the API's response from the users name. Sets up the Player object.

            playerName - the players name (case-sensitive)

            inputURL - the API's base URL

            inputNoOfMatches - an integer representing the number of matches that you want to display - which is passed on to processPlayerObject().
            This also seems to be unique per player.

            lifeTimeOrNot - bool representing whether it's a lifetime or seasonal request
        '''
        playerURL = APIFilter.buildPlayerFilter(inputURL, inputPlayerName)

        try:
            playerAPIRequest = requests.get(playerURL, headers=self.header)
            playerAPIRequest.close()
        except Exception as Excep:
            connectionTimeOut(Excep)

        self.playerName = inputPlayerName

        apiResponse = json.loads(playerAPIRequest.text)

        if 'errors' in apiResponse:
            playerNotFound(inputPlayerName)
            return False
        else:

            matches = []

            for matchID in apiResponse['data'][0]['relationships']['matches']['data']:
                if not lifeTimeOrNot and len(matches) < inputNoOfMatches and matchID['id'] is not None:
                    matches.append(matchID['id'])

            self.playerID = apiResponse['data'][0]['id']

            if len(matches) != 0 and not lifeTimeOrNot:
                self.setMatches(matches)

            return True

    def seasonStats(self, inputURL, inputGameMode, inputSeason):
        '''
            Proccesses and displays the users lifetime stats.

            apiResponse is the PUBG API's response.

            inputNoOfMatches is an integer representing the number of matches you want to display.

            inputSeason - SEASON playerID

        '''

        localSeasons = APIResponse(inputGameMode, self, seasonValue=inputSeason)
        localSeasons.parseJSONSeasonAndLifetimeResponse(inputURL)

    def lifetimeStats(self, inputURL, inputGameMode):
        '''
            Proccesses and displays the users lifetime stats.

            apiResponse is the PUBG API's response.

            inputNoOfMatches is an integer representing the number of matches you want to display.

            inputSeason - SEASON playerID

        '''

        localSeasons = APIResponse(inputGameMode, self)
        localSeasons.parseJSONSeasonAndLifetimeResponse(inputURL)

    def setAccountID(self, inputPlayerID):
        self.playerID = inputPlayerID

    def getPlayerID(self):
        return self.playerID

    def setPlayerName(self, name):
        self.playerName = name

    def getPlayerName(self):
        return self.playerName

    def setMatches(self, matches: list):

        if isinstance(matches, list):
            [self.matchIDS.append(x) for x in matches]
        else:
            raise TypeError("Matches must be of type List")

    def getMatches(self):
        return self.matchIDS

    def displayMatches(self, inputURL):
        '''
            Displays a number of matches.
        '''

        matchDates = []
        matchDamage = []
        matchMap = []
        matchGameMode = []
        matchPlacement = []
        matchKills = []

        totalWinCount = 0
        totalKillCount = 0
        totalDamageCount = 0
        i = 0

        excelXCol = []
        excelYCol = []

        for matchID in self.getMatches():

            url = inputURL + APIFilter.MATCH_FILTER.value.replace('$matchID', matchID)

            matchEndpointRequest = requests.get(url, headers=self.header)

            if matchEndpointRequest.status_code == 429:
                rateLimitReached()
                matchEndpointRequest = requests.get(url, headers=self.header)
                matchEndpointRequest.close()

            matchEndpointResponse = json.loads(matchEndpointRequest.text)

            if matchEndpointResponse['data']['attributes']['mapName'] == 'Range_Main':
                continue
            else:

                matchTimeData = datetime.strptime(matchEndpointResponse['data']['attributes']['createdAt'].replace('Z', ''), "%Y-%m-%dT%H:%M:%S")

                matchDates.append(str(matchTimeData.strftime('%m/%d/%Y')))

                matchMap.append(returnMapName(matchEndpointResponse['data']['attributes']['mapName']))

                matchGameMode.append(matchEndpointResponse['data']['attributes']['gameMode'].upper())

                for playerStat in matchEndpointResponse['included']:

                    if 'stats' in playerStat['attributes'] and 'playerId' in playerStat['attributes']['stats'] and playerStat['attributes']['stats']['playerId'] == self.getPlayerID():

                        matchDamage.append(round(playerStat['attributes']['stats']['damageDealt'], 2))

                        matchPlacement.append(f"{playerStat['attributes']['stats']['winPlace']}/100")

                        matchKills.append(f"{playerStat['attributes']['stats']['kills']}")

                        break
            i+=1
            print(f"Match request {i} completed...")

        excelYCol = set()

        for matchPlacementStr, matchKillStr, matchDamageStr, matchDateStr in zip(matchPlacement, matchKills, matchDamage, matchDates):
            totalKillCount += int(matchKillStr.replace('kills', '').strip())
            totalDamageCount += matchDamageStr
            excelYCol.add(matchDateStr)
            if matchPlacementStr == '1/100':
                totalWinCount += 1

        localKillsForDateCount = 0

        # This will be the dataset we use.
        dateDict = D({
            'dates': {

            }
        })

        totalKillsForDates = []

        del i

        for i, x in enumerate(matchDates):

            if i+1 <= len(matchDates)-1:

                if x == matchDates[i+1]:
                    localKillsForDateCount += int(matchKills[i])
                else:
                    dateDict['dates'][x] = localKillsForDateCount
                    totalKillsForDates.append(localKillsForDateCount)
                    localKillsForDateCount = 0

            else:

                if x == matchDates[len(matchDates)-1]:
                    localKillsForDateCount += int(matchKills[i])
                    dateDict['dates'][x] = localKillsForDateCount
                    totalKillsForDates.append(localKillsForDateCount)
                    localKillsForDateCount = 0

        excelDataStartLOC = [0, 0]  # xlsxwriter rquires list, no tuple
        excelDataEndLOC = [excelDataStartLOC[0] + len(dateDict['dates'])-1, 0]

        workbook = xlsxwriter.Workbook(f'DATA/{self.playerName}-{len(matchMap)}Matches.xlsx')

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
            'name': f'Amount of kills from {min(excelYCol)} - {max(excelYCol)}'
        })

        worksheet = workbook.add_worksheet()

        # A chart requires data to reference data insplayerIDe excel
        worksheet.write_column(*excelDataStartLOC, data=reversed(totalKillsForDates))
        chart.add_series({
            'values': [worksheet.name] + excelDataStartLOC + excelDataEndLOC,
            'name': "Kills",
        })

        worksheet.insert_chart('B1', chart)
        workbook.close()  # Write to file

        if user_settings.GUI:

            fileName = f'DATA/{self.playerName}-{len(matchMap)}Matches.csv'

            with open(fileName, 'w+', encoding="utf-8") as f:
                f.write('{},{},{},{},{},{},{}\n'.format('MATCH', 'DATE','PLACEMENT', 'MAP', 'MODE', 'DAMAGE', 'KILLS'))
                for i, item in enumerate(zip(matchDates, matchPlacement, matchMap, matchGameMode, matchDamage, matchKills)):
                    f.write('{},{},{},{},{},{},{}\n'.format(i+1, *item))
                f.write(
                    f'\n  Stats for {self.playerName} accross {len(matchMap)} matches\n  - Won {totalWinCount} out of {len(matchMap)} games\n  - Averages {round(totalKillCount / len(matchKills), 2)} kills per game\n  - Total of {totalKillCount} kills and {round(totalDamageCount,2)} damage across {round(len(matchKills), 2)} matches\n  - Highest kill game of {max(matchKills)} in {matchGameMode[matchKills.index(max(matchKills))]}\n')

        else:

            print('\n|-------------------------------------------------------------------------------------------------------------------|\n| {:<5} | {:<15} | {:<15} | {:<15} | {:<15} | {:<15} | {:<15} |'.format(
                'MATCH', 'DATE', 'PLACEMENT', 'MAP', 'MODE', 'DAMAGE', 'KILLS')+'\n|-------------------------------------------------------------------------------------------------------------------|')
            for i, item in enumerate(zip(matchDates, matchPlacement, matchMap, matchGameMode, matchDamage, matchKills)):
                print('| {:<5} | {:<15} | {:<15} | {:<15} | {:<15} | {:<15} | {:<15} |\n|-------------------------------------------------------------------------------------------------------------------|'.format(i+1, *item))
            print('| {:<5} | {:<15} | {:<15} | {:<15} | {:<15} | {:<15} | {:<15} |\n|-------------------------------------------------------------------------------------------------------------------|\n'.format(
                'MATCH', 'DATE', 'PLACEMENT', 'MAP', 'MODE', 'DAMAGE', 'KILLS'))
            print(
                f'\n  Stats for {self.playerName} accross {len(matchMap)} matches\n  - Won {totalWinCount} out of {len(matchMap)} games\n  - Averages {round(totalKillCount / len(matchKills), 2)} kills per game\n  - Total of {totalKillCount} kills and {round(totalDamageCount,2)} damage across {round(len(matchKills), 2)} matches\n  - Highest kill game of {max(matchKills)} in {matchGameMode[matchKills.index(max(matchKills))]}\n')
