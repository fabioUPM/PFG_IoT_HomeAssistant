/**
 * @file FlameDetector.h
 * @brief Header file for the FlameDetector class.
 * @author Fabio Antonio Valente
 * 
 * This file contains the declaration of the FlameDetector class, which represents a flame detection sensor.
 * The class provides methods to enable/disable the flame detection, check if a flame is detected,
 * check if the flame has ended, and get the intensity of the flame.
 */
#ifndef FLAME_H
#define FLAME_H
#include "Arduino.h"

/**
 * @brief The FlameDetector class represents a flame detection sensor.
 * 
 * This class provides methods to enable/disable the flame detection, check if a flame is detected,
 * check if the flame has ended, and get the intensity of the flame.
 */
class FlameDetector {
public:
    /**
     * @brief Constructs a new FlameDetector object.
     * 
     * @param flame_digital_pin The digital pin connected to the flame detection sensor.
     * @param flame_analog_pin The analog pin connected to the flame detection sensor.
     */
    FlameDetector(uint8_t flame_digital_pin, uint8_t flame_analog_pin);

    /**
     * @brief Destroys the FlameDetector object.
     */
    ~FlameDetector();

    /**
     * @brief Enables flame detection.
     * 
     * This method initializes the flame detection sensor.
     */
    void enableFlameDetection();

    /**
     * @brief Disables flame detection.
     * 
     * This method deactivates the flame detection sensor.
     */
    void disableFlameDetection();

    /**
     * @brief Checks if a flame is detected.
     * 
     * @return true if a flame is detected, false otherwise.
     */
    bool isFlameDetected();

    /**
     * @brief Checks if the flame has ended.
     * 
     * @return true if the flame has ended, false otherwise.
     */
    bool isFlameEnded();

    /**
     * @brief Gets the intensity of the flame.
     * 
     * @return The intensity of the flame as a 16-bit unsigned integer.
     */
    uint16_t getFlameIntensity();

private:
    // Private variables and methods necessary for the implementation of the flame detection sensor
    uint8_t __flame_analog_pin; // Analog pin of the flame detection sensor
};

#endif