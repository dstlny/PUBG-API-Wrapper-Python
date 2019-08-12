from config import user_settings

if user_settings.GUI:

    import wx


    def connectionTimeOut(Excep):
        wx.MessageBox('{}\n. Failed to establish connection with PUBG API'.format(Excep),"Player not found", style=wx.OK|wx.ICON_ERROR)
        return

else:

    def connectionTimeOut(Excep):
        print('{}\n. Failed to establish connection with PUBG API'.format(Excep))
        return
    
