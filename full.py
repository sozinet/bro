import time
import sys
import RPi.GPIO as GPIO
import os
import Adafruit_DHT
import urllib2
from TSL2581 import TSL2581

myAPI = "8XMCYIBW1SZCV10K"
baseURL = 'http://api.thingspeak.com/update?api_key=%s' % myAPI

DHTpin = 4
LEDpin = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(LEDpin, GPIO.OUT)
GPIO.output(LEDpin, GPIO.LOW)
GPIO.setup(DHTpin, GPIO.IN)

def getSensorData():
    try:
        RHW, TW = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHTpin)
   
    # return dict
        return (str(RHW), str(TW))
    except:
        return ('error', 'error')
    
def getTSLSensorData(Light):
    try:
        return str(Light.calculate_Lux(2, 148))
    except:
        return 'error'
print ('starting...')
try:
    
    Light=TSL2581(0X39, debug=False)

    Light.Init_TSL2581()

    while True:
      lux  =  getTSLSensorData(Light)
      RHW, TW = getSensorData()
      f = urllib2.urlopen(baseURL + 
                                "&field1=%s&field2=%s" % (TW, RHW)+
                                "&field3=%s" % (lux))
      print(TW + " " + RHW + " " +  lux)
      
#zapalenie swiatla przy zbyt malym oswiatleniu
      LT=int(lux)
      if LT <= 10:
        GPIO.output(LEDpin, GPIO.HIGH)
      else:
        GPIO.output(LEDpin, GPIO.LOW)
        
#timer odszytu danych z czujnikow (sekundy)
      time.sleep(5)

except Exception as inst:
    
    print ("\nProgram end")
    exit()
finally:
    GPIO.cleanup() 
