# Source: Electrocredible.com, Language: MicroPython

from machine import Pin,I2C
from bmp280 import *
import time

sdaPIN=machine.Pin(0)
sclPIN=machine.Pin(1)
bus = I2C(0,sda=sdaPIN, scl=sclPIN, freq=400000)
time.sleep(0.1)
bmp = BMP280(bus)

bmp.use_case(BMP280_CASE_INDOOR)

while True:
    pressure=bmp.pressure
    p_bar=pressure/100000
    p_mmHg=pressure/133.3224
    p_inHg=p_mmHg/25.4
    temperature=bmp.temperature
    print("Temperature: {} C".format(temperature))
    print("Pressure: {} Pa, {} bar, {} mmHg, {} inHg".format(pressure,p_bar,p_mmHg,p_inHg))
    time.sleep(5)