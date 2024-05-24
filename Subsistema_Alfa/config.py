"""
This module contains the configuration settings for the IoT subsystem in the Home Assistant project.

Attributes:
    wifi_ssid (str): The SSID of the WiFi network.
    wifi_psw (str): The password for the WiFi network.
    mqtt (dict): The MQTT broker configuration settings.
    topics (dict): The MQTT topics for different sensors and devices.
    alarm_payload (dict): The configuration payload for the alarm control panel.
    rgb_payload (dict): The configuration payload for the RGB light.
    temp_payload (dict): The configuration payload for the temperature sensor.
    hum_payload (dict): The configuration payload for the humidity sensor.
    gas_payload (dict): The configuration payload for the gas resistance sensor.
    press_payload (dict): The configuration payload for the pressure sensor.
"""

wifi_ssid = 'IoT'
wifi_psw = 'bgwdq77634'

mqtt = {
    "client_id": b"rpi_pico_exterior",
    "server": b'192.168.0.102',
    "port": 1883,
    "user": b'rpi',
    "psw": b'18102002',
    "keep_alive": 65535
}

topics ={
    "config_temp": "homeassistant/sensor/picoTemp/config",
    "config_hum": "homeassistant/sensor/picoHum/config",
    "config_gas": "homeassistant/sensor/picoGas/config",
    "config_press": "homeassistant/sensor/picoPress/config",
    "config_rgb": "homeassistant/light/picoRGB/config",
    "config_alarm": "homeassistant/alarm_control_panel/picoAlarm/config",
    "status_rgb": "rgb/pico/status/light",
    "command_rgb": "rgb/pico/command/light",
    "status_rgb_color": "rgb/pico/status/color",
    "command_rgb_color": "rgb/pico/command/color",
    "status_alarm": "rgb_buzzer/pico/status/alarm",
    "command_alarm": "rgb_buzzer/pico/command/alarm",
    "bme680": "bme680/pico/status/sensor"
}

alarm_payload ={
    "device_class":"alarm_control_panel",
    "name": "Backyard Alarm",
    "state_topic":topics["status_alarm"],
    "command_topic":topics["command_alarm"],
    "code_arm_required": True,
    "code_disarm_required": True,
    "code_trigger_required": True,
    "code": 1234,
    "payload_arm_away": "ARM_AWAY",
    "payload_disarm": "DISARM",
    "payload_trigger": "TRIGGER",
    "state_disarmed": "disarmed",
    "state_armed_away": "armed_away",
    "state_triggered": "triggered",
    "supported_features": ["arm_away", "trigger"],
    "unique_id":"alarm01by",
    "device":{
       "identifiers":[
           "backyard01by"
       ]}
}

rgb_payload ={
    "device_class":"light",
    "name": "Backyard Light",
    "state_topic":topics["status_rgb"],
    "command_topic":topics["command_rgb"],
    "rgb_state_topic":topics["status_rgb_color"],
    "rgb_command_topic":topics["command_rgb_color"],
    "rgb_value_template": "{{ value_json.rgb | join(',') }}",
    "payload_on": "ON",
    "payload_off": "OFF",
    "state_on": "ON",
    "state_off": "OFF",
    "restore_mode": "ALWAYS_OFF",
    "unique_id":"light01by",
    "device":{
       "identifiers":[
           "backyard01by"
       ]}
}

temp_payload ={
    "device_class":"temperature",
    "name": "Backyard Temperature",
    "state_topic":topics["bme680"],
    "unit_of_measurement":"C",
    "value_template":"{{ value_json.temperature}}",
    "unique_id":"temp01by",
    "device":{
       "identifiers":[
           "backyard01by"
       ]}
}

hum_payload ={
    "device_class":"humidity",
    "name": "Backyard Humidity",
    "state_topic":topics["bme680"],
    "unit_of_measurement":"%",
    "value_template":"{{ value_json.humidity}}",
    "unique_id":"hum01by",
    "device":{
       "identifiers":[
           "backyard01by"
       ]}
}

gas_payload ={
    "device_class":"gas",
    "name": "Backyard Gas Resistence",
    "state_topic":topics["bme680"],
    "unit_of_measurement":"kOhm",
    "value_template":"{{ value_json.gas}}",
    "unique_id":"gas01by",
    "device":{
       "identifiers":[
           "backyard01by"
       ]}
}

press_payload ={
    "device_class":"pressure",
    "name": "Backyard Pressure",
    "state_topic":topics["bme680"],
    "unit_of_measurement":"hPa",
    "value_template":"{{ value_json.pressure}}",
    "unique_id":"press01by",
    "device":{
       "identifiers":[
           "backyard01by"
       ]}
}

