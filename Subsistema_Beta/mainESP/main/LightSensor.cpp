/**
 * @file LightSensor.cpp
 * @brief Implementation file for the LightSensor class.
 */

#include "LightSensor.h"

/**
 * @brief Constructs a LightSensor object with the specified light pin.
 * @param light_pin The pin connected to the light sensor.
 */
LightSensor::LightSensor(uint8_t light_pin) {
    // Aquí puedes inicializar cualquier miembro de la clase si es necesario
    this->light_pin = light_pin;
    pinMode(light_pin, INPUT);
}

/**
 * @brief Gets the light level based on the analog reading from the light sensor.
 * @return The light level as a LightLevel enum value.
 */
LightLevel LightSensor::getLightLevel() {
    uint16_t light_value = analogRead(light_pin);
    if (light_value <= 1000) {
        return DARK;
    } else if (light_value <= 2000) {
        return LOW_LIGHT;
    } else if (light_value <= 4000) {
        return NORMAL_LIGHT;
    } else {
        return HIGH_LIGHT;
    }
}

/**
 * @brief Gets the raw analog reading from the light sensor.
 * @return The analog reading as a uint16_t value.
 */
uint16_t LightSensor::getLightValue() {
    return analogRead(light_pin);
}