from time import sleep
from sensors import Sensors
from actuators import Actuators
from TFTDisplay import TFTDisplay

def main():
    """
    Main function that reads sensor data and controls actuators based on the data.
    """
    sensor = Sensors()
    actuator = Actuators()
    display = TFTDisplay()
    actuator.initialize_RGBLEDs()
    actuator.initialize_Buzzer()
    actuator.setFreq_Buzzer(800)
    actuator.setVolume_Buzzer(300)
    sensor.initialize_apds9960()
    sensor.initialize_bme680()
    display.initializeDisplay()
    
    
    while True:
        try:
            sensor_data_bme680 = sensor.read_bme680_sensor()
            sensor_data_apds9960 = sensor.read_apds9960_sensor()
            
            if sensor_data_bme680 is not None and sensor_data_apds9960 != -1:
                temperature_C, temperature_F, humidity, pressure, gas_KOhms = sensor_data_bme680
                proximity = sensor_data_apds9960
                
                print(f'Temperature: {temperature_C:.2f} C | {temperature_F:.2f} F')
                print(f'Humidity: {humidity:.2f} %')
                print(f'Pressure: {pressure:.2f} hPa')
                print(f'Gas: {gas_KOhms:.2f} KOhms')
                print(f'Proximity: {proximity}')
                print('-------')
                
                display.showTemperature(temp=temperature_C)
                display.showHumidity(hum=humidity)
                display.showGas(gas=gas_KOhms)
                display.showPressure(pressure=pressure)
                display.showStatusAlarm(False)
                
                if proximity > 150:
                    actuator.activate_RGBLED_alarm()
                    actuator.activate_Buzzer_alarm()
                    display.activateTFTAlarm()
                else:
                    actuator.deactivate_Buzzer_alarm()
                    actuator.deactivate_RGBLED_alarm()
                    display.deactivateTFTAlarm()
                    #actuator.turnOn_RGBLED(1,Actuators.GREEN)
                    
            sleep(1)
        except KeyboardInterrupt:
            print("Exiting program")
            actuator.deinit()
            display.deinitializeDisplay()
            break
        
if __name__ == "__main__":
    main()