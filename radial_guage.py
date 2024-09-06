import time
import math
from machine import Pin, SPI
import gc9a01

# Initialize SPI
spi = SPI(1, baudrate=40000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19))

# Initialize display
display = gc9a01.GC9A01(spi, cs=Pin(22), dc=Pin(21), rst=Pin(20), width=240, height=240)

# Function to draw the needle
def draw_needle(angle, length, color):
    x0 = 120
    y0 = 120
    x1 = x0 + int(length * math.cos(math.radians(angle)))
    y1 = y0 + int(length * math.sin(math.radians(angle)))
    display.line(x0, y0, x1, y1, color)

# Main loop
while True:
    for angle in range(0, 360, 5):
        display.fill(0)  # Clear the display
        draw_needle(angle, 100, gc9a01.color565(255, 0, 0))  # Draw the needle
        display.show()
        time.sleep(0.1)