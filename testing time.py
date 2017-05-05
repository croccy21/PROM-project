#-------------------------------------------------------------------------------
# Name:        Time testing
# Purpose:
#
# Author:      callum
#
# Created:     05/05/2017
# Copyright:   (c) callum 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import time
import timeit



def sleepytime(): #assumes length is an int in ms
    wake = time.time()+100/1000
    while wake > time.time():
        time.sleep(100/10000)

def oldsleep():
    time.sleep(100/1000)

print(timeit.Timer(sleepytime).timeit(1))
print(timeit.Timer(oldsleep).timeit(1))