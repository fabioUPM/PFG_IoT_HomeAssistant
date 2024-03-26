"""LilyGo T-DISPLAY RP2040 135x240

https://www.lilygo.cc/products/t-display-rp2040

"""
from machine import Pin, SPI
import st7789py as st7789

TFA = 0
BFA = 80
WIDE = 1
TALL = 0
SCROLL = 0      # orientation for scroll.py
FEATHERS = 1    # orientation for feathers.py

def config(rotation=0):
    """
    Configures and returns an instance of the ST7789 display driver.

    Args:
        rotation (int): The rotation of the display (default: 0).

    Returns:
        ST7789: An instance of the ST7789 display driver.
    """

    return st7789.ST7789(
        SPI(1, baudrate=60000000, sck=Pin(10), mosi=Pin(11), miso=None),
        240,
        240,
        reset=Pin(16, Pin.OUT),
        cs=Pin(13, Pin.OUT),
        dc=Pin(12, Pin.OUT),
        backlight=Pin(14, Pin.OUT),
        rotation=rotation)
