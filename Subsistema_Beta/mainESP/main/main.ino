/* Example code for HC-SR501 PIR motion sensor with Arduino. More info: www.www.makerguides.com */

#include "MotionSensor.h"
#include "Actuator.h"
#include "LightSensor.h"
#include "DHT.h"  //Cambiar la libreria
#include "FlameDetector.h"
#include "Alarm.h"


// Define connection pins:

// Motion Sensor PINs
#define pirPin 34  //NARANJA
#define ledPin 13

// DHT pins
#define DHTPIN 32      //AZUL
#define DHTTYPE DHT11  // DHT 11

// Light Sensor pins
#define LIGHT_SENSOR_PIN 36

// Flame Sensor pins
#define FLAME_DIGITAL 35
#define FLAME_ANALOG 39

//RGB LED pins
#define RED_PIN 33
#define GREEN_PIN 25
#define BLUE_PIN 26

//Buzzer pins
#define BUZZER_PIN 27

//Bluetooth pins
#define TX_PIN 1
#define RX_PIN 0


MotionSensor motion(pirPin);
DHT dht(DHTPIN, DHTTYPE);
LightSensor light(LIGHT_SENSOR_PIN);
FlameDetector flame(FLAME_DIGITAL, FLAME_ANALOG);
Actuator actuator(BUZZER_PIN, RED_PIN, GREEN_PIN, BLUE_PIN);
Alarm alarmFlameMotion;

unsigned long time_now = 0;
unsigned long time_now2 = 0;
uint16_t speed = 0;

void setup() {
  // Configure the pins as input or output:
  Serial.begin(9600);
  Serial.println("Comienza prueba");

  dht.begin();
  flame.enableFlameDetection();
  motion.enableMotionDetection();

  actuator.setRGBColor(0, 0, 0);
  actuator.turnOffRGB();
  actuator.turnOffBuzzer();
  alarmFlameMotion.configureAlarmActuator(actuator);

  time_now = millis();
  time_now2 = millis();
}


void loop() {

  /************* FLAME DETECTION**********/
  if (flame.isFlameDetected()) {
    alarmFlameMotion.activateFlameAlarm();
    //BT.write("FLAME DETECTED");
    //actuator.setRGBColor(0, 255, 0);
    //actuator.turnOnRGB();
    Serial.println("FLAME DETECTED");
  } else if (flame.isFlameEnded()) {
    alarmFlameMotion.deactivateFlameAlarm();
    //BT.write("FLAME ENDED");
    //actuator.setRGBColor(0, 0, 255);
    //actuator.turnOnRGB();
    Serial.println("FLAME ENDED");
  } else {
    //nothing
  }

  /************ MOTION DETECTION **********/
  if (motion.isMotionDetected()) {
    Serial.println("Motion detected");
    //BT.write("Motion detected");
    alarmFlameMotion.activateMotionAlarm();
    //actuator.setRGBColor(0, 255, 255);
    //actuator.turnOnRGB();
  } else if (motion.isMotionEnded()) {
    //BT.write("Motion ended");
    Serial.println("Motion ended");
    alarmFlameMotion.deactivateMotionAlarm();
    //actuator.setRGBColor(255, 255, 255);
    //actuator.turnOnRGB();
  } else {
    //nothing
  }

  /**************** LIGHT SENSOR *********/
  if (!alarmFlameMotion.getIsFlameActivated()) {
    if (millis() >= (time_now2 + 1000)) {
      time_now2 = millis();
      String mensaje = "Light: " + String(light.getLightValue());
      Serial.println(mensaje);
      LightLevel l = light.getLightLevel();
      if (l == DARK) {
        actuator.setRGBColor(255, 255, 255);
        //actuator.setBuzzerFrequency(1000);
        //actuator.turnOnBuzzer();
        actuator.turnOnRGB();

      } else if (l == LOW_LIGHT) {
        actuator.setRGBColor(0, 255, 0);
        //actuator.setBuzzerFrequency(500);
        //actuator.turnOnBuzzer();
        actuator.turnOnRGB();

      } else if (l == NORMAL_LIGHT) {
        actuator.setRGBColor(0, 0, 255);
        //actuator.setBuzzerFrequency(2000);
        //actuator.turnOnBuzzer();
        actuator.turnOnRGB();

      } else if (l == HIGH_LIGHT) {
        actuator.setRGBColor(255, 0, 0);
        //actuator.setBuzzerFrequency(1500);
        //actuator.turnOnBuzzer();
        actuator.turnOnRGB();
      } else {
        //nothing
      }
    }
  } else {
    //nothing
  }

  /*************** TEMP AND HUM ***********/
  if (millis() >= (time_now + 2000)) {
    time_now = millis();
    uint8_t h = dht.readHumidity();
    float t = dht.readTemperature();
    if (isnan(h) || isnan(t)) {
      Serial.println(F("Failed to read from DHT sensor!"));
    } else {
      String mensaje = "Temperatura: " + String(t) + " ºC, Humedad: " + String(h) + " %";
      Serial.print(F("Humidity: "));
      Serial.print(h);
      Serial.print(F("%  Temperature: "));
      Serial.print(t);
      Serial.println(F("°C "));
    }
  } else {
    //nothing
  }
}