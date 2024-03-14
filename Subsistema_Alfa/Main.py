from machine import Pin, SoftI2C
from time import sleep
from bme680 import BME680_I2C
 
def initialize_bme680():
    i2c = SoftI2C(scl=Pin(27), sda=Pin(26), timeout=5000000)
    bme = BME680_I2C(i2c=i2c)
    return bme
 
def read_bme680_sensor(bme):
    try:
        temperature_C = bme.temperature
        temperature_F = (temperature_C * 9/5) + 32
        humidity = bme.humidity
        pressure = bme.pressure
        gas_KOhms = bme.gas / 1000
 
        return temperature_C, temperature_F, humidity, pressure, gas_KOhms
    except OSError as e:
        print('Failed to read BME680 sensor.')
        return None
 
def main():
    bme = initialize_bme680()
    
    while True:
        sensor_data = read_bme680_sensor(bme)
        
        if sensor_data is not None:
            temperature_C, temperature_F, humidity, pressure, gas_KOhms = sensor_data
            
            print(f'Temperature: {temperature_C:.2f} C | {temperature_F:.2f} F')
            print(f'Humidity: {humidity:.2f} %')
            print(f'Pressure: {pressure:.2f} hPa')
            print(f'Gas: {gas_KOhms:.2f} KOhms')
            print('-------')
        
        sleep(1)
 
if __name__ == "__main__":
    main()