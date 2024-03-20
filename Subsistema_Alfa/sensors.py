from machine import Pin, I2C
from bme680 import BME680_I2C
from apds9960LITE import APDS9960LITE
"""
Author: Fabio Antonio Valente
Version: 1.0
Summary: This file contains the Sensors class which represents a collection of sensors.
"""

# Rest of the code...

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

class Sensors:
    """
    A class that represents a collection of sensors.

    Attributes:
        __i2c (I2C): The I2C bus object used for communication with the sensors.
        __apds9960 (APDS9960LITE): The APDS9960 proximity sensor object.
        __bme (BME680_I2C): The BME680 environmental sensor object.
    """

    def __init__(self, sdaPin: int = 0, sclPin: int = 1, id_i2c: int = 0):
        """
        Initializes a Sensors object.

        Args:
            sdaPin (int): The pin number for the SDA line of the I2C bus. Defaults to 0.
            sclPin (int): The pin number for the SCL line of the I2C bus. Defaults to 1.
            id_i2c (int): The ID of the I2C bus. Defaults to 0.
        """
        self.__i2c = I2C(id_i2c, scl=Pin(sclPin), sda=Pin(sdaPin))

    def initialize_apds9960(self, ledCurrent: int = APDS9960_LED_DRIVE_100MA, proxGain: int = APDS9960_PGAIN_8X) -> None:
        """
        Initializes the APDS9960 proximity sensor.

        Args:
            ledCurrent (int): The LED drive current. Defaults to APDS9960_LED_DRIVE_100MA.
            proxGain (int): The proximity gain. Defaults to APDS9960_PGAIN_8X.
        """
        self.__apds9960 = APDS9960LITE(self.__i2c)
        self.__apds9960.prox.eLEDCurrent = ledCurrent
        self.__apds9960.prox.eProximityGain = proxGain
        self.__apds9960.prox.enableSensor()

    def initialize_bme680(self) -> None:
        """
        Initializes the BME680 environmental sensor.
        """
        self.__bme = BME680_I2C(self.__i2c)
        self.__bme.sea_level_pressure = 1013.25

    def read_apds9960_sensor(self) -> int:
        """
        Reads the proximity level from the APDS9960 sensor.

        Returns:
            int: The proximity level.
        """
        return self.__apds9960.prox.proximityLevel

    def read_bme680_sensor(self):
        """
        Reads the temperature, humidity, pressure, and gas resistance from the BME680 sensor.

        Returns:
            A list containing the temperature in Celsius, temperature in Fahrenheit,
            humidity, pressure, and gas resistance in kilo-ohms. Returns None if reading fails.
        """
        try:
            temperature_C = self.__bme.temperature - 5
            temperature_F = (temperature_C * 9/5) + 32
            humidity = self.__bme.humidity
            pressure = self.__bme.pressure
            gas_KOhms = self.__bme.gas / 1000

            return temperature_C, temperature_F, humidity, pressure, gas_KOhms
        except OSError as e:
            print('Failed to read BME680 sensor.')
            return None
