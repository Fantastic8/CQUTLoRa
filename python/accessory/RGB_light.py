import RPi.GPIO as GPIO

'''
set up global variables
'''
PIN_RED=17
PIN_BLUE=27
PIN_GREEN=22
frequency=1000

#set up pins
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_RED, GPIO.OUT)
GPIO.setup(PIN_BLUE, GPIO.OUT)
GPIO.setup(PIN_GREEN, GPIO.OUT)

#set up PWM
PWM_RED=GPIO.PWM(PIN_RED,frequency)
PWM_BLUE=GPIO.PWM(PIN_BLUE,frequency)
PWM_GREEN=GPIO.PWM(PIN_GREEN,frequency)
PWM_RED.start(100)
PWM_BLUE.start(100)
PWM_GREEN.start(100)

def RGB(red:int,green:int,blue:int):
    global PWM_RED
    global PWM_BLUE
    global PWM_GREEN
    
    if red<0 or blue<0 or green<0 or red>255 or blue>255 or green>255:
        return False
    
    PWM_RED.ChangeDutyCycle((1-red/255)*100)
    PWM_BLUE.ChangeDutyCycle((1-blue/255)*100)
    PWM_GREEN.ChangeDutyCycle((1-green/255)*100)

while True:
    inputstr=input("Please Input GRB value(Split by blank space):")
    values=inputstr.split( )
    if len(values)==3:
        value_red=int(values[0])
        value_green=int(values[1])
        value_blue=int(values[2])
        
        RGB(value_red,value_green,value_blue)
        print("RED:"+str(value_red)+" GREEN:"+str(value_green)+" BLUE:"+str(value_blue))
