#include "Arduino.h"
/**
 * @file FlameDetector.cpp
 * @brief Implementation file for the FlameDetector class.
 * @author Fabio Antonio Valente
 */

#include "FlameDetector.h"

volatile static bool flameDetected = false; 
volatile static bool flameEnded = false;
volatile static uint8_t pin;

// Callback function prototypes
static void onRise(void);
static void onFall(void);

/**
 * @brief Constructs a FlameDetector object with the specified digital and analog pins.
 * @param flame_digital_pin The digital pin connected to the flame detector module.
 * @param flame_analog_pin The analog pin connected to the flame detector module.
 */
FlameDetector::FlameDetector(uint8_t flame_digital_pin, uint8_t flame_analog_pin) {
    pin = flame_digital_pin;
    pinMode(flame_digital_pin, INPUT);
    pinMode(flame_analog_pin, INPUT);
    this->__flame_analog_pin = flame_analog_pin;
}

/**
 * @brief Destroys the FlameDetector object.
 */
FlameDetector::~FlameDetector() {
    flameDetected = false;
    flameEnded = false;
    this->disableFlameDetection();
}

/**
 * @brief Enables flame detection by attaching an interrupt to the digital pin.
 */
void FlameDetector::enableFlameDetection() {
    detachInterrupt(digitalPinToInterrupt(pin));
    delay(100);
    attachInterrupt(digitalPinToInterrupt(pin), onRise, RISING);
    delay(100);
    flameDetected = false;
    flameEnded = false;
}

/**
 * @brief Disables flame detection by detaching the interrupt from the digital pin.
 */
void FlameDetector::disableFlameDetection() {
    detachInterrupt(digitalPinToInterrupt(pin));
    flameDetected = false;
    flameEnded = false;
}

/**
 * @brief Checks if a flame is currently detected.
 * @return True if a flame is detected, false otherwise.
 */
bool FlameDetector::isFlameDetected() {
    if (flameDetected && !flameEnded) {
        flameDetected = false;
        detachInterrupt(digitalPinToInterrupt(pin));
        delay(100);
        attachInterrupt(digitalPinToInterrupt(pin), onFall, FALLING);
        return true;
    }
    return false;
}

/**
 * @brief Checks if the flame has ended.
 * @return True if the flame has ended, false otherwise.
 */
bool FlameDetector::isFlameEnded() {
    if (flameEnded && !flameDetected) {
        flameEnded = false;
        detachInterrupt(digitalPinToInterrupt(pin));
        delay(100);
        attachInterrupt(digitalPinToInterrupt(pin), onRise, RISING);
        return true;
    }
    return false;
}

/**
 * @brief Gets the intensity of the flame.
 * @return The intensity of the flame as an unsigned 16-bit integer.
 */
uint16_t FlameDetector::getFlameIntensity() {
    return analogRead(this->__flame_analog_pin);
}

/**
 * @brief Callback function called when the flame is detected.
 */
static void onRise(void) {
    flameDetected = true;
    flameEnded = false;
}

/**
 * @brief Callback function called when the flame ends.
 */
static void onFall(void) {
    flameDetected = false;
    flameEnded = true;
}