/* Example code for HC-SR501 PIR motion sensor with Arduino. More info: www.www.makerguides.com */

#include "MotionSensor.h"
#include "Fan.h"
#include "LightSensor.h"
#include "DHT.h"
#include "FlameDetector.h"
#include "RGB.h"
#include "Buzzer.h"
#include "Alarm.h"


// Define connection pins:

// Motion Sensor PINs
#define pirPin 2 //NARANJA
#define ledPin 13

// Fan pins
#define PIN_ENABLE 8 //BLANCO
#define PIN_DIR_CW 10 //NARANJA
#define PIN_DIR_CCW 9 //AZUL

// DHT pins
#define DHTPIN 4 //AZUL
#define DHTTYPE DHT11   // DHT 11

// Light Sensor pins
#define LIGHT_SENSOR_PIN A0

// Flame Sensor pins
#define FLAME_DIGITAL 3
#define FLAME_ANALOG A1

//RGB LED pins
#define RED_PIN 5
#define GREEN_PIN 6
#define BLUE_PIN 7

//Buzzer pins
#define BUZZER_PIN 11

//MotionSensor motion(pirPin);
//Fan fan(PIN_ENABLE, PIN_DIR_CW, PIN_DIR_CCW);
//dht11 DHT;
//DHT dht(DHTPIN, DHTTYPE);

//LightSensor light(LIGHT_SENSOR_PIN);

//FlameDetector flame(FLAME_DIGITAL, FLAME_ANALOG);

RGBLed rgb(RED_PIN, GREEN_PIN, BLUE_PIN);
Buzzer buzzer(BUZZER_PIN);
Alarm alarm;

void setup() {
  // Configure the pins as input or output:
  Serial.begin(9600);
  Serial.println("Comienza prueba");
  //dht.begin();
  //flame.enableFlameDetection();
  digitalWrite(ledPin, LOW);
  rgb.setColor(0,0,0);
  alarm.configureAlarmLEDs(rgb);
  alarm.configureAlarmBuzzer(buzzer);
}


void loop() {
  
  delay(5000);
  alarm.activateAlarm();
  delay(500);
  alarm.deactivateAlarm();



  /*if(flame.isFlameDetected()){
    digitalWrite(ledPin, HIGH);
  } else if (flame.isFlameEnded()) {
    digitalWrite(ledPin, LOW);
  } else {
    Serial.println(flame.getFlameIntensity());
  }*/



  /*uint16_t value = light.getLightValue();
  LightLevel k = light.getLightLevel();

  if(k == DARK || k == LOW_LIGHT){
    digitalWrite(ledPin, HIGH);
  } else {
    digitalWrite(ledPin, LOW);
  }

  Serial.print("Analog  Value: ");
  Serial.println(value);*/



  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  //uint16_t h = dht.readHumidity();
  // Read temperature as Celsius (the default)
  //float t = dht.readTemperature();


  // Check if any reads failed and exit early (to try again).
  /*if (isnan(h) || isnan(t)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }

  Serial.print(F("Humidity: "));
  Serial.print(h);
  Serial.print(F("%  Temperature: "));
  Serial.print(t);
  Serial.println(F("°C "));*/

  
  /*fan.setDirection(COUNTER_CLOCKWISE);
  fan.turnOn();
  for(uint16_t i= 100; i < 256; i++){
      fan.setSpeed(i);
      delay(100);
  }
  fan.setDirection(CLOCKWISE);
  delay(1000);
  for(uint16_t i = 255; i >= 100; i--){
      fan.setSpeed(i);
      delay(100);
  }
  fan.turnOff();
  delay(2000);*/

  /*if(motion.isMotionDetected()){
    analogWrite(ledPin, HIGH); // Turn on the on-board LED.
    Serial.println("Motion detected!");
  } else if(motion.isMotionEnded()){
    analogWrite(ledPin, LOW); // Turn off the on-board LED.
    Serial.println("Motion ended!");
  }*/
}