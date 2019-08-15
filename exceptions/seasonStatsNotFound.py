from config import user_settings

if user_settings.GUI:

   import wx

   def seasonStatsNotFound(_season, _name):
      wx.MessageBox(f"It would seem {_season} doesn't have any stats for the player named '{_name}''","No season data for player", style=wx.OK|wx.ICON_ERROR)

else:

   def seasonStatsNotFound(_season, _name):
      print(f"It would seem {_season} doesn't have any stats for the player named '{_name}'")