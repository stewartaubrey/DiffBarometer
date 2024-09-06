from machine import I2C, Pin
import bmp280

i2c = I2C(scl=Pin(1), sda=Pin(0))
sensor = bmp280.BMP280(i2c)

# Read calibration data
calib_data = sensor.read_calibration_data()
print(calib_data)