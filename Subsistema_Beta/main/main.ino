/* Example code for HC-SR501 PIR motion sensor with Arduino. More info: www.www.makerguides.com */

#include "MotionSensor.h"
#include "Fan.h"
// Define connection pins:
#define pirPin 2 //NARANJA
#define ledPin 13

#define PIN_ENABLE 8 //BLANCO
#define PIN_DIR_CW 10 //NARANJA
#define PIN_DIR_CCW 9 //AZUL

//MotionSensor motion(pirPin);
Fan fan(PIN_ENABLE, PIN_DIR_CW, PIN_DIR_CCW);

void setup() {
  // Configure the pins as input or output:

  fan.initializeFan();
  fan.setSpeed(200);
  fan.setDirection(COUNTER_CLOCKWISE);

  // Begin serial communication at a baud rate of 9600:
  Serial.begin(9600);
  //motion.enableMotionDetection();
  Serial.println("Comienza prueba");
  delay(5000);
}

void loop() {

  fan.setDirection(COUNTER_CLOCKWISE);
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
  delay(2000);

  /*if(motion.isMotionDetected()){
    analogWrite(ledPin, HIGH); // Turn on the on-board LED.
    Serial.println("Motion detected!");
  } else if(motion.isMotionEnded()){
    analogWrite(ledPin, LOW); // Turn off the on-board LED.
    Serial.println("Motion ended!");
  }*/
}