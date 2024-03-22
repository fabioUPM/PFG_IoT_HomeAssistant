/**
 * @file Buzzer.cpp
 * @brief Implementation of the Buzzer class.
 * @author Fabio Antonio Valente
 */

#include "Buzzer.h"

/**
 * @brief Constructor for the Buzzer class.
 * @param buzzer_pin The pin number to which the buzzer is connected.
 */
Buzzer::Buzzer(uint8_t buzzer_pin) {
    this->buzzer_pin = buzzer_pin;
    pinMode(buzzer_pin, OUTPUT);
    buzzerIsOn = false;
    this->frequency = 0;
    this->duration = 0;
}

/**
 * @brief Destructor for the Buzzer class.
 */
Buzzer::~Buzzer() {
    // Destructor
    turnOff();
}

/**
 * @brief Turns off the buzzer.
 */
void Buzzer::turnOff() {
    noTone(buzzer_pin);
    buzzerIsOn = false;
}

/**
 * @brief Turns on the buzzer with the specified frequency and duration.
 */
void Buzzer::turnOn() {
    tone(buzzer_pin, frequency, duration);
    buzzerIsOn = true;
}

/**
 * @brief Sets the frequency of the buzzer.
 * @param frequency The frequency to set.
 */
void Buzzer::setFrequency(unsigned int frequency) {
    this->frequency = frequency;
    if(buzzerIsOn) {
        turnOn();
    } else {
        turnOff();
    }
}

/**
 * @brief Sets the duration of the buzzer.
 * @param duration The duration to set.
 */
void Buzzer::setDuration(unsigned int duration = 0) {
    this->duration = duration;
}

/**
 * @brief Checks if the buzzer is currently on.
 * @return True if the buzzer is on, false otherwise.
 */
bool Buzzer::isOn() {
    return buzzerIsOn;
}