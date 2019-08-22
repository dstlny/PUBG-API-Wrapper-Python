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
            Wrapper for season stats.
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
            _season - the season you want to query the API for.
        '''

        _URL = Shard.buildURL(platform)

        _player_object = player(auth_header)
        _player_object.getAccountID(playerName, _URL, 0, True)
        _player_object.seasonStats(_URL, game_mode.lower(), _season)

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

            self._GAMEMODES = ['duo', 'squad', 'solo', 'duo-fpp', 'squad-fpp', 'solo-fpp', 'all', 'fpp', 'tpp']

            self._PC_REGIONS = ['pc-eu', 'pc-as', 'pc-na', 'pc-oc', 'pc-jp', 'pc-krjp', 'pc-ru', 'pc-sa','pc-sea','pc-kakao']
            self._PC_SEASONS = ['division.bro.official.2017-beta','division.bro.official.2017-pre1', 'division.bro.official.2017-pre2', 'division.bro.official.2017-pre3','division.bro.official.2017-pre4','division.bro.official.2017-pre5','division.bro.official.2017-pre6','division.bro.official.2017-pre7','division.bro.official.2017-pre8','division.bro.official.2017-pre9','division.bro.official.2018-01', 'division.bro.official.2018-02','division.bro.official.2018-03','division.bro.official.2018-04','division.bro.official.2018-05','division.bro.official.2018-06','division.bro.official.2018-07','division.bro.official.2018-08','division.bro.official.2018-09','division.bro.official.pc-2018-01', 'division.bro.official.pc-2018-02','division.bro.official.pc-2018-03','division.bro.official.pc-2018-04']
            
            self._PSN_REGIONS = ['psn-as','psn-eu','psn-na','psn-oc']
            self._PSN_SEASONS =['division.bro.official.2018-09',
                            'division.bro.official.playstation-01',
                            'division.bro.official.playstation-02']
            
            self._XBOX_REGIONS = ['xbox-as','xbox-eu','xbox-na','xbox-oc', 'xbox-na']
            self._XBOX_SEASONS = ['division.bro.official.2018-05',
                            'division.bro.official.2018-06',
                            'division.bro.official.2018-07',
                            'division.bro.official.2018-08',
                            'division.bro.official.xbox-01',
                            'division.bro.official.xbox-02',
                            'division.bro.official.xb-pre1']
            
            self._PLATFORMS = ['PC','XBOX','PSN']
            self._CHOICES = ['Lifetime Statisics', 'Specific Season', 'X Matches']

            self.outer = wx.StaticBox(self.mainPanel, wx.ID_ANY, "Platform, Region, Token, Player details and option", size=(440, 125), pos=(10,10))
            self._PLATFORM_SELECT = wx.RadioBox(self.mainPanel, wx.ID_ANY, label="Platform", pos=(20,30), choices=self._PLATFORMS, style=wx.RA_SPECIFY_ROWS)

            self.regionLabel = wx.StaticText(self.mainPanel, wx.ID_ANY, label="Region", pos=(100,30))
            self.regionDropDown = wx.ComboBox(self.mainPanel, wx.ID_ANY, value="", choices=self._PC_REGIONS, pos=(100,50))

            self.gameModeLabel = wx.StaticText(self.mainPanel, wx.ID_ANY, label="Game Mode", pos=(100,80))
            self.gameModeDrop= wx.ComboBox(self.mainPanel, wx.ID_ANY, value="", choices=self._GAMEMODES, pos=(100,100))


            self.apiTokenLabel= wx.StaticText(self.mainPanel, wx.ID_ANY, label="API Token", pos=(200,30))

            if APISettings.API_TOKEN != "":
                self.apiTokenBox= wx.TextCtrl(self.mainPanel, wx.ID_ANY, value=APISettings.API_TOKEN, pos=(200,50))
            else:
                self.apiTokenBox= wx.TextCtrl(self.mainPanel, wx.ID_ANY, value="", pos=(200,50))

            self.playerNameLabel= wx.StaticText(self.mainPanel, wx.ID_ANY, label="Player Name", pos=(200,80))

            if user_settings.PLAYER_NAME != "":
                self.playerNameBox= wx.TextCtrl(self.mainPanel, wx.ID_ANY, value=user_settings.PLAYER_NAME, pos=(200,100))
            else:
                self.playerNameBox= wx.TextCtrl(self.mainPanel, wx.ID_ANY, value="", pos=(200,100))

            self._CHOICES_SELECT = wx.RadioBox(self.mainPanel, wx.ID_ANY, label="Options", pos=(320,30), choices=self._CHOICES, style=wx.RA_SPECIFY_ROWS)

            self.seasonLabel = wx.StaticText(self.mainPanel, wx.ID_ANY, label="Season", pos=(450,30))
            self.seasonDropDown = wx.ComboBox(self.mainPanel, wx.ID_ANY, value="", choices=self._PC_SEASONS, pos=(450,50))

            self.noOfMatchesLabel = wx.StaticText(self.mainPanel, wx.ID_ANY, label="No of Matches", pos=(450,30))
            
            if user_settings.MATCH_INTEGER != 0:
                self.noOfMatches = wx.TextCtrl(self.mainPanel, wx.ID_ANY, value=str(user_settings.MATCH_INTEGER), pos=(450,50))
            else:
                self.noOfMatches = wx.TextCtrl(self.mainPanel, wx.ID_ANY, value="", pos=(450,50))
            
            self.submit = wx.Button(self.mainPanel, wx.ID_ANY, label="Query PUBG API", pos=(10,140), size=(440, 40))
            
            self.seasonLabel.Hide()
            self.seasonDropDown.Hide()
            self.noOfMatchesLabel.Hide()
            self.noOfMatches.Hide()

            self.Bind(wx.EVT_RADIOBOX, self.hideOrShowRegion, source=self._PLATFORM_SELECT)
            self.Bind(wx.EVT_RADIOBOX, self.changeRegionContent, source=self._CHOICES_SELECT)
            self.Bind(wx.EVT_RADIOBOX, self.changeSeasonOrRegionCont, source=self._PLATFORM_SELECT)
            self.Bind(wx.EVT_BUTTON, self.submitQuery, source=self.submit)

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

        def submitQuery(self, evt):
            
            start_time = time.time()
            _HEADER = APIConfig(APISettings.API_TOKEN).setupAuth()        
            _PLAT_CHOICE = self._PLATFORM_SELECT.GetItemLabel(self._PLATFORM_SELECT.GetSelection())

            _URL = Shard.buildURL(_PLAT_CHOICE)

            if self.regionDropDown.GetValue() != "":
                
                _REGION = self.regionDropDown.GetValue()
                _player_object = player(_HEADER, _REGION)

                if self.gameModeDrop.GetValue() != "":

                    _MODE = self.gameModeDrop.GetValue()

                    if self.apiTokenBox.GetValue() != "":

                        _TOKEN = self.apiTokenBox.GetValue()

                        if self.playerNameBox.GetValue() != "":

                            _PLAYER = self.playerNameBox.GetValue()

                            if self._CHOICES_SELECT.GetSelection() == 0:
                                
                                self.SetStatusText(f"Requesting and Parsing PUBG API Lifetime request for {_PLAYER}...")

                                if _player_object.getAccountID(_PLAYER, _URL, 0, True) != False:
                                    _player_object.lifetimeStats(_URL, _MODE.lower())

                            elif self._CHOICES_SELECT.GetSelection() == 1:
                                
                                if self.seasonDropDown.GetValue() != "":
                                    
                                    _SEASON = self.seasonDropDown.GetValue()

                                    self.SetStatusText(f"Requesting and Parsing PUBG API season data for season {_SEASON}...")

                                    if _player_object.getAccountID(_PLAYER, _URL, 0, False) != False:
                                        _player_object.seasonStats(_URL, _MODE.lower(), _SEASON)

                                else:
                                    self.SetStatusText(f"ERROR: Cannot enter non-numeric characters in no-of-matches box!")

                            elif self._CHOICES_SELECT.GetSelection() == 2:

                                if self.noOfMatches.GetValue() != "":

                                    _AMOUNT = self.noOfMatches.GetValue()

                                    self.SetStatusText(f"Requesting and Parsing {_AMOUNT} match responses from PUBG API... if this hangs it's fine")

                                    if _player_object.getAccountID(_PLAYER, _URL, int(_AMOUNT), False) != False:
                                        _player_object.displayMatches(_URL)

                        else:
                            self.SetStatusText(f"ERROR: Players name cannot be empty!")

                    else:
                        self.SetStatusText(f"ERROR: API TOKEN cannot be empty!")

                else:
                    self.SetStatusText(f"ERROR: Game Mode cannot be empty!")

            else:
                self.SetStatusText(f"ERROR: Region cannot be empty!")

            self.SetStatusText(f"Took {time.time() - start_time} seconds to complete parsing data...")

        def changeSeasonOrRegionCont(self, evt):
            if self._PLATFORM_SELECT.GetSelection() == 0:
                self.clearAndAppend(self.regionDropDown, self._PC_REGIONS, self.seasonDropDown, self._PC_SEASONS)
            elif self._PLATFORM_SELECT.GetSelection() == 1:
                self.clearAndAppend(self.regionDropDown, self._XBOX_REGIONS, self.seasonDropDown, self._XBOX_SEASONS)
            elif self._PLATFORM_SELECT.GetSelection() == 2:
                self.clearAndAppend(self.regionDropDown, self._PSN_REGIONS, self.seasonDropDown, self._PSN_SEASONS)

        def clearAndAppend(self, obj1, obj1_item, obj2, obj2_item):
            obj1.Clear()
            obj1.AppendItems(obj1_item)
            obj2.Clear()
            obj2.AppendItems(obj2_item)
            
        def changeRegionContent(self, evt):
            
            if self._CHOICES_SELECT.GetSelection() == 0:
                self.hideOrShowRegion(False, False)
                self.outer.SetSize(440, 125)
                self.SetSize(480, 250)
                self.submit.SetSize(440, 40)
            elif self._CHOICES_SELECT.GetSelection() == 1:
                self.hideOrShowRegion(True, False)
                self.outer.SetSize(650, 125)
                self.SetSize(690,250)
                self.submit.SetSize(650, 40)
            elif self._CHOICES_SELECT.GetSelection() == 2:
                self.hideOrShowRegion(False, True)
                self.outer.SetSize(560, 125)
                self.SetSize(600,250)
                self.submit.SetSize(560, 40)

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
