from machine import Pin, I2C
from bme680 import BME680_I2C
from apds9960LITE import APDS9960LITE

# Proximity Gain (PGAIN) values
APDS9960_PGAIN_1X = const(0)
APDS9960_PGAIN_2X = const(1)
APDS9960_PGAIN_4X = const(2)
APDS9960_PGAIN_8X = const(3)

# LED Drive values
APDS9960_LED_DRIVE_100MA  = const(0)
APDS9960_LED_DRIVE_50MA   = const(1)
APDS9960_LED_DRIVE_25MA   = const(2)
APDS9960_LED_DRIVE_12_5MA = const(3)

class Peripherals:
    
    def __init__(self,sdaPin: int =0, sclPin: int =1, id_i2c: int= 0):
        self.__i2c =I2C(id_i2c,scl=Pin(sclPin), sda=Pin(sdaPin))
        

    def initialize_apds9960(self, ledCurrent: int= APDS9960_LED_DRIVE_100MA, proxGain: int= APDS9960_PGAIN_8X) -> None:
        self.__apds9960=APDS9960LITE(self.__i2c)
        self.__apds9960.prox.eLEDCurrent   =ledCurrent    
        self.__apds9960.prox.eProximityGain=proxGain   
        self.__apds9960.prox.enableSensor()

    def initialize_bme680(self) -> None:
        self.__bme = BME680_I2C(self.__i2c)

    def read_apds9960_sensor(self) -> int:
        return self.__apds9960.prox.proximityLevel

    def read_bme680_sensor(self) -> list or None:
        try:
            temperature_C = self.__bme.temperature
            temperature_F = (temperature_C * 9/5) + 32
            humidity = self.__bme.humidity
            pressure = self.__bme.pressure
            gas_KOhms = self.__bme.gas / 1000

            return temperature_C, temperature_F, humidity, pressure, gas_KOhms
        except OSError as e:
            print('Failed to read BME680 sensor.')
            return None
