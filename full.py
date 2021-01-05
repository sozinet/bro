"""
My First Internet of Things

Temperature/Humidity Light monitor using Raspberry Pi, DHT11, and photosensor 
Data is displayed at thingspeak.com
2015/06/15
SolderingSunday.com

Based on project by Mahesh Venkitachalam at electronut.in

"""
# Import all the libraries we need to run
import sys
import RPi.GPIO as GPIO
import os
from time import sleep
import Adafruit_DHT
import urllib2



DEBUG = 1
# Setup the pins we are connect to
RCpin = 24
DHTpin = 4

#Setup our API and delay
myAPI = "8XMCYIBW1SZCV10K"
myDelay = 15 #how many seconds between posting data

GPIO.setmode(GPIO.BCM)
GPIO.setup(RCpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)



def getSensorData():
    RHW, TW = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHTpin)
   
    # return dict
    return (str(RHW), str(TW))

def RCtime(RCpin):
    LT = 0
    
    if (GPIO.input(RCpin) == True):
        LT += 1
    return (str(LT))
    
# main() function
def main():
    
    print ('starting...')

    baseURL = 'http://api.thingspeak.com/update?api_key=%s' % myAPI
    print (baseURL)
    
    while True:
        try:
            RHW, TW = getSensorData()
            LT = RCtime(RCpin)
            f = urllib2.urlopen(baseURL + 
                                "&field1=%s&field2=%s" % (TW, RHW)+
                                "&field3=%s" % (LT))
            print (TW + " " + RHW + " " + LT)
            

            sleep(int(myDelay))
        except:
            print ('exiting.')
            break

# call main
if __name__ == '__main__':
    main()
