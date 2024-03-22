#ifndef RGB_H
#define RGB_H

#include "Arduino.h"

/**
 * @brief Represents an RGB LED.
 */
class RGBLed {
public:
    /**
     * @brief Constructs an RGBLed object with the specified pin numbers for red, green, and blue.
     * 
     * @param redPin The pin number for the red color.
     * @param greenPin The pin number for the green color.
     * @param bluePin The pin number for the blue color.
     */
    RGBLed(uint8_t redPin, uint8_t greenPin, uint8_t bluePin);

    /**
     * @brief Destroys the RGBLed object.
     */
    ~RGBLed();

    /**
     * @brief Turns on the RGB LED.
     */
    void turnOn(void);

    /**
     * @brief Turns off the RGB LED.
     */
    void turnOff(void);

    /**
     * @brief Sets the color of the RGB LED.
     * 
     * @param red The intensity of the red color (0-65535).
     * @param green The intensity of the green color (0-65535).
     * @param blue The intensity of the blue color (0-65535).
     */
    void setColor(uint16_t red, uint16_t green, uint16_t blue);

private:
    uint8_t redPin; /**< The pin number for the red color. */
    uint8_t greenPin; /**< The pin number for the green color. */
    uint8_t bluePin; /**< The pin number for the blue color. */
    uint16_t red; /**< The intensity of the red color (0-255). */
    uint16_t green; /**< The intensity of the green color (0-255). */
    uint16_t blue; /**< The intensity of the blue color (0-255). */
    bool isOn; /**< Indicates whether the RGB LED is turned on or off. */
};

#endif