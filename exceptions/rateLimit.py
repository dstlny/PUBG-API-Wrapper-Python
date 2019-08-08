from os import system
import sys
from time import sleep

def rateLimitReached():
    print('We have reached the rate limit. Retrying in 60 seconds.')
    for _TIME_REMAINING in range(60,0,-1):
        sys.stdout.write("\r")
        sys.stdout.write("{:2d} seconds remaining.".format(_TIME_REMAINING))
        sys.stdout.flush()
        sleep(1)
    system("cls")