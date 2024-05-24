from time import sleep
from sensors import Sensors
from actuators import Actuators
from TFTDisplay import TFTDisplay
import config
from communications import Communication

def main() -> None:
    """
    Main function that reads sensor data and controls actuators based on the data.
    """
    sensor = Sensors()
    actuator = Actuators()
    display = TFTDisplay()
    com = Communication(config)
    actuator.initialize_rgbleds()
    actuator.initialize_buzzer()
    actuator.set_freq_buzzer(800)
    actuator.set_volume_buzzer(300)
    sensor.initialize_apds9960()
    sensor.initialize_bme680()
    display.initialize_display()
    
    if com.initialize_wifi():
        com.connect_mqtt()
        sleep(1)
        com.config_bme680_sensor()
        com.config_actuators()
        while True:
            try:
                sensor_data_bme680 = sensor.read_bme680_sensor()
                sensor_data_apds9960 = sensor.read_apds9960_sensor()
                
                if sensor_data_bme680 is not None and sensor_data_apds9960 != -1:
                    temperature_c, temperature_f, humidity, pressure, gas_k_ohms = sensor_data_bme680
                    proximity = sensor_data_apds9960
                    
                    print_sensor_data(temperature_c, temperature_f, humidity, pressure, gas_k_ohms, proximity)
                    
                    display.show_temperature(temp=temperature_c)
                    display.show_humidity(hum=humidity)
                    display.show_gas(gas=gas_k_ohms)
                    display.show_pressure(pressure=pressure)
                    
                    com.send_bme680_data(temperature_c, humidity, gas_k_ohms, pressure)
                    com.check_new_message()
                    com.check_new_message()
                    com.check_new_message()
                    
                    alarm_status = com.alarm_status()
                    color, rgb_state = com.rgb_state()
                    
                    handle_alarm_status(alarm_status, proximity, actuator, display, com)
                    handle_rgb_state(alarm_status, rgb_state, color, actuator, com)
                            
                #sleep(1)
            except KeyboardInterrupt:
                print("Exiting program")
                actuator.deinit()
                display.deinitialize_display()
                com.disconnect_mqtt()
                break
    else:
        print("Error connecting")
        actuator.deinit()
        display.deinitialize_display()
        com.disconnect_mqtt()

def print_sensor_data(temperature_c, temperature_f, humidity, pressure, gas_k_ohms, proximity):
    """
    Print sensor data.
    """
    print(f'Temperature: {temperature_c:.2f} C | {temperature_f:.2f} F')
    print(f'Humidity: {humidity:.2f} %')
    print(f'Pressure: {pressure:.2f} hPa')
    print(f'Gas: {gas_k_ohms:.2f} KOhms')
    print(f'Proximity: {proximity}')
    print('-------')

def handle_alarm_status(alarm_status, proximity, actuator, display, com) -> None:
    """
    Handle alarm status and proximity.
    """
    if alarm_status == Communication.ARMED:
        display.show_status_alarm(True)
    else:
        display.show_status_alarm(False)
    
    if proximity > 150 and alarm_status == Communication.ARMED:
        actuator.activate_alarm()
        display.activate_tft_alarm()
        com.set_alarm_status(Communication.TRIGGERED)
    elif alarm_status == Communication.TRIGGERED:
        if proximity > 150:
            actuator.activate_alarm()
            display.activate_tft_alarm()
            com.set_alarm_status(Communication.TRIGGERED)
        else:
            actuator.deactivate_alarm()
            display.deactivate_tft_alarm()
            com.set_alarm_status(Communication.ARMED)
    else:
        actuator.deactivate_alarm()
        display.deactivate_tft_alarm()
        if alarm_status == com.DISARMED:
            com.set_alarm_status(Communication.DISARMED)
        else:
            com.set_alarm_status(Communication.ARMED)

def handle_rgb_state(alarm_status, rgb_state, color, actuator, com) -> None:
    """
    Handle RGB state.
    """
    if alarm_status != Communication.TRIGGERED:
        if rgb_state == com.RGB_ON:
            actuator.turn_on_all_rgbleds(color)
            com.set_rgb_state(com.RGB_ON, color)
        else:
            actuator.turn_off_all_rgbleds()
            com.set_rgb_state(com.RGB_OFF, color)
    else:
        actuator.turn_off_all_rgbleds()
        com.set_rgb_state(com.RGB_OFF, color)
        
if __name__ == "__main__":
    main()