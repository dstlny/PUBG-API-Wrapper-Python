from config import user_settings

if user_settings.GUI:

    import wx

    def playerNotFound(player):
        wx.MessageBox(f'The PUBG API could not find a player named "{player}"',"Player not found", style=wx.OK|wx.ICON_ERROR)
        return
else:

    def playerNotFound(player):
        print(f'The PUBG API could not find a player named "{player}"')
        return
