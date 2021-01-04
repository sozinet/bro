#!/usr/bin/python
import time
import sys
from TSL2581 import TSL2581
import onemore
import Adafruit_DHT

try:
    Light=TSL2581(0X39, debug=False)

    id=Light.Read_ID() & 0xf0
    print('ID = %#x'%id)
    Light.Init_TSL2581()

    while True:
      lux  =  Light.calculate_Lux(2, 148)
      print('lux = %#d'%lux)
      time.sleep(1)

except:
    # GPIO.cleanup()
    print ("\nProgram end")
    exit()
