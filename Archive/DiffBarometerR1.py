# Source: Electrocredible.com, Language: MicroPython
"""
Definitions for internet:
Rapid change: More than 0.18 in-Hg in less than three hours - Ref 1
Fast-moving system: 0.05 to 0.06 inches per hour = 0.15 to 0.18 inches per 3 hours
Slow-moving system: 0.02 to 0.03 inches per hour = 0.06 to 0.09 inches per 3 hours
Slow change: 0.003 to 0.04 in-Hg in less than three hours
Holding steady: Less than 0.003 in-Hg in less than three hours

ALS mods to account for gaps in internet definition of ranges
? there are gaps in the ranges:
? there is no category between 0.09 and 0.15 in less than three hours
? there is no category between 0.04 and 0.06 in less than three hours? als
so:
I'm going to split the gap on Slow change to 0.05 per 3 hours
I'm going to split the gap on slow and fast moving systems at 0.12 inches per 3 hours
"""

from machine import Pin,I2C
from bmp280 import *
import time

sdaPIN=machine.Pin(0)
sclPIN=machine.Pin(1)
bus = I2C(0,sda=sdaPIN, scl=sclPIN, freq=400000)
time.sleep(0.1)
bmp = BMP280(bus)
bmp.use_case(BMP280_CASE_INDOOR)

#Initial Variables
second_reading_inHg=0.
change="Initializing"
direction=""
count=0
p_delta_summer=0
p_pressure_summer=0
sample=5

#Rate of Change Calculations; all rates in inHg/sec
timebase = 1 #denominator for calculating rate of change, used for sleep time and calc rate of change
rapid=0.18/(3*60*timebase) #Ref 1
upper_fast_sys= 0.18/(3*60*timebase)
lower_fast_sys = 0.12/(3*60*timebase)
upper_slow_sys= 0.12/(3*60*timebase)
lower_slow_sys = 0.05/(3*60*timebase)
upper_slow_change= 0.05/(3*60*timebase)
lower_slow_change = 0.003/(3*60*timebase)
steady = 0.003/(3*60*timebase)
#print(f'{rapid:2.10f}')
#Logging Instructions


#LED Logic


#Main Loop
while count < sample:
    pressure=bmp.pressure
    p_bar=pressure/100000
    p_mmHg=pressure/133.3224
    p_inHg=p_mmHg/25.4
    temperature=bmp.temperature
    tempF=temperature*(9/5)+32
    time.sleep(timebase) #delay between readings
    new_pressure=bmp.pressure
    second_reading_inHg = new_pressure/(133.3244*25.4)
    p_delta=second_reading_inHg-p_inHg
    count += 1
    p_delta_summer = (p_delta_summer+p_delta)
    #print(f'{p_delta_summer:2.5f}',count)
    
    avg_p_delta = p_delta_summer/(count)
    #print("p_delta,sum,count,avg")
    #print(f'{p_delta:2.6f}',f'{p_delta_summer:2.6f}',count,f'{avg_p_delta:2.6f}')#print("p_delta=",f'{p_delta:2.6f}')

    #print(f'{p_delta_summer:2.6f}')
    #print(f'{avg_p_delta:2.6f}')
#compute 10 reading avg of p_delta here eventually
    if count>(sample-1):
        #count = 0
        #rate of change logic    
        if (avg_p_delta) >=  rapid:
            change="Extreme Change!"
        if ( ((avg_p_delta) >= lower_fast_sys) and ((p_delta) < upper_fast_sys)):
            change="Rapid Moving System"
        if ( ((avg_p_delta) >= lower_slow_sys) and ((p_delta) < upper_slow_sys)):
            change="Slow Moving System"
        if ( ((avg_p_delta) >= lower_slow_change) and ((p_delta) < upper_slow_change)):
            change="Slow Change"
        if (avg_p_delta <= steady):
            change="Steady"
        if (avg_p_delta < 0):
            direction="Falling"
        elif (avg_p_delta >= 0):
            direction="Rising"
        p_delta_summer=0
    #print(f'{tempF:3.1f}')
        print("Temp:{}, Pressure: {} inHg, {} Press Chg: {} {}".format(f'{tempF:3.1f}',f'{p_inHg:2.5f}', f'{p_delta:2.6f}',change,direction))
        count=0
    #result = "Falling" if second_reading_inHg <= p_inHg else "Rising"
    #print(change, second_reading_inHg-p_inHg,direction) # Output will depend on the values of a and b
    
    #if ((p_inHg < second_reading_inHg) < 0.1):
        #print(p_inHg, second_reading_inHg)
        #print("Falling",second_reading_inHg)
    
    #time.sleep(3)