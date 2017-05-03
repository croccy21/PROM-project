#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      callum
#
# Created:     03/05/2017
# Copyright:   (c) callum 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(5,GPIO.OUT)
GPIO.setup(6,GPIO.OUT)
GPIO.setup(12,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(16,GPIO.OUT)
GPIO.setup(19,GPIO.OUT)
GPIO.setup(20,GPIO.OUT)
GPIO.setup(26,GPIO.OUT)


GPIO.output(5,1)
GPIO.output(6,1)
GPIO.output(12,1)
GPIO.output(13,1)
GPIO.output(16,1)
GPIO.output(19,1)
GPIO.output(20,1)
GPIO.output(26,1)
def main():
    leds = [5,6,12,13,16,19,20,26]
    for i in range (len(leds)):
        GPIO.output(leds[i],0)
        time.sleep(1)

main()