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

from umachine import Pin,I2C
from bmp280 import *
from ucollections import deque
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

dwell =  2   #time between pressure readings
sample = 5

avg_p_delta=0.0
pressure_array=deque([],sample)
avg_p_array=deque([],2)
#avg_p_array=[1,1]
pressure_avg=0
old_p_pressure=0

#Rate of Change Rules; all rates in inHg/sec

rapid=0.18/(3*60*dwell) #Ref 1
upper_fast_sys= 0.18/(3*60*(dwell/60))
lower_fast_sys = 0.12/(3*60*(dwell/60))
upper_slow_sys= 0.12/(3*60*(dwell/60))
lower_slow_sys = 0.05/(3*60*(dwell/60))
upper_slow_change= 0.05/(3*60*(dwell/60))
lower_slow_change = 0.003/(3*60*(dwell/60))
steady = 0.003/(3*60*(dwell/60))
#print(f'{rapid:2.10f}')
#Logging Instructions


#LED Logic


#Main Loop
while count <= sample:
    pressure=bmp.pressure
    p_bar=pressure/100000
    p_mmHg=pressure/133.3224
    p_inHg=p_mmHg/25.4
    pressure_array.append(p_inHg)
    temperature=bmp.temperature
    tempF=temperature*(9/5)+32
    time.sleep(dwell) #delay between readings

    count += 1
 
    avg_p_pressure = (sum(pressure_array)/sample)
    
    print(f"Pressure Array: {list(pressure_array)}")
#compute "sample" readings avg of p_delta here eventually
    if count>(sample):
        print("Avg of above array:",avg_p_pressure)
        #print(count,sample,alength)

        #avg_p_array.append(88.0)
        avg_p_array.append((avg_p_pressure))
        print(f"Avg Pressure Array: {list(avg_p_array)}")
        avg_p_delta=(avg_p_pressure)-(old_p_pressure)
        print("Pressure Change between samples:",avg_p_delta,"inHg")

        print(avg_p_delta)
        #rate of change logic    
        if (avg_p_delta) >=  rapid:
            change="Extreme Change!"
        if ( ((avg_p_delta) >= lower_fast_sys) and ((avg_p_delta) < upper_fast_sys)):
            change="Rapid Moving System"
        if ( ((avg_p_delta) >= lower_slow_sys) and ((avg_p_delta) < upper_slow_sys)):
            change="Slow Moving System"
        if ( ((avg_p_delta) >= lower_slow_change) and ((avg_p_delta) < upper_slow_change)):
            change="Slow Change"
        if (abs(avg_p_delta) <= steady):
            change="Steady"
        if (avg_p_delta < 0):
            direction="Falling"
        elif (avg_p_delta >= 0):
            direction="Rising"

        #print((sum(pressure_array)/sample),"Change=",f'{avg_p_delta:1.5f}',change,direction)
        #print(f'{tempF:3.1f}')
        #print("Temp:{}, Pressure: {} inHg, {} Press Chg: {} {}".format(f'{tempF:3.1f}',f'{avg_p_pressure:2.5f}', f'{avg_p_delta:2.6f}',change,direction))
        count=0
        old_p_pressure=(sum(pressure_array)/sample)
        
        
    