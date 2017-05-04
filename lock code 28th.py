#Key lock system
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#Settting up the load and output-enable (only needs to be done once because always output
GPIO.setup(14,GPIO.OUT) #load
GPIO.setup(15,GPIO.OUT) #enable

GPIO.output(14,0)
GPIO.output(15,1) # active low

#This sets up the onboard leds (active low) [5,6,12,13,16,19,20,26]
GPIO.setup(5,GPIO.OUT)
GPIO.setup(6,GPIO.OUT)
GPIO.setup(12,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(16,GPIO.OUT)
GPIO.setup(19,GPIO.OUT)
GPIO.setup(20,GPIO.OUT)
GPIO.setup(26,GPIO.OUT)


GPIO.output(5,0)
GPIO.output(6,0)
GPIO.output(12,0)
GPIO.output(13,0)
GPIO.output(16,0)
GPIO.output(19,0)
GPIO.output(20,0)
GPIO.output(26,0)
#this needs sleeps, and lots of them
def read_password():
    #Code for reading the password
    try:
        code_file = open("password.txt","r")
        code = code_file.readline()
        code_file.close()
    except:
        code = "1234"
    return code

def ledset(colour, on_off):
    #Sets and turns off the led, needs a string of which colour and a bool of on or off
    GPIO.setup(9,GPIO.OUT)
    GPIO.setup(10,GPIO.OUT)
    GPIO.setup(11,GPIO.OUT)
    if (colour == "red"):
        GPIO.output(9,1)
        GPIO.output(10,0)
        if(on_off == True):
            GPIO.output(11,0)
        else:
            GPIO.output(11,1)
    elif (colour == "green"):
        GPIO.output(9,1)
        GPIO.output(10,1)
        if(on_off == True):
            GPIO.output(11,0)
        else:
            GPIO.output(11,1)
    time.sleep(10/1000)
    GPIO.output(14,1)
    time.sleep(10/1000)
    GPIO.output(14,0)

def timer(timeout,position):
    #needs better timing
    #wait= 1
    onboardgpio = [5,6,12,13,16,19,20,26]
    if (timeout >= 0.375):
        GPIO.output(onboardgpio[0],1)
    elif (timeout >= 0.375*2):
        GPIO.output(onboardgpio[1],1)
    elif (timeout >= 0.375*3):
        GPIO.output(onboardgpio[2],1)
    elif (timeout >= 0.375*4):
        GPIO.output(onboardgpio[3],1)
    elif (timeout >= 0.375*5):
        GPIO.output(onboardgpio[4],1)
    elif (timeout >= 0.375*6):
        GPIO.output(onboardgpio[5],1)
    elif (timeout >= 0.375*7):
        GPIO.output(onboardgpio[6],1)
    elif (timeout >= 0.375*8):
        GPIO.output(onboardgpio[7],1)
        position = 0
        print("Time out")
        GPIO.output(onboardgpio[0],0)
        GPIO.output(onboardgpio[1],0)
        GPIO.output(onboardgpio[2],0)
        GPIO.output(onboardgpio[3],0)
        GPIO.output(onboardgpio[4],0)
        GPIO.output(onboardgpio[5],0)
        GPIO.output(onboardgpio[6],0)
        GPIO.output(onboardgpio[7],0)
    return position


#d type clocks on rising edge
def poll_row(nine,ten,eleven):
    #This sets up the GPIO pins to outputs at the start of each cycle
    GPIO.setup(9,GPIO.OUT)
    GPIO.setup(10,GPIO.OUT)
    GPIO.setup(11,GPIO.OUT)
    # This then sets them all to high
    GPIO.output(9,1)
    GPIO.output(10,1)
    GPIO.output(11,1)

    #Sets them to the desired value and then loads the registers
    GPIO.output(9,nine)
    GPIO.output(11,eleven)
    GPIO.output(10,ten)
    time.sleep(10/100)
    GPIO.output(14,1) # loading
    time.sleep(10/100)
    GPIO.output(14,0) # resetting the load
    time.sleep(10/100)
    change_to_inputs()
    GPIO.output(15,0)# Activating the enable from the tri-state
    time.sleep(10/100)
    #recognising which number has been entered
    if (GPIO.input(9) == 0):
        GPIO.output(15,1) # disabling tristate
        return 2
    elif (GPIO.input(10) == 0):
        GPIO.output(15,1) # disabling tristate
        return 1
    elif (GPIO.input(11) == 0):
        GPIO.output(15,1) # disabling tristate
        return 0
    else:
        return 100
def change_to_inputs():
    GPIO.setup(9,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(10,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(11,GPIO.IN,pull_up_down=GPIO.PUD_UP)

#red led (4/5)
#Green Led 6/7

def main():
    key_board = [["1","2","3"],["4","5","6"],["7","8","9"],["*","0","#"]]
    password = read_password()
    wrong = False;
    position = 0 #the point in the password the person is at
    #the main loop the repeatedly polls each line
    timeout = 0 # this counts up continously lighting up the onboard leds until all are lit then resets position
    while wrong ==False:
        nine = 0
        ten = 0
        eleven = 0
        #this loop polls each of the rows in order
        for index in range (4):
            pressed = poll_row(nine,ten,eleven)
            #this gets which column the person has pressed
            time.sleep(1)
            if(pressed!= 100):
                time.sleep(10/100)
            if(pressed == 100):
                time.sleep(10/100)
            elif (key_board[index][pressed] == password[position]):
                timeout = 0
                position +=1
                if (position >3):
                #runs if the whole password has been entered
                    ledset("green",True)
                    time.sleep(3)
                    ledset("green",False)
                    position = 0
            else:
                 #runs if the wrong number has been entered
                 ledset("red",True)
                 time.sleep(1)
                 ledset("red",False)
                 position = 0 #sends them back to the start
                 timeout = 0
            print("{0}: {1} --> {2}".format(index, str(nine) + str(ten) +str(eleven), key_board[index][pressed] if pressed != 100 else "N"))
            if (index == 0):
                eleven = 1
                ten = 0
            elif (index == 1):
                eleven = 0
                ten = 1
            elif (index == 2):
                eleven = 1
                ten = 1
            #time.sleep(1)
        timeout += 30/1000
        position = timer(timeout,position)

try:
    main()
except:
    GPIO.cleanup()
