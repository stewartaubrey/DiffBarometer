from machine import Pin, I2C
import ssd1306
import time
x=0
col=5
row=1
# Initialize I2C
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)

# Initialize the display
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
oled.init_display()
#oled.invert()
# Function to display text
def display_text(text):
    oled.fill(0)  # Clear the display
    oled.text(text, col, row)
    oled.text(text, col, row+12)
    #oled.text(text, 0, 27)
    #oled.text(text, 0, 39)
    #oled.text(text, 0, 51)
    #oled.text(text, 0, 63)

    oled.show()
    #oled.init_display()

# Main loop
#while True:
while x<12:
    display_text("P=, 0123456789")
    time.sleep(1)
    print("Running",x)
    x+=1
    row+=6
oled.init_display()