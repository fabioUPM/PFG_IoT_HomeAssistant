import network
from time import sleep
import json
from umqtt.robust import MQTTClient
from actuators import Actuators, Color

class Communication:
    """
    This class represents the communication module of the IoT Home Assistant subsystem.
    It handles the Wi-Fi connection, MQTT communication, and configuration of sensors and actuators.
    """

    ARMED = 1
    DISARMED = 2
    TRIGGERED = 3
    
    RGB_ON = 1
    RGB_OFF = 2
    
    __ssid: string
    __psw: string
    __mqtt_client_id: string
    __mqtt_server: string
    __mqtt_port: int
    __mqtt_user: string
    __mqtt_psw: string
    __mqtt_keep_alive: int
    __mqtt_client: MQTTClient
    __wlan: WLAN
    
    __temp_config_topic: string
    __temp_config_payload: dict
    __hum_config_topic: string
    __hum_config_payload: dict
    __press_config_topic: string
    __press_config_payload: dict
    __gas_config_topic: string
    __gas_config_payload: dict
    
    __bme680_topic: string
    
    __rgb_config_topic: string
    __rgb_command_topic: string
    __rgb_status_topic: string
    __rgb_color_command_topic: string
    __rgb_color_status_topic:string
    __rgb_config_payload: dict
    
    __color: Color
    
    __alarm_config_topic: string
    __alarm_command_topic: string
    __alarm_status_topic: string
    __alarm_config_payload: dict
    
    __alarm_armed: int
    __rgb_state: int

    
    def __init__(self, config):
        """
        Initializes the Communication object with the provided configuration.

        Args:
            config: The configuration object containing the necessary parameters for Wi-Fi and MQTT connection, as well as sensor and actuator configurations.
        """
        self.__ssid = config.wifi_ssid
        self.__psw = config.wifi_psw
        self.__mqtt_client_id = config.mqtt["client_id"]
        self.__mqtt_server = config.mqtt["server"]
        self.__mqtt_port = config.mqtt["port"]
        self.__mqtt_user = config.mqtt["user"]
        self.__mqtt_psw = config.mqtt["psw"]
        self.__mqtt_keep_alive = config.mqtt["keep_alive"]
        
        self.__temp_config_topic = config.topics["config_temp"]
        self.__temp_config_payload = config.temp_payload
        self.__hum_config_topic = config.topics["config_hum"]
        self.__hum_config_payload = config.hum_payload
        self.__gas_config_topic = config.topics["config_gas"]
        self.__gas_config_payload = config.gas_payload
        self.__press_config_topic = config.topics["config_press"]
        self.__press_config_payload = config.press_payload
        
        self.__rgb_config_topic = config.topics["config_rgb"]
        self.__rgb_config_payload = config.rgb_payload
        self.__rgb_command_topic = config.topics["command_rgb"]
        self.__rgb_status_topic= config.topics["status_rgb"]
        self.__rgb_color_command_topic = config.topics["command_rgb_color"]
        self.__rgb_color_status_topic= config.topics["status_rgb_color"]
        
        self.__bme680_topic = config.topics["bme680"]
        self.__color = Color(255,0,0)
        self.__alarm_armed = self.DISARMED
        self.__rgb_state = self.RGB_OFF
        
        self.__alarm_config_topic = config.topics["config_alarm"]
        self.__alarm_config_payload = config.alarm_payload
        self.__alarm_command_topic = config.topics["command_alarm"]
        self.__alarm_status_topic= config.topics["status_alarm"]
        
        
    def initialize_wifi(self) -> bool:
        """
        Initializes the Wi-Fi connection.

        Returns:
            True if the Wi-Fi connection is successful, False otherwise.
        """
        self.__wlan = network.WLAN(network.STA_IF)
        self.__wlan.active(True)

        # Connect to the network
        self.__wlan.connect(self.__ssid, self.__psw)

        # Wait for Wi-Fi connection
        connection_timeout = 10
        while connection_timeout > 0:
            if self.__wlan.status() >= 3:
                break
            connection_timeout -= 1
            print('Waiting for Wi-Fi connection...')
            sleep(1)

        # Check if connection is successful
        if self.__wlan.status() != 3:
            return False
        else:
            print('Connection successful!')
            network_info = self.__wlan.ifconfig()
            print('IP address:', network_info[0])
            return True
        
    def is_wifi_connected(self) -> bool:
        """
        Checks if the Wi-Fi connection is established.

        Returns:
            True if the Wi-Fi connection is established, False otherwise.
        """
        return self.__wlan.isConnected()
    
    def connect_mqtt(self) -> None:
        """
        Connects to the MQTT broker.
        """
        try:
            self.__mqtt_client = MQTTClient(client_id=self.__mqtt_client_id,
                                server=self.__mqtt_server,
                                port=self.__mqtt_port,
                                user=self.__mqtt_user,
                                password=self.__mqtt_psw,
                                keepalive=self.__mqtt_keep_alive)
            
            self.__mqtt_client.connect()
        except Exception as e:
            print('Error connecting to MQTT:', e)
            raise  # Re-raise the exception to see the full traceback
        
    def config_bme680_sensor(self) -> None:
        """
        Configures the BME680 sensor by publishing the configuration payloads to the respective topics.
        """
        i = 0
        while i < 5:
            self.__mqtt_client.publish(self.__temp_config_topic, json.dumps(self.__temp_config_payload))
            sleep(0.25)
            self.__mqtt_client.publish(self.__hum_config_topic, json.dumps(self.__hum_config_payload))
            sleep(0.25)
            self.__mqtt_client.publish(self.__gas_config_topic, json.dumps(self.__gas_config_payload))
            sleep(0.25)
            self.__mqtt_client.publish(self.__press_config_topic, json.dumps(self.__press_config_payload))
            sleep(0.25)
            i+=1
            
    def send_bme680_data(self, temp, hum, gas, press) -> None:
        """
        Publishes the BME680 sensor data to the MQTT broker.

        Args:
            temp: The temperature value.
            hum: The humidity value.
            gas: The gas value.
            press: The pressure value.
        """
        data = {
            "temperature": temp,
            "humidity": hum,
            "gas": gas,
            "pressure": press
            }
        self.__mqtt_client.publish(self.__bme680_topic, json.dumps(data))
        
    def config_actuators(self) -> None:
        """
        Configures the actuators by publishing the configuration payloads to the respective topics.
        """
        i = 0
        while i < 5:
            self.__mqtt_client.publish(self.__rgb_config_topic, json.dumps(self.__rgb_config_payload))
            sleep(0.25)
            self.__mqtt_client.publish(self.__alarm_config_topic, json.dumps(self.__alarm_config_payload))
            sleep(0.25)
            i+=1
            
        self.__mqtt_client.set_callback(self._my_callback)
        
        self.__mqtt_client.publish(self.__rgb_status_topic, b'OFF')
        sleep(0.25)
        self.__mqtt_client.publish(self.__alarm_status_topic, b'disarmed')
        
        i = 0
        while i < 1:
            self.__mqtt_client.subscribe(self.__rgb_command_topic)
            self.__mqtt_client.subscribe(self.__rgb_color_command_topic)
            self.__mqtt_client.subscribe(self.__alarm_command_topic)
            i+=1
    
    def check_new_message(self) -> None:
        """
        Checks for new messages from the MQTT broker.
        """
        self.__mqtt_client.check_msg()
    
    def _my_callback(self,topic, message) -> None:
        """
        Callback function for handling incoming MQTT messages.

        Args:
            topic: The topic of the incoming message.
            message: The payload of the incoming message.
        """
        msg_clear = message.decode()
        topic_clear = topic.decode()
        if topic_clear == self.__rgb_command_topic:
            if msg_clear == "ON" and self.__alarm_armed != self.TRIGGERED:
                self.__rgb_state = self.RGB_ON
            else:
                self.__rgb_state = self.RGB_OFF
                
        elif topic_clear == self.__rgb_color_command_topic:
            data_received = msg_clear.split(',')
            r,g,b = data_received
            self.__color = Color(int(b),int(g),int(r))
            
        elif topic_clear == self.__alarm_command_topic:
            if msg_clear == "DISARM":
                self.__alarm_armed = self.DISARMED
            elif msg_clear == "ARM_AWAY":
                self.__alarm_armed = self.ARMED
            else:
                self.__alarm_armed = self.TRIGGERED
                self.__rgb_state = self.RGB_OFF
   
    def alarm_status(self) -> int:
        """
        Returns the current status of the alarm.

        Returns:
            The alarm status (ARMED, DISARMED, or TRIGGERED).
        """
        return self.__alarm_armed
    
    def rgb_state(self) -> tuple:
        """
        Returns the current state of the RGB LED.

        Returns:
            The RGB color and state (ON or OFF).
        """
        return self.__color, self.__rgb_state
    
    def set_rgb_state(self, status: int, color: Color) -> None:
        """
        Sets the state of the RGB LED.

        Args:
            status: The desired state of the RGB LED (RGB_ON or RGB_OFF).
            color: The desired color of the RGB LED.
        """
        msg = b''
        msg_color = (str(color._color[2])+","+str(color._color[1])+","+str(color._color[0])).encode()
        if status == self.RGB_OFF:
            msg = b'OFF'
            self.__rgb_state = self.RGB_OFF
        elif status == self.RGB_ON:
            msg = b'ON'
            self.__rgb_state = self.RGB_ON
        i = 0
        while i < 3:
            self.__mqtt_client.publish(self.__rgb_status_topic.encode(), msg)
            self.__mqtt_client.publish(self.__rgb_color_status_topic.encode(), msg_color)
            i+=1
    
    def set_alarm_status(self, status: int) -> None:
        """
        Sets the status of the alarm.

        Args:
            status: The desired status of the alarm (DISARMED, ARMED, or TRIGGERED).
        """
        msg = b''
        if status == self.DISARMED:
            msg = b'disarmed'
            self.__alarm_armed = self.DISARMED
        elif status == self.ARMED:
            msg = b'armed_away'
            self.__alarm_armed = self.ARMED
        elif status == self.TRIGGERED:
            msg = b'triggered'
            self.__alarm_armed = self.TRIGGERED
            self.__rgb_state = self.RGB_OFF
            self.__mqtt_client.publish(self.__rgb_status_topic.encode(), b'OFF')
        i = 0
        while i < 3:
            self.__mqtt_client.publish(self.__alarm_status_topic.encode(), msg)
            i+=1
            
    def disconnect_mqtt(self) -> None:
        """
        Disconnects from the MQTT broker.
        """
        self.__mqtt_client.disconnect()
        
        
