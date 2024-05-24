
"""
Author: Fabio Antonio Valente
Description: This file contains the implementation of the Actuators class, which represents a set of actuators including RGB LEDs and a buzzer.
"""

from machine import Pin, SoftSPI, PWM, Timer
from generic_dotstar import SpiDotStar as SPIDotStar

class Color:
    def __init__(self, red:int, green:int, blue:int):
        """
        Initialize a Color object with RGB values.

        Args:
            red (int): The red component of the color (0-255).
            green (int): The green component of the color (0-255).
            blue (int): The blue component of the color (0-255).
        """
        self._color = (blue, green, red)

class Actuators:
    """
    Class representing a set of actuators including RGB LEDs and a buzzer.
    """

    RED = Color(0, 0, 255)
    GREEN = Color(0, 255, 0)
    BLUE = Color(255, 0, 0)
    WHITE = Color(255, 255, 255)

    __change_on_off: bool
    __alarm_activated: bool
    __num_led_alarm: int
    __alarm_color: Color
    __rgb_led_on: bool

    def __init__(self, sck_pin: int=2, mosi_pin: int=3, id_spi: int=0, pwm_pin: int=15):
        """
        Initialize the Actuators object.

        Args:
            sck_pin (int, optional): The pin number for the SPI clock. Defaults to 2.
            mosi_pin (int, optional): The pin number for the SPI MOSI. Defaults to 3.
            id_spi (int, optional): The SPI ID. Defaults to 0.
            pwm_pin (int, optional): The pin number for the PWM output. Defaults to 15.
        """
        self.__spi = SoftSPI(sck=Pin(sck_pin), mosi=Pin(mosi_pin), baudrate=1000000, miso=Pin(4))
        self.__pwm_pin = pwm_pin
        self.__alarm_timer = None
        self.__alarm_activated = False
        self.__change_on_off = True

    def initialize_rgbleds(self, num_rgb_leds: int= 5) -> None:
        """
        Initialize the RGB LEDs.

        Args:
            num_rgb_leds (int, optional): The number of RGB LEDs. Defaults to 5.
        """
        self.__num_rgb_leds = num_rgb_leds
        self.__pixelp = SPIDotStar(self.__spi, num_rgb_leds)
        self.__rgb_led_on = False

    def turn_off_all_rgbleds(self) -> None:
        """
        Turn off all RGB LEDs.
        """
        for pixel in range(self.__num_rgb_leds):
            self.__pixelp[pixel] = (0, 0, 0)
        self.__pixelp.show()
        self.__rgb_led_on = False

    def turn_on_all_rgbleds(self, color: Color) -> None:
        """
        Turn on all RGB LEDs with the specified color.

        Args:
            color (Color): The color to set the LEDs to.
        """
        for pixel in range(self.__num_rgb_leds):
            self.__pixelp[pixel] = color._color
        self.__pixelp.show()
        self.__rgb_led_on = True

    def turn_off_rgbled(self, num_led: int) -> None:
        """
        Turn off a specific RGB LED.

        Args:
            num_led (int): The index of the LED to turn off.
        """
        if num_led in range(self.__num_rgb_leds):
            self.__pixelp[num_led] = (0, 0, 0)
            self.__pixelp.show()
            self.__rgb_led_on = False
        else:
            print("Index out of bound")

    def turn_on_rgbled(self, num_led: int, color: Color) -> None:
        """
        Turn on a specific RGB LED with the specified color.

        Args:
            num_led (int): The index of the LED to turn on.
            color (Color): The color to set the LED to.
        """
        if num_led in range(self.__num_rgb_leds):
            self.__pixelp[num_led] = color._color
            self.__pixelp.show()
            self.__rgb_led_on = True
        else:
            print("Index out of bound")
            
    def is_rgb_led_on(self) -> bool:
        return self.__rgb_led_on

    def _turn_alarm(self, t) -> None:
        """
        Internal method for toggling the RGB LEDs and Buzzeron/off based on the alarm state.
        """
        if self.__change_on_off:
            self.sound_buzzer()
            if self.__num_led_alarm in range(self.__num_rgb_leds):
                self.turn_on_rgbled(self.__num_led_alarm, self.__alarm_color)
            else:
                self.turn_on_all_rgbleds(self.__alarm_color)
        else:
            self.silence_buzzer()
            if self.__num_led_alarm in range(self.__num_rgb_leds):
                self.turn_off_rgbled(self.__num_led_alarm)
            else:
                self.turn_off_all_rgbleds()
        self.__change_on_off = not self.__change_on_off

    def activate_alarm(self, num_led_alarm: int= -1, alarm_color: Color= RED) -> None:
        """
        Activate the alarm.

        Args:
            num_led_alarm (int, optional): The index of the LED to use for the alarm. Defaults to -1.
            alarm_color (Color, optional): The color to set the LED(s) to during the alarm. Defaults to RED.
        """
        if not self.__alarm_activated:
            self.__num_led_alarm = num_led_alarm
            self.__alarm_color = alarm_color
            self.turn_off_all_rgbleds()
            self.silence_buzzer()
            self.__alarm_timer = Timer(period=500, mode=Timer.PERIODIC, callback=self._turn_alarm)
            self.__alarm_activated = True
            self.__change_on_off = True

    def deactivate_alarm(self) -> None:
        """
        Deactivate the alarm.
        """
        if self.__alarm_activated:
            self.__alarm_timer.deinit()
            self.__alarm_activated = False
            self.turn_off_all_rgbleds()
            self.silence_buzzer()
            self.__change_on_off = True

    def initialize_buzzer(self) -> None:
        """
        Initialize the buzzer.
        """
        self.__pwm = PWM(Pin(self.__pwm_pin))
        self.__pwm_freq = 1000
        self.__duty_u16 = 0

    def set_freq_buzzer(self, freq: int) -> None:
        """
        Set the frequency of the buzzer.

        Args:
            freq (int): The frequency to set (in Hz).
        """
        if freq < 50 or freq > 20000:
            print("It is not possible to set the frequency to " + str(freq) + "Hz")
        else:
            self.__pwm_freq = freq

    def set_volume_buzzer(self, volume: int) -> None:
        """
        Set the volume of the buzzer.

        Args:
            volume (int): The volume to set (0-65535).
        """
        if volume < 0 or volume > 65535:
            print("It is not possible to set the volume to " + str(volume))
        else:
            self.__duty_u16 = volume

    def sound_buzzer(self) -> None:
        """
        Turn on the buzzer with the set frequency and volume.
        """
        self.__pwm.freq(self.__pwm_freq)
        self.__pwm.duty_u16(self.__duty_u16)

    def silence_buzzer(self) -> None:
        """
        Turn off the buzzer.
        """
        self.__pwm.duty_u16(0)

    def deinit(self) -> None:
        """
        Deinitialize the Actuators object.
        """
        self.silence_buzzer()
        self.turn_off_all_rgbleds()
        if self.__alarm_timer is not None:
            self.__alarm_timer.deinit()
        self.__pwm.deinit()
        self.__pixelp.deinit()
        