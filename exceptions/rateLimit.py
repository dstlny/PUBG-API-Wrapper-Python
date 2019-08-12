from os import system
import sys
from time import sleep
from config import user_settings

if user_settings.GUI:

    import wx

    def rateLimitReached():
        for _TIME_REMAINING in range(60,0,-1):
            wx.MessageBox(f'We have reached the rate limit. Retrying in {_TIME_REMAINING} seconds.',"Rate limit reached", style=wx.OK|wx.ICON_ERROR)
            sleep(1)
        return

else:

    def rateLimitReached():
        print('We have reached the rate limit. Retrying in 60 seconds.')
        for _TIME_REMAINING in range(60,0,-1):
            sys.stdout.write("\r")
            sys.stdout.write("{:2d} seconds remaining.".format(_TIME_REMAINING))
            sys.stdout.flush()
            sleep(1)
        system("cls")



