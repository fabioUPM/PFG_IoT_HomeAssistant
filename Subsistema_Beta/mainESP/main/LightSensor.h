/**
 * @file LightSensor.h
 * @brief Header file for the LightSensor class.
 * @author Fabio Antonio Valente
 * 
 * This file defines the LightSensor class, which represents a light sensor component.
 * The LightSensor class provides methods to get the light level and light value.
 */

#ifndef LIGHT_H
#define LIGHT_H

#include "Arduino.h"

/**
 * @enum LightLevel
 * @brief Enumeration for different light levels.
 * 
 * This enumeration defines different light levels that can be detected by the light sensor.
 * The light levels include DARK, LOW_LIGHT, NORMAL_LIGHT, and HIGH_LIGHT.
 */
enum LightLevel {
    DARK, // 0-100
    LOW_LIGHT, // 101-400
    NORMAL_LIGHT, // 401-600
    HIGH_LIGHT // >600
};

/**
 * @class LightSensor
 * @brief Class representing a light sensor component.
 * 
 * The LightSensor class provides methods to interact with a light sensor.
 * It allows getting the light level and light value from the sensor.
 */
class LightSensor {
public:
    /**
     * @brief Constructor for the LightSensor class.
     * @param light_pin The pin number to which the light sensor is connected.
     */
    LightSensor(uint8_t light_pin);

    /**
     * @brief Get the light level detected by the sensor.
     * @return The light level as a LightLevel enum value.
     */
    LightLevel getLightLevel();

    /**
     * @brief Get the raw light value from the sensor.
     * @return The light value as a uint16_t.
     */
    uint16_t getLightValue();

private:
    // Here you can add any private members you need
    uint8_t light_pin;
};

#endif