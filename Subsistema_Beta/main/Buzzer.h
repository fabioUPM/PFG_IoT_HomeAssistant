#ifndef BUZZER_H
#define BUZZER_H

#include "Arduino.h"

/**
 * @brief The Buzzer class represents a buzzer component.
 * 
 * This class provides methods to control the buzzer, such as turning it on/off, setting the frequency and duration,
 * and checking if it is currently turned on.
 */
class Buzzer {
public:
    /**
     * @brief Constructs a Buzzer object with the specified buzzer pin.
     * 
     * @param buzzer_pin The pin connected to the buzzer.
     */
    Buzzer(uint8_t buzzer_pin);

    /**
     * @brief Destroys the Buzzer object.
     */
    ~Buzzer();

    /**
     * @brief Turns off the buzzer.
     */
    void turnOff();

    /**
     * @brief Turns on the buzzer.
     */
    void turnOn();

    /**
     * @brief Sets the frequency of the buzzer.
     * 
     * @param frequency The frequency to set.
     */
    void setFrequency(unsigned int frequency);

    /**
     * @brief Sets the duration of the buzzer.
     * 
     * @param duration The duration to set.
     */
    void setDuration(unsigned int duration);

    /**
     * @brief Checks if the buzzer is currently turned on.
     * 
     * @return True if the buzzer is turned on, false otherwise.
     */
    bool isOn();

private:
    uint8_t buzzer_pin; // The pin connected to the buzzer
    unsigned int frequency; // The frequency of the buzzer
    unsigned int duration; // The duration of the buzzer
    bool buzzerIsOn; // Flag indicating if the buzzer is turned on
};

#endif