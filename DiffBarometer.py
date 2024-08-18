# Source: Electrocredible.com, Language: MicroPython
"""
Slow-moving system: 0.02 to 0.03 inches per hour
Fast-moving system: 0.05 to 0.06 inches per hour
Rapid change: More than 0.18 in-Hg in less than three hours
Slow change: 0.003 to 0.04 in-Hg in less than three hours
Holding steady: Less than 0.003 in-Hg in less than three hours"""

from machine import Pin,I2C
from bmp280 import *
import time

sdaPIN=machine.Pin(0)
sclPIN=machine.Pin(1)
bus = I2C(0,sda=sdaPIN, scl=sclPIN, freq=400000)
time.sleep(0.1)
bmp = BMP280(bus)
p_oldHg=0.
bmp.use_case(BMP280_CASE_INDOOR)
#p_oldHg = 31.0
change=""
direction=""
while True:
    pressure=bmp.pressure
    p_bar=pressure/100000
    p_mmHg=pressure/133.3224
    p_inHg=p_mmHg/25.4
    temperature=bmp.temperature
    tempF=temperature*(9/5)+32
    time.sleep(60 )
    new_pressure=bmp.pressure
    p_oldHg = new_pressure/(133.3244*25.4)
    print("Temperature: {} C, {} F".format(temperature, tempF))
    print("Pressure: {} mmHg, {} inHg, {} Press Chg, Temp:{}".format(p_mmHg,p_inHg, (p_oldHg-p_inHg),tempF))
    #p_oldHg = p_inHg
    #print(p_oldHg - p_inHg)
    time.sleep(0)
    if abs(p_oldHg - p_inHg) >=  .001:
        change="Rapid Change"
    if ( ( (p_oldHg - p_inHg) > .000017) and ((p_inHg - p_oldHg) < .001)):
        change="Slow Change"
    if (abs(p_oldHg - p_inHg) <= .000017):
        change="Steady Pressure"
    if (p_oldHg<p_inHg):
        direction="Falling"
    elif (p_oldHg>p_inHg):
        direction="Rising"
    #result = "Falling" if p_oldHg <= p_inHg else "Rising"
    print(change, p_oldHg-p_inHg,direction) # Output will depend on the values of a and b
    
    #if ((p_inHg < p_oldHg) < 0.1):
        #print(p_inHg, p_oldHg)
        #print("Falling",p_oldHg)
    
    #time.sleep(3)