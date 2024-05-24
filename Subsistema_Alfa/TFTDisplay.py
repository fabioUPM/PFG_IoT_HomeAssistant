
from machine import Pin, SPI, Timer
import st7789py as st7789
import vga2_bold_16x32 as font
import vga1_bold_16x16 as fontA

class TFTDisplay:
    """
    This class represents a TFT display module.
    It provides methods to initialize the display, show temperature, humidity, gas, pressure, and alarm status,
    activate and deactivate the alarm, and deinitialize the display.
    """

    def __init__(self, spi_id: int=1, sck_pin: int=10, mosi_pin: int=11,
                 reset_pin: int=16, cs_pin: int=13, dc_pin: int=12,
                 bl_pin: int=14, rotation: int=0, height: int=240, width: int=240):
        """
        Initializes the TFTDisplay object.

        Parameters:
        - spi_id (int): The SPI ID.
        - sck_pin (int): The SCK pin number.
        - mosi_pin (int): The MOSI pin number.
        - reset_pin (int): The RESET pin number.
        - cs_pin (int): The CS pin number.
        - dc_pin (int): The DC pin number.
        - bl_pin (int): The BL pin number.
        - rotation (int): The rotation value.
        - height (int): The display height.
        - width (int): The display width.
        """
        
        self.__spi = SPI(spi_id, baudrate=60000000, sck=Pin(sck_pin), mosi=Pin(mosi_pin), miso=None)
        self.__reset = Pin(reset_pin, Pin.OUT)
        self.__cs = Pin(cs_pin, Pin.OUT)
        self.__dc = Pin(dc_pin, Pin.OUT)
        self.__bl = Pin(bl_pin, Pin.OUT)
        self.__rotation = rotation
        self.__height = height
        self.__width = width
        self.__tft_alarm_activated = False
        self.__tft_timer = None
        self.__change_tft = False
        
    def initialize_display(self)-> None:
        """
        Initializes the TFT display.
        """
        
        self.__display = st7789.ST7789(self.__spi, self.__height, self.__width,
                                     reset=self.__reset, cs=self.__cs, dc=self.__dc,
                                     backlight=self.__bl, rotation=self.__rotation)
        
        self.__display.fill(st7789.BLACK)
        
        
    def show_temperature(self, show: bool=True, temp: float=0.00)-> None:
        """
        Displays the temperature on the TFT display.

        Parameters:
        - show (bool): Whether to show the temperature or not.
        - temp (float): The temperature value.
        """
        if not self.__tft_alarm_activated:
            show_temp = str(f'{temp:.2f} C') if show else str('       ')
            length = len(show_temp)
            self.__display.text(
                        font,
                        show_temp,
                        self.__display.width // 2 - length // 2 * font.WIDTH,
                        self.__display.height // 3 - font.HEIGHT //3,
                        st7789.WHITE,
                        st7789.BLACK)
        
    def show_humidity(self, show: bool=True, hum: float=0.00)-> None:
        """
        Displays the humidity on the TFT display.

        Parameters:
        - show (bool): Whether to show the humidity or not.
        - hum (float): The humidity value.
        """
        if not self.__tft_alarm_activated:
            show_hum = str(f'{hum:.2f} %') if show else str('       ')
            length = len(show_hum)
            self.__display.text(
                        font,
                        show_hum,
                        self.__display.width // 2 - length // 2 * font.WIDTH,
                        self.__display.height // 2 - font.HEIGHT //2,
                        st7789.WHITE,
                        st7789.BLACK)
        
    def show_gas(self, show: bool=True, gas: float=0.00)-> None:
        """
        Displays the gas value on the TFT display.

        Parameters:
        - show (bool): Whether to show the gas value or not.
        - gas (float): The gas value.
        """
        if not self.__tft_alarm_activated:
            show_gas_r = str(f'{gas:.2f} kOhm') if show else str('          ')
            length = len(show_gas_r)
            self.__display.text(
                        font,
                        show_gas_r,
                        self.__display.width // 2 - length // 2 * font.WIDTH,
                        140,
                        st7789.WHITE,
                        st7789.BLACK)
            
    def show_pressure(self, show: bool=True, pressure: float=0.00)-> None:
        """
        Displays the pressure on the TFT display.

        Parameters:
        - show (bool): Whether to show the pressure or not.
        - pressure (float): The pressure value.
        """
        if not self.__tft_alarm_activated:
            show_press = str(f'{pressure:.2f} hPa') if show else str('          ')
            length = len(show_press)
            self.__display.text(
                        font,
                        show_press,
                        self.__display.width // 2 - length // 2 * font.WIDTH,
                        180,
                        st7789.WHITE,
                        st7789.BLACK)
            
    def show_status_alarm(self, engage: bool)-> None:
        """
        Displays the alarm status on the TFT display.

        Parameters:
        - engage (bool): Whether the alarm is engaged or not.
        """
        if not self.__tft_alarm_activated:
            alarm_status = "ALARM ON " if engage else "ALARM OFF"
            length = len(alarm_status)
            self.__display.text(
                        fontA,
                        alarm_status,
                        self.__display.width // 2 - length // 2 * font.WIDTH,
                        self.__display.height // 5 - fontA.HEIGHT //5,
                        st7789.GREEN if engage else st7789.RED,
                        st7789.BLACK)
    
    def activate_tft_alarm(self):
        """
        Activates the TFT alarm.
        """
        if not self.__tft_alarm_activated:
            self.__tft_alarm_activated = True
            self.__display.fill(st7789.BLACK)
            self.__tft_timer = Timer(period=505, mode=Timer.PERIODIC, callback=self._show_alarm)
            
    
    def deactivate_tft_alarm(self):
        """
        Deactivates the TFT alarm.
        """
        if self.__tft_alarm_activated:
            self.__display.fill(st7789.BLACK)
            self.__tft_alarm_activated = False
            self.__tft_timer.deinit()
            
    def _show_alarm(self, t: Timer):
        """
        Shows the alarm on the TFT display.
        This method is called periodically by the timer.

        Parameters:
        - t (Timer): The timer object.
        """
        if self.__change_tft:
            self.__display.fill(st7789.RED)
            warning = str("WARNING!!")
            length = len(warning)
            self.__display.text(
                        font,
                        warning,
                        self.__display.width // 2 - length // 2 * font.WIDTH,
                        self.__display.height // 2 - font.HEIGHT //2,
                        st7789.WHITE,
                        st7789.RED)
        else:
            self.__display.fill(st7789.YELLOW)
            motion = str("MOTION")
            detected = str("DETECTED")
            length_m = len(motion)
            length_d = len(detected)
            self.__display.text(
                        font,
                        motion,
                        self.__display.width // 2 - length_m // 2 * font.WIDTH,
                        self.__display.height // 3 - font.HEIGHT //3,
                        st7789.BLACK,
                        st7789.YELLOW)
            self.__display.text(
                        font,
                        detected,
                        self.__display.width // 2 - length_d // 2 * font.WIDTH,
                        self.__display.height // 2 - font.HEIGHT //2,
                        st7789.BLACK,
                        st7789.YELLOW)
            
        self.__change_tft = not self.__change_tft
            
        
    def deinitialize_display(self):
        """
        Deinitializes the TFT display.
        """
        self.__display.fill(st7789.BLACK)
        self.__spi.deinit()
        if self.__tft_timer is not None:
            self.__tft_timer.deinit()
        
        
        
        
    
        