##Import my tools to be used
from utility.platforms.platform_shards import Shard
from objects.player import player
from utility.endpoint.filters import APIFilter
from config.APIConfig import APIConfig
from config.APISettings import APISettings
from config import user_settings

#import pythons Time lib
import time, json

class API_INTERFACE():

    def matchStats(playerName: str, platform: str, authheader, amount: int):
        '''
            Wrapper for a quick breakdown of player stats over a number of matches. 
            Also prints a table including each of these matches out to the console.
            playerName - the players name that you want to produce a quick breakdown of over a number matches (case-sensitive)
            platform - the platform the player is playing on, can be one of the following:
            - XBOX / xbox
            - PC / pc
            - PSN / psn
            - KAKAO / kakao
            authheader - the header we will use to contact the API.
            amount - amount of matches you want to display. 
            The amount of time the script will take to process the data, scales linearly with this.
        '''
        
        url = Shard.buildURL(platform)

        playerObject = player(authheader)
        playerObject.getAccountID(playerName, url, amount, False)
        playerObject.displayMatches(url)

    def lifetimeStats(playerName: str, platform: str, authheader, gameplayerMode):
        '''
            Wrapper for lifetime stats.
            playerName - the players name you want to lookup the lifetime stats of (case-sensitive)
            platform - the platform the player is playing on, can be one of the following:
            - XBOX / xbox
            - PC / pc
            - PSN / psn
            - KAKAO / kakao
            authheader - the header we will use to contact the API.
            gameplayerMode - the game mode you want to lookup, one of the following:
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

        url = Shard.buildURL(platform)

        playerObject = player(authheader)
        playerObject.getAccountID(playerName, url, 0, True)
        playerObject.lifetimeStats(url, gameplayerMode.lower())

    def seasonStats(playerName: str, platform: str, authheader, gameplayerMode, seasonValue):
        '''
            Wrapper for lifetime stats.
            playerName - the players name you want to lookup the lifetime stats of (case-sensitive)
            platform - the platform the player is playing on, can be one of the following:
            - XBOX / xbox
            - PC / pc
            - PSN / psn
            - KAKAO / kakao
            authheader - the header we will use to contact the API.
            gameplayerMode - the game mode you want to lookup, one of the following:
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

        url = Shard.buildURL(platform)

        playerObject = player(authheader)
        playerObject.getAccountID(playerName, url, 0, True)
        playerObject.seasonStats(url, gameplayerMode.lower(), seasonValue)

if user_settings.GUI:

    import wx

    class AppFrame(wx.Frame):

        def __init__(self, *args, **kw):
            """Constructor for this class"""

            # ensure the parent"s __init__ is called
            super(AppFrame, self).__init__(*args, **kw)
            # and a status bar
            self.CreateStatusBar()
            self.SetStatusText("Welcome!")
            self.SetSize(480, 250)
            self.SetMaxSize((690, 250))
            self.SetMinSize((480, 250))
            self.mainPanel()

        def mainPanel(self):
            # Setting up the panel and stuff.
            self.mainPanel = wx.Panel(self)
            self.mainPanel.SetBackgroundColour(wx.WHITE)

            self.gameModes = ['duo', 'squad', 'solo', 'duo-fpp', 'squad-fpp', 'solo-fpp', 'all', 'fpp', 'tpp']

            self.pcRegions = ['pc-eu', 'pc-as', 'pc-na', 'pc-oc', 'pc-jp', 'pc-krjp', 'pc-ru', 'pc-sa','pc-sea','pc-kakao']
            self.pcSeasons = ['division.bro.official.2017-beta','division.bro.official.2017-pre1', 'division.bro.official.2017-pre2', 'division.bro.official.2017-pre3','division.bro.official.2017-pre4','division.bro.official.2017-pre5','division.bro.official.2017-pre6','division.bro.official.2017-pre7','division.bro.official.2017-pre8','division.bro.official.2017-pre9','division.bro.official.2018-01', 'division.bro.official.2018-02','division.bro.official.2018-03','division.bro.official.2018-04','division.bro.official.2018-05','division.bro.official.2018-06','division.bro.official.2018-07','division.bro.official.2018-08','division.bro.official.2018-09','division.bro.official.pc-2018-01', 'division.bro.official.pc-2018-02','division.bro.official.pc-2018-03','division.bro.official.pc-2018-04']
            
            self.psnRegions = ['psn-as','psn-eu','psn-na','psn-oc']
            self.psnSeasons =['division.bro.official.2018-09',
                            'division.bro.official.playstation-01',
                            'division.bro.official.playstation-02']
            
            self.xboxRegions = ['xbox-as','xbox-eu','xbox-na','xbox-oc', 'xbox-na']
            self.xboxSeasons = ['division.bro.official.2018-05',
                            'division.bro.official.2018-06',
                            'division.bro.official.2018-07',
                            'division.bro.official.2018-08',
                            'division.bro.official.xbox-01',
                            'division.bro.official.xbox-02',
                            'division.bro.official.xb-pre1']
            
            self.platforms = ['PC','XBOX','PSN']
            self.optionChoices = ['Lifetime Statisics', 'Specific Season', 'X Matches']

            self.outerBox = wx.StaticBox(self.mainPanel, wx.ID_ANY, "Platform, Region, Token, Player details and option", size=(440, 125), pos=(10,10))
            self.platformSelect = wx.RadioBox(self.mainPanel, wx.ID_ANY, label="Platform", pos=(20,30), choices=self.platforms, style=wx.RA_SPECIFY_ROWS)

            self.regionLabel = wx.StaticText(self.mainPanel, wx.ID_ANY, label="Region", pos=(100,30))
            self.regionDropDown = wx.ComboBox(self.mainPanel, wx.ID_ANY, value="", choices=self.pcRegions, pos=(100,50))

            self.gameModeLabel = wx.StaticText(self.mainPanel, wx.ID_ANY, label="Game Mode", pos=(100,80))
            self.gameModeDrop= wx.ComboBox(self.mainPanel, wx.ID_ANY, value="", choices=self.gameModes, pos=(100,100))


            self.apiTokenLabel= wx.StaticText(self.mainPanel, wx.ID_ANY, label="API Token", pos=(200,30))

            if APISettings.API_TOKEN != "":
                self.apiTokenBox = wx.TextCtrl(self.mainPanel, wx.ID_ANY, value=APISettings.API_TOKEN, pos=(200,50))
            else:
                self.apiTokenBox = wx.TextCtrl(self.mainPanel, wx.ID_ANY, value="", pos=(200,50))

            self.playerNameLabel= wx.StaticText(self.mainPanel, wx.ID_ANY, label="Player Name", pos=(200,80))

            if user_settings.PLAYER_NAME != "":
                self.playerNameBox = wx.TextCtrl(self.mainPanel, wx.ID_ANY, value=user_settings.PLAYER_NAME, pos=(200,100))
            else:
                self.playerNameBox = wx.TextCtrl(self.mainPanel, wx.ID_ANY, value="", pos=(200,100))

            self.optionChoicesSelect = wx.RadioBox(self.mainPanel, wx.ID_ANY, label="Options", pos=(320,30), choices=self.optionChoices, style=wx.RA_SPECIFY_ROWS)

            self.seasonLabel = wx.StaticText(self.mainPanel, wx.ID_ANY, label="Season", pos=(450,30))
            self.seasonDropDown = wx.ComboBox(self.mainPanel, wx.ID_ANY, value="", choices=self.pcSeasons, pos=(450,50))

            self.noOfMatchesLabel = wx.StaticText(self.mainPanel, wx.ID_ANY, label="No of Matches", pos=(450,30))
            
            if user_settings.MATCH_INTEGER != 0:
                self.noOfMatches = wx.TextCtrl(self.mainPanel, wx.ID_ANY, value=str(user_settings.MATCH_INTEGER), pos=(450,50))
            else:
                self.noOfMatches = wx.TextCtrl(self.mainPanel, wx.ID_ANY, value="", pos=(450,50))
            
            self.submitButton = wx.Button(self.mainPanel, wx.ID_ANY, label="Query PUBG API", pos=(10,140), size=(440, 40))
            
            self.seasonLabel.Hide()
            self.seasonDropDown.Hide()
            self.noOfMatchesLabel.Hide()
            self.noOfMatches.Hide()

            self.Bind(wx.EVT_RADIOBOX, self.hideOrShowRegion, source=self.platformSelect)
            self.Bind(wx.EVT_RADIOBOX, self.changeRegionContent, source=self.optionChoicesSelect)
            self.Bind(wx.EVT_RADIOBOX, self.changeSeasonOrRegionCont, source=self.platformSelect)
            self.Bind(wx.EVT_BUTTON, self.submitButtonQuery, source=self.submitButton)

        def hideOrShowRegion(self, bool1, bool2):
            
            if bool1:
                self.seasonLabel.Show()
                self.seasonDropDown.Show()
            else:
                self.seasonLabel.Hide()
                self.seasonDropDown.Hide()

            if bool2:
                self.noOfMatchesLabel.Show()
                self.noOfMatches.Show()
            else:
                self.noOfMatchesLabel.Hide()
                self.noOfMatches.Hide()

        def submitButtonQuery(self, evt):
            
            start_time = time.time()
            header = APIConfig(APISettings.API_TOKEN).setupAuth()        
            platformChoice = self.platformSelect.GetItemLabel(self.platformSelect.GetSelection())

            url = Shard.buildURL(platformChoice)

            if not self.regionDropDown.GetValue():
                self.SetStatusText(f"ERROR: Region cannot be empty!")
                return

            if not self.gameModeDrop.GetValue():
                self.SetStatusText(f"ERROR: Game Mode cannot be empty!")
                return

            if not self.apiTokenBox.GetValue():
                self.SetStatusText(f"ERROR: API Token cannot be empty!")
                return

            if not self.playerNameBox.GetValue():
                self.SetStatusText(f"ERROR: Players Name cannot be empty!")
                return
            
            playerRegion = self.regionDropDown.GetValue()
            playerObject = player(header, playerRegion)
            playerMode = self.gameModeDrop.GetValue()
            playerName = self.playerNameBox.GetValue()

            if self.optionChoicesSelect.GetSelection() == 0:
                
                self.SetStatusText(f"Requesting and Parsing PUBG API Lifetime request for {playerName}...")

                if playerObject.getAccountID(playerName, url, 0, True) != False:
                    playerObject.lifetimeStats(url, playerMode.lower())

            elif self.optionChoicesSelect.GetSelection() == 1:
                
                if not self.seasonDropDown.GetValue():
                    self.SetStatusText(f"ERROR: You must select a season!")
                    return 
                else:
                    
                    seasonValue = self.seasonDropDown.GetValue()

                    self.SetStatusText(f"Requesting and Parsing PUBG API season data for season {seasonValue}...")

                    if playerObject.getAccountID(playerName, url, 0, False) != False:
                        playerObject.seasonStats(url, playerMode.lower(), seasonValue)

            elif self.optionChoicesSelect.GetSelection() == 2:

                if not self.noOfMatches.GetValue():
                    self.SetStatusText(f"ERROR: Cannot enter non-numeric characters in no-of-matches box!")
                    return 
                else:

                    matchAmountValue = self.noOfMatches.GetValue()

                    self.SetStatusText(f"Requesting and Parsing {matchAmountValue} match responses from PUBG API... if this hangs it's fine")

                    if playerObject.getAccountID(playerName, url, int(matchAmountValue), False) != False:
                        playerObject.displayMatches(url)
                    
            self.SetStatusText(f"Took {time.time() - start_time} seconds to complete parsing data...")

        def changeSeasonOrRegionCont(self, evt):
            if self.platformSelect.GetSelection() == 0:
                self.clearAndAppend(self.regionDropDown, self.pcRegions, self.seasonDropDown, self.pcSeasons)
            elif self.platformSelect.GetSelection() == 1:
                self.clearAndAppend(self.regionDropDown, self.xboxRegions, self.seasonDropDown, self.xboxSeasons)
            elif self.platformSelect.GetSelection() == 2:
                self.clearAndAppend(self.regionDropDown, self.psnRegions, self.seasonDropDown, self.psnSeasons)

        def clearAndAppend(self, obj1, obj1_item, obj2, obj2_item):
            obj1.Clear()
            obj1.AppendItems(obj1_item)
            obj2.Clear()
            obj2.AppendItems(obj2_item)
            
        def changeRegionContent(self, evt):
            
            if self.optionChoicesSelect.GetSelection() == 0:
                self.hideOrShowRegion(False, False)
                self.outerBox.SetSize(440, 125)
                self.SetSize(480, 250)
                self.submitButton.SetSize(440, 40)
            elif self.optionChoicesSelect.GetSelection() == 1:
                self.hideOrShowRegion(True, False)
                self.outerBox.SetSize(650, 125)
                self.SetSize(690,250)
                self.submitButton.SetSize(650, 40)
            elif self.optionChoicesSelect.GetSelection() == 2:
                self.hideOrShowRegion(False, True)
                self.outerBox.SetSize(560, 125)
                self.SetSize(600,250)
                self.submitButton.SetSize(560, 40)

    # Main program loop
    def main():
        """"Sets up the programs main window"""
        app = wx.App()
        frm = AppFrame(None, title="PUBG Developer API GUI Wrapper")
        frm.Show()
        app.MainLoop()

    # Main main, but it"s ugly, thus the redirect
    if __name__ == "__main__":
        main()

else:

    with open('user_input.py', 'w+', encoding='utf-8') as f:
        f.write(user_settings._PYTHON_FILE_CONTENTS)

    exec(open('user_input.py').read())