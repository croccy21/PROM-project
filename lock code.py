#Key lock system
import RPi.GPIO as GPIO
import time
import os


side_attack = True
#This is the setup fo the Maximum Try Lockout
#number of trys first, then delay
#if number of trys  = 0 then won't run
tryanddelay=[]
tryanddelay.append(4)
tryanddelay.append(60)

#Time lockout (was told it had to take the start and end tiems and assume these were from boot up)
#Passed in as an array of hours, and then time past hour in minutes
#Will return ValueError if minutes >59 or hours > 24
timestart = []
timeend = []

timestart.append(0)
timestart.append(0)
timeend.append(0)
timeend.append(0)
if (timestart[1] or timeend[1]) > 59:
    ValueError("Please enter an amount of minutes less than 60")
elif (timestart[0] or timeend[0]) > 24:
    ValueError("Please use 24hour clock times")

opentime =[0,0]
opentime[0] =abs( timeend[0] - timestart[1])
if timeend[1] < timestart[1]:
    opentime[0]-=1
    opentime[1] = 60- (timeend[1] - timestart[1])
else:
    opentime[1] = timeend[1] - timestart[1]

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#The length of sleeps
length = 500
#Settting up the load and output-enable (only needs to be done once because always output
GPIO.setup(14, GPIO.OUT) #load
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
    #Sets and turns off the led, needs a string of which colour and a bool (True = on, False = off)
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
    sleepytime(10)
    GPIO.output(14,1)
    sleepytime(10)
    GPIO.output(14,0)


def buttonpressed():
    onboardgpio = [5,6,12,13,16,19,20,26]
    GPIO.output(onboardgpio[0],0)
    GPIO.output(onboardgpio[1],0)
    GPIO.output(onboardgpio[2],0)
    GPIO.output(onboardgpio[3],0)
    GPIO.output(onboardgpio[4],0)
    GPIO.output(onboardgpio[5],0)
    GPIO.output(onboardgpio[6],0)
    GPIO.output(onboardgpio[7],0)

def timer(timeout,position):
    #needs better timing
    #wait= 1
    onboardgpio = [5,6,12,13,16,19,20,26]
    if (timeout >= 375):
        GPIO.output(onboardgpio[0],1)
    if (timeout >= 375*2):
        GPIO.output(onboardgpio[1],1)
    if (timeout >= 375*3):
        GPIO.output(onboardgpio[2],1)
    if (timeout >= 375*4):
        GPIO.output(onboardgpio[3],1)
    if (timeout >= 375*5):
        GPIO.output(onboardgpio[4],1)
    if (timeout >= 375*6):
        GPIO.output(onboardgpio[5],1)
    if (timeout >= 375*7):
        GPIO.output(onboardgpio[6],1)
    if (timeout >= 375*8):
        GPIO.output(onboardgpio[7],1)
        position = 0
        timeout = 0
        print("Time out")
        GPIO.output(onboardgpio[0],0)
        GPIO.output(onboardgpio[1],0)
        GPIO.output(onboardgpio[2],0)
        GPIO.output(onboardgpio[3],0)
        GPIO.output(onboardgpio[4],0)
        GPIO.output(onboardgpio[5],0)
        GPIO.output(onboardgpio[6],0)
        GPIO.output(onboardgpio[7],0)
    return (position,timeout)


#d type clocks on rising edge
def poll_row(nine,ten,eleven,length):
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
    sleepytime(length)
    GPIO.output(14,1) # loading
    sleepytime(length)
    GPIO.output(14,0) # resetting the load
    sleepytime(length)
    change_to_inputs(length)
    GPIO.output(15,0)# Activating the enable from the tri-state
    sleepytime(length)
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
def change_to_inputs(length):
    GPIO.setup(9,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(10,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(11,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    sleepytime(length)
#red led (4/5)
#Green Led 6/7

def main(length, seconds, side_attack, tryanddelay):
    key_board = [["1","2","3"],["4","5","6"],["7","8","9"],["*","0","#"]]
    password = read_password()
    open_csv()
    wrong = False;
    key_pressed_time =time.time()*10
    gap = 0 # used for software debouncing
    position = 0 #the point in the password the person is at
    #the main loop the repeatedly polls each line
    numtrys = 0
    timeout = 0 # this counts up continously lighting up the onboard leds until all are lit then resets position
    while wrong ==False:
        if (time.time() > seconds) and (seconds != 0):
            onboardgpio = [5,6,12,13,16,19,20,26]
            GPIO.output(onboardgpio[0],1)
            GPIO.output(onboardgpio[1],1)
            GPIO.output(onboardgpio[2],1)
            GPIO.output(onboardgpio[3],1)
            GPIO.output(onboardgpio[4],1)
            GPIO.output(onboardgpio[5],1)
            GPIO.output(onboardgpio[6],1)
            GPIO.output(onboardgpio[7],1)
            ledset("red",True)
            sleepytime(10000)
            return ("Outside of open times")
        nine = 0
        ten = 0
        eleven = 0

        #this loop polls each of key_pressed_timethe rows in order

        for index in range (4):
            pressed = poll_row(nine,ten,eleven,length)
            #this gets which column the person has pressed
            #time.sleep(1)
            if(pressed!= 100):
                sleepytime(length)
            if(pressed == 100):
                sleepytime(length)
                gap += 1
            elif (gap < 16):
                gap = 0 # stops other presses being registered for a bit
            elif (key_board[index][pressed] == password[position]):
                gap = 0 # stops other presses being registered for a bit
                timeout = 0
                incorrect = 0
                buttonpressed()
                position +=1
                #print("{0}: {1} --> {2}".format(index, str(nine) + str(ten) +str(eleven), key_board[index][pressed] if pressed != 100 else "N"))
                #This is the code for the digit display, currently looks wrong because of debugging print
                os.system('clear')
                item = ""
                for  i in range (position-1):
                    item = item + "*"
                print(item + str(key_board[index][pressed]))
                key_pressed_time = time.time()+1
                if (position >3):
                    #This is the code for the digit display
                    os.system('clear')
                    print("****")
                    #runs if the whole password has been entered
                    write_csv("Accepted")
                    ledset("green",True)
                    sleepytime(3000)
                    ledset("green",False)
                    position = 0
                    timeout = 0
                    buttonpressed()
                    os.system('clear')
            else:
                #This is the code for the digit display:
                os.system('clear')
                item = ""
                for  i in range (position-1):
                    item + item+ "*"
                print(item + str(key_board[index][pressed]))
                key_pressed_time = time.time()+1
                #Enables or disables side attacks based on the side_attack constant
                if side_attack == True:
                    gap = 0 # stops other presses being registered for a bit
                    #runs if the wrong number has been entered
                    write_csv("Denied")
                    ledset("red",True)
                    sleepytime(1000)
                    ledset("red",False)
                    position = 0 #sends them back to the start
                    timeout = 0
                    buttonpressed()
                else:
                    gap = 0 # stops other presses being registered for a bit
                    #runs if the wrong number has been entered
                    write_csv("Denied")
                    incorrect+= 1
                    timeout = 0
                    buttonpressed()
                    if incorrect > 3:
                        incorrect = 0
                        position = 0 # only sends them back to the start on their third incorrect press
                        ledset("red",True)
                        sleepytime(1000)
                        ledset("red",False)
                #This clears the digit output
                os.system('clear')
                #This is the maximum try lockout
                if (tryanddelay[0]!= 0):
                    numtrys += 1
                    if (numtrys >= tryanddelay[0]):
                        numsecondsleft = tryanddelay[1]
                        for index in range(tryanddelay[1]):
                            os.system('clear')
                            print("LOCKED " + str(numsecondsleft))
                            numsecondsleft -=1
                            sleepytime(1000)
                        numtrys = 0

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
            #print(str(nine) + str(ten) + str(eleven) + (key_board[index][pressed] if pressed != 100 else "N"))
            timeout += 5
            values =timer(timeout,position)
            position = values[0]
            timeout = values[1]
            if key_pressed_time <= time.time():
                os.system('clear')
                item = ""
                for  i in range (position):
                    item = item +"*"
                print(item)


def sleepytime(length): #assumes length is an int in ms
    wake = time.time()+0.0005+length/1000
    while wake > time.time():
        time.sleep(length/10000)




def open_csv():
    file = "AccessLog.csv"
    f = "data.dat"

    header = False

    if not os.path.exists(file):
    	header = True

    csv = open(file,"a")
    dat = open(f,"a")

    if header:
        csv.write("Time, Action\n")

    csv.write(time.asctime(time.localtime())+", Start Lock \n")

    t = time.ctime().split(' ')[3].split(":")
    t = t[0]+t[1]+t[2]
    dat.write(t+" 0\n")

    dat.close()
    csv.close()


def write_csv(text):
    csv = open("AccessLog.csv","a")
    csv.write(time.asctime(time.localtime())+", "+text+ "\n")
    csv.close()

    if "Ac" in text:
        num = 2
    elif "De" in text:
        num = 1
    else:
        num = 0

    dat = open("data.dat","a")
    t = time.ctime().split(' ')[3].split(":")
    t = t[0]+t[1]+t[2]
    dat.write(t+" "+str(num)+"\n")
    dat.close()

#This runs the main loop. If it is outside of access times then it will turn on the red led and timeout leds and stop
if (opentime[0] and opentime[1])==0:
    try:
        main(length, 0, side_attack,tryanddelay)
    except:
        write_csv("Stop Lock")
    os.system('gnuplot "graph.p"')
    GPIO.cleanup()
else:
    seconds = 60*60*opentime[0]
    seconds += 60*opentime[1]
    if (time.time() < seconds):
        try:
            main(length,seconds, side_attack,tryanddelay)
        except:
            write_csv("Stop Lock")
        os.system('gnuplot "graph.p"')
        GPIO.cleanup()
    else:
        onboardgpio = [5,6,12,13,16,19,20,26]
        GPIO.output(onboardgpio[0],1)
        GPIO.output(onboardgpio[1],1)
        GPIO.output(onboardgpio[2],1)
        GPIO.output(onboardgpio[3],1)
        GPIO.output(onboardgpio[4],1)
        GPIO.output(onboardgpio[5],1)
        GPIO.output(onboardgpio[6],1)
        GPIO.output(onboardgpio[7],1)
        ledset("red",True)
        sleepytime(10000)
        GPIO.cleanup()


