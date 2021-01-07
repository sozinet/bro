"""
Program do sterowania systemem automatyzacji hodowli roslin
Andrew Sozinov
Politechnika Bialostocka, 2021
"""
import time
import sys
import RPi.GPIO as GPIO
import os
import Adafruit_DHT
import urllib2
from TSL2581 import TSL2581

myAPI = "8XMCYIBW1SZCV10K"
baseURL = 'http://api.thingspeak.com/update?api_key=%s' % myAPI

#Definicja pinow
DHTpin = 4
LEDpin = 17
FANpin = 27

#Ustawienia pinow
GPIO.setmode(GPIO.BCM)
GPIO.setup(LEDpin, GPIO.OUT)
GPIO.output(LEDpin, GPIO.LOW)
GPIO.setup(FANpin, GPIO.OUT)
GPIO.output(FANpin, GPIO.LOW)
GPIO.setup(DHTpin, GPIO.IN)

#funkcja pobierania danych z czujnika temperatury i wilgotnosci
def getSensorData():
    try:
        RHW, TW = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHTpin)
        return (str(RHW), str(TW))
    except:
        return ('error', 'error')

#funkcja pobierania danych z czujnika natenia owatlenia    
def getTSLSensorData(Light):
    try:
        return str(Light.calculate_Lux(2, 148))
    except:
        return 'error'
#start programu glownego
print ('starting...')
try:
    
    Light=TSL2581(0X39, debug=False)

    Light.Init_TSL2581()
    while True:
#Uruchomienie funkcji do pobrania danych z czujnikow
      lux  =  getTSLSensorData(Light)
      LT = int(lux)*4
      lux4 = str(LT)
      RHW, TW = getSensorData()

#przesylanie danych do servisu internetowego oraz ich wyswietlenie w terminalu
      f = urllib2.urlopen(baseURL + 
                                "&field1=%s&field2=%s" % (TW, RHW)+
                                "&field3=%s" % (lux4))
      print(TW + " " + RHW + " " +  lux4) 
      
#zapalenie swiatla przy zbyt malym oswiatleniu
      if LT >= 900:
        GPIO.output(LEDpin, GPIO.HIGH)
      else:
        GPIO.output(LEDpin, GPIO.LOW)

#wlaczenie wentylatora przy zbyt uze temperaturze lub wilotnosci
      if TW >= 24 or RHW >=40:
        GPIO.output(FANpin, GPIO.HIGH)
      else:
        GPIO.output(FANpin, GPIO.LOW)
        
#timer odszytu danych z czujnikow (sekundy)
      time.sleep(5)

#except Exception as inst:
except KeyboardInterrupt:
     
    print ("\nProgram end")
    exit()
finally:
    GPIO.cleanup() 
