from time import sleep
from peripherals import Peripherals

def main():
    
    per = Peripherals()
    per.initialize_apds9960()
    per.initialize_bme680()
    
    while True:
        try:
            sensor_data_bme680 = per.read_bme680_sensor()
            sensor_data_apds9960 = per.read_apds9960_sensor()
            
            if sensor_data_bme680 is not None and sensor_data_apds9960 != -1:
                temperature_C, temperature_F, humidity, pressure, gas_KOhms = sensor_data_bme680
                proximity = sensor_data_apds9960
                
                print(f'Temperature: {temperature_C:.2f} C | {temperature_F:.2f} F')
                print(f'Humidity: {humidity:.2f} %')
                print(f'Pressure: {pressure:.2f} hPa')
                print(f'Gas: {gas_KOhms:.2f} KOhms')
                print(f'Proximity: {proximity}')
                print('-------')
            
            sleep(1)
        except KeyboardInterrupt:
            print("Exiting program")
            break
        
if __name__ == "__main__":
    main()