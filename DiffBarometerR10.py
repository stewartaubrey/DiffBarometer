# R10 incorporated ssd1306 0.96" OLED display in lieu of plain leds 8/31/24
"""
Definitions from internet and other references:
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
https://weather.us/observations/pressure-change.html
https://sciencing.com/high-low-reading-barometric-pressure-5814364.html
https://sciencing.com/high-low-reading-barometric-pressure-5814364.html#:~:text=If%20barometric%20pressure%20rises%20or%20falls%20more%20than,three%20hours%20is%20considered%20to%20be%20holding%20steady.
"""

from machine import Pin,I2C
from bmp280 import *
from ucollections import deque
import time
import ssd1306


sdaPINbmp=machine.Pin(0)
sclPINbmp=machine.Pin(1)
sdaPIN1306=machine.Pin(2)
sclPIN1306=machine.Pin(3)
bmpbus = I2C(0,sda=sdaPINbmp, scl=sclPINbmp, freq=400000)
ssdbus = I2C(1,sda=sdaPIN1306, scl=sclPIN1306, freq=400000)
time.sleep(0.1)
bmp = BMP280(bmpbus)
bmp.use_case(BMP280_CASE_INDOOR)
display = ssd1306.SSD1306_I2C(128, 64, ssdbus)


""" Run these 2 lines to extract cal data from specific sensor
and then update bmp280.py with that data; did it but made no difference

calib_data = bmp.print_calibration()
print(calib_data)    """

#Initial Variables

count=0
"""pin2=Pin(2,Pin.OUT)
pin3=Pin(3,Pin.OUT)
pin4=Pin(4,Pin.OUT)
pin5=Pin(5,Pin.OUT)
pin6=Pin(6,Pin.OUT)
pin7=Pin(7,Pin.OUT)
pin8=Pin(8,Pin.OUT)"""
display.clear()
display.wrap("RUNNING", 10, 20, 2, 1)

dwell =  15   #time between pressure readings
sample = 60   #number of samples in avg calc

avg_p_delta=0.0
pressure_array=deque([],sample)
avg_p_array=deque([],2)

pressure_avg=0
old_p_pressure=0

#Rate of Change Rules; all rates in inHg/sec*(dwell*sample) <-because dwell*sample is how long between calc diffs

rapid=(0.18/(3*60*60))*(dwell*sample) #Ref 1
upper_fast_sys= (0.18/(3*60*60))*(dwell*sample) #dwell * sample is the total time between readings in seconds
lower_fast_sys = (0.12/(3*60*60))*(dwell*sample) #here's where I split the gap to cover missing ranges
upper_slow_sys= (0.12/(3*60*60))*(dwell*sample)
lower_slow_sys = (0.05/(3*60*60))*(dwell*sample)  #here's where I split the gap to cover missing ranges
upper_slow_change= (0.05/(3*60*60))*(dwell*sample)
lower_slow_change = (0.003/(3*60*60))*(dwell*sample)
steady = (0.003/(3*60*60))*(dwell*sample)

"""
#Use snippet below to print calculated rates per sample
print(f'{rapid:1.8f}')  #f'{abs(avg_p_delta):1.5f}'
print(f'{upper_fast_sys:1.8f}')
print(f'{lower_fast_sys:1.8f}')
print(f'{upper_slow_sys:1.8f}')
print(f'{lower_slow_sys:1.8f}')
print(f'{upper_slow_change:1.8f}')
print(f'{lower_slow_change:1.8f}')
print(f'{steady:1.8f}')   """

#Logging Instructions
 



"""
#ALS calibration approach (sketchy).  Assumes a static offset type error
# Just run for calibration when needed and capture the calibration factor
# code snipped follows:

ref_pressure=30.02 #get from local airport METAR 
pressure=bmp.pressure
p_bar=pressure/100000
p_mmHg=pressure/133.3224
p_inHg=p_mmHg/25.4
correction_factor = ref_pressure-p_inHg
print("correction_factor=",correction_factor)    """

correction_factor= 0.8218842  #hard coded from running the above and then commenting it back
#Main Loop
display.clear()
display.wrap("RUNNING", 30, 30, 2, 1)
display.show()
print("Running...") #note that program is active
print (time.localtime())
print (time.gmtime())

"""
Pin2=pin2.value(1)
Pin3=pin3.value(1)
Pin4=pin4.value(1)
Pin5=pin5.value(1)
Pin6=pin6.value(1)
Pin7=pin7.value(1)
Pin8=pin8.value(1)
time.sleep(2)

Pin2=pin2.value(0)
Pin3=pin3.value(0)
Pin4=pin4.value(0)
Pin5=pin5.value(0)
Pin6=pin6.value(0)
Pin7=pin7.value(0)
Pin8=pin8.value(0)"""


while count < sample:
    #print(count,sample) debug code
    pressure=bmp.pressure
    p_bar=pressure/100000
    p_mmHg=pressure/133.3224
    p_inHg=(p_mmHg/25.4)+correction_factor
    pressure_array.append(p_inHg)
    temperature=bmp.temperature
    tempF=temperature*(9/5)+32
    time.sleep(dwell) #delay between readings



    count += 1
 
    avg_p_pressure = (sum(pressure_array)/sample)
    disp_press=f'{(sum(pressure_array)/sample):2.2f}'
    #print(f"Pressure Array: {list(pressure_array)}") #debug print
#compute "sample" readings avg of p_delta here eventually
    if count>=(sample):
        #print("Avg Pressure of Sample:",avg_p_pressure) #debug print
        avg_p_array.append((avg_p_pressure))
        #print(f"Avg Pressure Array: {list(avg_p_array)}") #debug print
        avg_p_delta=(avg_p_pressure)-(old_p_pressure)
        #print("Pressure Change between samples:",avg_p_delta,"inHg") #debug print

        #rate of change logic    
        if (avg_p_delta) >=  rapid:
            change=" Extreme Change!"
        if ( ((avg_p_delta) >= lower_fast_sys) and ((avg_p_delta) < upper_fast_sys)):
            change="  Rapid System"
        if ( ((avg_p_delta) >= lower_slow_sys) and ((avg_p_delta) < upper_slow_sys)):
            change="  Slow System"
        if ( ((avg_p_delta) >= lower_slow_change) and ((avg_p_delta) < upper_slow_change)):
            change="  Very Slow Chg"
        if (abs(avg_p_delta) <= steady):
            change="     Steady"
        if (avg_p_delta < 0 ):
            direction="Falling"
        elif (avg_p_delta >= 0):
            direction="Rising"

        #display.fill(1)
        #display.clear()
        #display.show()
        #time.sleep(.5)
        # Wait 2 seconds
        #time.sleep(2)

        # Fill White Background
        #display.fill(1)
        row=5

        # Display a text in white background with default font size 4
        display.clear()
        display.rect(1, 1, 127, 63, 2)
        #display.wrap("Pressure:",1,row,1.5,1)
        display.wrap(str(disp_press), 25, row, 3, 1)
        display.line(105,5,102,10,1)
        display.line(108,5,105,10,1)
        display.wrap("TREND:", 10, row+20, 1.5, 1)
        display.wrap(str(direction), 65, row+20, 1.5, 1)
        display.line(1,36,128,36,1)
        display.wrap("Rate of Change", 14, row+36, 1.5, 1)
        display.wrap(str(change), 5, row+46, 1.5, 1)
        display.show()
        # Update Display
#         display.show()
        #print(f'{abs(avg_p_delta):1.5f}') #delta pressure only for fine plotting
        print("Current Pressure:", f'{(sum(pressure_array)/sample):2.5f}', "inHg,","Change =",f'{abs(avg_p_delta):1.5f}',",",change,direction)
        #file.write("hello",a)

        print (time.localtime())
        file_path = "Pressure History.txt"
        pressure_avg=f'{(sum(pressure_array)/sample):2.5f}'
        with open(file_path, 'a') as file:
            file.write(f"{pressure_avg}  ")

            file.write(f"{time.localtime()}\n")
        #with open(file_path, 'a') as file:

        #print(f'{tempF:3.1f}')
        #print("Temp:{}, Pressure: {} inHg, {} Press Chg: {} {}".format(f'{tempF:3.1f}',f'{avg_p_pressure:2.5f}', f'{avg_p_delta:2.6f}',change,direction))
        count=0
        old_p_pressure=(sum(pressure_array)/sample)
        
"""#LED Logic
        #print(change,direction)
        if change == "Steady":
            Pin2=pin2.value(0)
            Pin3=pin3.value(0)
            Pin4=pin4.value(0)
            Pin5=pin5.value(1)
            Pin6=pin6.value(0)
            Pin7=pin7.value(0)
            Pin8=pin8.value(0)
            
        if (  (change == ("Slow Change")) and (direction == ("Falling")) ):                 
            Pin2=pin2.value(0)
            Pin3=pin3.value(0)
            Pin4=pin4.value(0)
            Pin5=pin5.value(1)
            Pin6=pin6.value(1)
            Pin7=pin7.value(0)
            Pin8=pin8.value(0)
            
        if (change == ("Slow Change") and direction == ("Rising")):
            Pin2=pin2.value(0)
            Pin3=pin3.value(0)
            Pin4=pin4.value(1)
            Pin5=pin5.value(1)
            Pin6=pin6.value(0)
            Pin7=pin7.value(0)
            Pin8=pin8.value(0)
            
        if (change == ("Slow Moving System") and direction == ("Falling")):
            Pin2=pin2.value(0)
            Pin3=pin3.value(0)
            Pin4=pin4.value(0)
            Pin5=pin5.value(1)
            Pin6=pin6.value(1)
            Pin7=pin7.value(1)
            Pin8=pin8.value(0)                       
            
        if (change == ("Slow Moving System") and direction == ("Rising")):            
            Pin2=pin2.value(1)
            Pin3=pin3.value(1)
            Pin4=pin4.value(1)
            Pin5=pin5.value(1)
            Pin6=pin6.value(0)
            Pin7=pin7.value(0)
            Pin8=pin8.value(0)
            
        if (change == ("Fast Moving System") and direction == ("Falling")):            
            Pin2=pin2.value(0)
            Pin3=pin3.value(0)
            Pin4=pin4.value(0)
            Pin5=pin5.value(1)
            Pin6=pin6.value(1)
            Pin7=pin7.value(1)
            Pin8=pin8.value(1)
            
        if (change == ("Fast Moving System") and direction == ("Rising")):         
            Pin2=pin2.value(1)
            Pin3=pin3.value(1)
            Pin4=pin4.value(1)
            Pin5=pin5.value(1)
            Pin6=pin6.value(0)
            Pin7=pin7.value(0)
            Pin8=pin8.value(0)       

        if (change == ("Extreme Change!") and direction == ("Falling")):
            Pin2=pin2.value(0)
            Pin3=pin3.value(0)
            Pin4=pin4.value(0)
            Pin5=pin5.value(0)
            Pin6=pin6.value(0)
            Pin7=pin7.value(0)
            Pin8=pin8.value(1) # <-make flashing somehow

        if (change == ("Extreme Change!") and direction == ("Rising")):
            Pin2=pin2.value(1) # <-make flashing somehow
            Pin3=pin3.value(0)
            Pin4=pin4.value(0)
            Pin5=pin5.value(0)
            Pin6=pin6.value(0)
            Pin7=pin7.value(0)
            Pin8=pin8.value(0) # <-but flashing"""


