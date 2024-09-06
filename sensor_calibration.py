#import smbus2
import bme280
import time

# I2C settings
port = 1
address = 0x76  # Change to 0x77 if needed

# Initialize I2C bus
bus = smbus2.SMBus(port)

# Load calibration parameters
calibration_params = bme280.load_calibration_params(bus, address)

# Function to read pressure from BME280
def read_pressure():
    data = bme280.sample(bus, address, calibration_params)
    return data.pressure

# Main loop to read and split pressure data
while True:
    pressure = read_pressure()
    print(f"Pressure: {pressure:.2f} hPa")
    
    # Split the pressure data (example: integer and decimal parts)
    integer_part = int(pressure)
    decimal_part = pressure - integer_part
    
    print(f"Integer Part: {integer_part}, Decimal Part: {decimal_part:.2f}")
    
    # Wait before the next reading
    time.sleep(1)  # Adjust the interval as needed