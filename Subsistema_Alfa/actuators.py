from machine import Pin, SoftSPI, PWM, Timer
from generic_dotstar import SpiDotStar as SPIDotStar

class Color:
    def __init__(self, red:int, green:int, blue:int):
        self._color = (blue, green, red)

class Actuators:
    
    RED = Color(0, 0, 255)
    GREEN = Color(0, 255, 0)
    BLUE = Color(255, 0, 0)
    WHITE = Color(255, 255, 255)
    
    __changeOn_Off_led: bool
    __rgb_alarm_activated: bool
    __numLED_alarm: int
    __alarm_color: Color
    
    __buzzer_alarm_activated: bool
    __changeOn_Off_buzzer: bool
########################################### CONSTRUCTOR #########################################
    
    def __init__(self,sckPin: int= 2, mosiPin: int= 3, id_spi: int= 0, pwmPin: int= 15):
        self.__spi =SoftSPI(sck=Pin(sckPin), mosi=Pin(mosiPin), baudrate=1000000, miso = Pin(4))
        self.__pwmPin = pwmPin
        
###################################### RGB LEDs #################################################
        
    def initialize_RGBLEDs(self, num_RGBLEDs: int= 5) -> None:
        self.__pixelp = SPIDotStar(self.__spi, num_RGBLEDs)
        self.__numRGBLEDs = num_RGBLEDs
        self.__changeOn_Off_led = False
        self.__rgb_alarm_activated = False
        
    def turnOff_all_RGBLEDs(self) -> None:
        for pixel in range(self.__numRGBLEDs):
            self.__pixelp[pixel] = (0, 0, 0)
        self.__pixelp.show()
        
    def turnOn_all_RGBLEDs(self, color: Color) -> None:
        for pixel in range(self.__numRGBLEDs):
            self.__pixelp[pixel] = color._color
        self.__pixelp.show()
        
    def turnOff_RGBLED(self, numLED: int) -> None:
        if numLED in range(self.__numRGBLEDs):
            self.__pixelp[numLED] = (0, 0, 0)
            self.__pixelp.show()
        else:
            print("Index out of bound")
    
    def turnOn_RGBLED(self, numLED: int, color: Color) -> None:
        if numLED in range(self.__numRGBLEDs):
            self.__pixelp[numLED] = color._color
            self.__pixelp.show()
        else:
            print("Index out of bound")
            
    def _turn_RGBLED(self, t) -> None:
        if self.__changeOn_Off_led:
            if self.__numLED_alarm in range(self.__numRGBLEDs):
               self.turnOn_RGBLED(self.__numLED_alarm, self.__alarm_color) 
            else:
                self.turnOn_all_RGBLEDs(self.__alarm_color)
        else:
            if self.__numLED_alarm in range(self.__numRGBLEDs):
               self.turnOff_RGBLED(self.__numLED_alarm) 
            else:
                self.turnOff_all_RGBLEDs()
        self.__changeOn_Off_led = not self.__changeOn_Off_led
            
    def activate_RGBLED_alarm(self, numLED_alarm: int= -1, alarm_color: Color= RED) -> None:
        if not self.__rgb_alarm_activated:
            self.__numLED_alarm = numLED_alarm
            self.__alarm_color = alarm_color
            self.__rgbled_timer = Timer(period=500, mode=Timer.PERIODIC, callback=self._turn_RGBLED)
            self.__rgb_alarm_activated = True
            
    def deactivate_RGBLED_alarm(self) -> None:
        if self.__rgb_alarm_activated:
            self.__rgbled_timer.deinit()
            self.__rgb_alarm_activated = False
            self.turnOff_all_RGBLEDs()
            
###############################################   BUZZER   ################################################################3
        
    def initialize_Buzzer(self) -> None:
        self.__pwm = PWM(self.__pwmPin, freq=2000, duty_u16=0)
        self.__pwmFreq= 1000
        self.__duty_u16= 0
        self.__buzzer_alarm_activated = False
        self.__changeOn_Off_buzzer = False
     
    def setFreq_Buzzer(self, freq: int) -> None:
        if(freq < 50 or freq > 20000):
            print("It is not possible to set the frecuency to "+freq+"Hz")
        else:
          self.__pwmFreq= freq
    
    def setVolume_Buzzer(self, volume: int) -> None:
        if(volume < 0 or volume > 65535):
            print("It is not possible to set the volume to "+volume)
        else:
          self.__duty_u16= volume
          
    def sound_Buzzer(self) -> None:
        self.__pwm.freq(self.__pwmFreq)
        self.__pwm.duty_u16(self.__duty_u16)
        
    def silence_Buzzer(self) -> None:
        self.__pwm.duty_u16(0)
        
    def _tune_Buzzer(self, t) -> None:
        if self.__changeOn_Off_buzzer:
            self.sound_Buzzer()
        else:
            self.silence_Buzzer()
        self.__changeOn_Off_buzzer = not self.__changeOn_Off_buzzer
            
    def activate_Buzzer_alarm(self) -> None:
        if not self.__buzzer_alarm_activated:
            self.__buzzer_timer = Timer(period=500, mode=Timer.PERIODIC, callback=self._tune_Buzzer)
            self.__buzzer_alarm_activated = True
            
    def deactivate_Buzzer_alarm(self) -> None:
        if self.__buzzer_alarm_activated:
            self.__buzzer_timer.deinit()
            self.__buzzer_alarm_activated = False
            self.silence_Buzzer()

################################################### FINALIZER ##############################################

    def deinit(self) -> None:
        self.silence_Buzzer()
        self.turnOff_all_RGBLEDs()
        self.__rgbled_timer.deinit()
        self.__buzzer_timer.deinit()
        self.__pwm.deinit()
        self.__pixelp.deinit()
        