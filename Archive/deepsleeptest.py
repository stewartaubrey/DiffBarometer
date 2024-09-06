# Test program to understand how to place RP2040 into low power mode

import machine
import time

# Configure an LED to indicate sleep mode
led = machine.Pin(16, machine.Pin.OUT)

# Turn on the LED
led.value(1)

"""
time.sleep(2)
# Turn off the LED and enter deep sleep mode for 10 seconds
led.value(0)
time.sleep(2)  # Keep the LED on for 1 second

#machine.deepsleep(2)  # Sleep time in milliseconds

# The code will restart from here after waking up from deep sleep
led.value(1)
print("Woke up from deep sleep")

"""