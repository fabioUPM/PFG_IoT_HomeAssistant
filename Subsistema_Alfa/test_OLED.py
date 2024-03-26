from time import sleep
import st7789py as st7789
import tft_config
import vga2_bold_16x32 as font
import vga1_bold_16x16 as fontA

tft = tft_config.config(tft_config.TALL)

def temp(text):
    length = 1 if isinstance(text, int) else len(text)
    tft.text(
        font,
        text,
        tft.width // 2 - length // 2 * font.WIDTH,
        tft.height // 3 - font.HEIGHT //3,
        st7789.WHITE,
        st7789.BLACK)
    
def hum(text):
     length = 1 if isinstance(text, int) else len(text)
     tft.text(
         font,
         text,
         tft.width // 2 - length // 2 * font.WIDTH,
         tft.height // 2 - font.HEIGHT //2,
         st7789.WHITE,
         st7789.BLACK)
     
def gas(text):
     length = 1 if isinstance(text, int) else len(text)
     tft.text(
         font,
         text,
         tft.width // 2 - length // 2 * font.WIDTH,
         140,
         st7789.WHITE,
         st7789.BLACK)
     
def alarm(text):
     length = 1 if isinstance(text, int) else len(text)
     tft.text(
         fontA,
         text,
         tft.width // 2 - length // 2 * fontA.WIDTH,
         tft.height // 5 - fontA.HEIGHT //5,
         st7789.RED,
         st7789.BLACK)
     
def alarmOff(text):
     length = 1 if isinstance(text, int) else len(text)
     tft.text(
         fontA,
         text,
         tft.width // 2 - length // 2 * fontA.WIDTH,
         180,
         st7789.GREEN,
         st7789.BLACK)


def main():
    """
    The big show!
    """
    tft.fill(st7789.BLACK)
    

    while True:
        try:
            temp("Temp:55.55 C")
            sleep(4)
            hum("Hum:67.89 %")
            sleep(4)
            gas("Gas:62.89 kOhm")
            sleep(4)
            alarm("ALARM ON ")
            sleep(4)
            alarmOff("ALARM OFF")
            sleep(4)
            
            
        except KeyboardInterrupt:
            tft.fill(0x0)
            break
            

main()



