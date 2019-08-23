from time import sleep
from config import user_settings

if user_settings.GUI:

    import wx

    def rateLimitReached():
        for timeRemaining in range(60,0,-1):
            wx.MessageBox(f'We have reached the rate limit. Retrying in {timeRemaining} seconds.',"Rate limit reached", style=wx.OK|wx.ICON_ERROR)
            sleep(1)
        return

else:

    from os import system
    import sys

    def rateLimitReached():
        print('We have reached the rate limit. Retrying in 60 seconds.')
        for timeRemaining in range(60,0,-1):
            sys.stdout.write("\r")
            sys.stdout.write("{:2d} seconds remaining.".format(timeRemaining))
            sys.stdout.flush()
            sleep(1)
        system("cls")