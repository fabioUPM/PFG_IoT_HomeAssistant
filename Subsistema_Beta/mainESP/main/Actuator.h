#ifndef ACTUATOR_H
#define ACTUATOR_H

#include "Arduino.h"
#include "esp32-hal-timer.h"
#include "esp32-hal-ledc.h"

/**
 * @brief The Actuator class represents an actuator component.
 * 
 * This class provides methods to control the buzzer and RGB LED. It allows turning the buzzer on/off, setting the frequency and duration, checking if the buzzer is currently turned on, turning the RGB LED on/off, and setting the color of the RGB LED.
 */
class Actuator {
public:
    /**
     * @brief Constructs an Actuator object with the specified buzzer pin and RGB LED pins.
     * 
     * @param buzzer_pin The pin connected to the buzzer.
     * @param redPin The pin number for the red color of the RGB LED.
     * @param greenPin The pin number for the green color of the RGB LED.
     * @param bluePin The pin number for the blue color of the RGB LED.
     */
    Actuator(uint8_t buzzer_pin, uint8_t redPin, uint8_t greenPin, uint8_t bluePin);

    /**
     * @brief Constructs an Actuator object.
     */
    Actuator();

    /**
     * @brief Destroys the Actuator object.
     */
    ~Actuator();

    /**
     * @brief Turns off the buzzer.
     */
    void turnOffBuzzer(void);

    /**
     * @brief Turns on the buzzer.
     */
    void turnOnBuzzer(void);

    /**
     * @brief Sets the frequency of the buzzer.
     * 
     * @param frequency The frequency to set.
     */
    void setBuzzerFrequency(unsigned int frequency);

    /**
     * @brief Sets the duration of the buzzer.
     * 
     * @param duration The duration to set.
     */
    void setBuzzerDuration(unsigned int duration);

    /**
     * @brief Checks if the buzzer is currently turned on.
     * 
     * @return True if the buzzer is turned on, false otherwise.
     */
    bool buzzerIsOn(void);

    /**
     * @brief Turns on the RGB LED.
     */
    void turnOnRGB(void);

    /**
     * @brief Turns off the RGB LED.
     */
    void turnOffRGB(void);

    /**
     * @brief Sets the color of the RGB LED.
     * 
     * @param red The intensity of the red color (0-255).
     * @param green The intensity of the green color (0-255).
     * @param blue The intensity of the blue color (0-255).
     */
    void setRGBColor(uint16_t red, uint16_t green, uint16_t blue);

private:
    uint8_t buzzer_pin; // The pin connected to the buzzer
    unsigned int frequency; // The frequency of the buzzer
    unsigned int duration; // The duration of the buzzer
    bool _buzzerIsOn; // Flag indicating if the buzzer is turned on

    uint8_t redPin; /**< The pin number for the red color. */
    uint8_t greenPin; /**< The pin number for the green color. */
    uint8_t bluePin; /**< The pin number for the blue color. */
    uint16_t red; /**< The intensity of the red color (0-255). */
    uint16_t green; /**< The intensity of the green color (0-255). */
    uint16_t blue; /**< The intensity of the blue color (0-255). */
    bool RGBIsOn; /**< Indicates whether the RGB LED is turned on or off. */

};

#endif