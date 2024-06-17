/**
 * @file MotionSensor.cpp
 * @brief Implementation file for the MotionSensor class.
 * 
 * This file contains the implementation of the MotionSensor class, which represents a motion sensor device.
 * The MotionSensor class provides methods to enable/disable motion detection, check if motion is detected, and check if motion has ended.
 * 
 * @author Fabio Antonio Valente
 */

#include "MotionSensor.h"

// Static variables
volatile static bool motionDetected = false; 
volatile static bool motionEnded = false;
static uint8_t pin; 

// Callback function prototypes
static void onRise(void);
static void onFall(void);

/**
 * @brief Callback function for the rising edge interrupt.
 * 
 * This function is called when a rising edge interrupt is triggered.
 * It sets the motionDetected flag to true and the motionEnded flag to false.
 */
static void onRise(void){
    motionDetected = true;
    motionEnded = false;
}

/**
 * @brief Callback function for the falling edge interrupt.
 * 
 * This function is called when a falling edge interrupt is triggered.
 * It sets the motionDetected flag to false and the motionEnded flag to true.
 */
static void onFall(void){
    motionDetected = false;
    motionEnded = true;
}

/**
 * @brief Constructor for the MotionSensor class.
 * 
 * This constructor initializes the motionDetected and motionEnded flags to false.
 * It also sets the pin number for the motion sensor.
 * 
 * @param pin_p The pin number for the motion sensor.
 */
MotionSensor::MotionSensor(uint8_t pin_p) {
    pin = pin_p;
    motionDetected = false;
    motionEnded = false;
    pinMode(pin, INPUT);
}

/**
 * @brief Destructor for the MotionSensor class.
 * 
 * This destructor resets the motionDetected and motionEnded flags to false.
 * It also detaches the interrupt for the motion sensor pin.
 */
MotionSensor::~MotionSensor() {
    motionDetected = false;
    motionEnded = false;
    detachInterrupt(digitalPinToInterrupt(pin));
}

/**
 * @brief Enable motion detection.
 * 
 * This method enables motion detection by setting the motionDetected and motionEnded flags to false.
 * It also attaches the interrupt for the motion sensor pin, triggering on a rising edge.
 */
void MotionSensor::enableMotionDetection(void){
    motionDetected = false;
    motionEnded = false;
    attachInterrupt(digitalPinToInterrupt(pin),onRise, RISING);
}

/**
 * @brief Disable motion detection.
 * 
 * This method disables motion detection by setting the motionDetected and motionEnded flags to false.
 * It also detaches the interrupt for the motion sensor pin.
 */
void MotionSensor::disableMotionDetection(void){
    motionDetected = false;
    motionEnded = false;
    detachInterrupt(digitalPinToInterrupt(pin));
}

/**
 * @brief Check if motion is detected.
 * 
 * This method checks if motion is detected by checking the motionDetected and motionEnded flags.
 * If motion is detected and motion has not ended, it sets the motionDetected flag to false and attaches the interrupt for the motion sensor pin, triggering on a falling edge.
 * 
 * @return True if motion is detected, false otherwise.
 */
bool MotionSensor::isMotionDetected() {
    if(motionDetected && !motionEnded){
        motionDetected = false;
        attachInterrupt(digitalPinToInterrupt(pin),onFall, FALLING);
        return true;
    }
    return false;
}

/**
 * @brief Check if motion has ended.
 * 
 * This method checks if motion has ended by checking the motionDetected and motionEnded flags.
 * If motion has ended and motion was not detected, it sets the motionEnded flag to false and attaches the interrupt for the motion sensor pin, triggering on a rising edge.
 * 
 * @return True if motion has ended, false otherwise.
 */
bool MotionSensor::isMotionEnded() {
    if(!motionDetected && motionEnded){
        motionEnded = false;
        attachInterrupt(digitalPinToInterrupt(pin),onRise, RISING);
        return true;
    }
    return false;
}
