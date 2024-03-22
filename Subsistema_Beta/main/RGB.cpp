/**
 * @file RGB.cpp
 * @brief Implementation file for the RGBLed class.
 * @author Fabio Antonio Valente
 */

#include "RGB.h"

/**
 * @brief Constructs an RGBLed object with the specified pin numbers for red, green, and blue.
 * 
 * @param redPin The pin number for the red LED.
 * @param greenPin The pin number for the green LED.
 * @param bluePin The pin number for the blue LED.
 */
RGBLed::RGBLed(uint8_t redPin, uint8_t greenPin, uint8_t bluePin) {
    this->redPin = redPin;
    this->greenPin = greenPin;
    this->bluePin = bluePin;
    this->red = 0;
    this->green = 0;
    this->blue = 0;
    this->isOn = false;
    pinMode(redPin, OUTPUT);
    pinMode(greenPin, OUTPUT);
    pinMode(bluePin, OUTPUT);
}

/**
 * @brief Destructor for the RGBLed object.
 * Turns off the LED before destroying the object.
 */
RGBLed::~RGBLed() {
    turnOff();
}

/**
 * @brief Turns on the RGB LED with the current color settings.
 */
void RGBLed::turnOn() {
    analogWrite(redPin, red);
    analogWrite(greenPin, green);
    digitalWrite(bluePin, blue);
    this->isOn = true;
}

/**
 * @brief Turns off the RGB LED.
 */
void RGBLed::turnOff() {
    analogWrite(redPin, 0);
    analogWrite(greenPin, 0);
    digitalWrite(bluePin, 0);
    this->isOn = false;
}

/**
 * @brief Sets the color of the RGB LED.
 * 
 * @param red The intensity of the red color (0-255).
 * @param green The intensity of the green color (0-255).
 * @param blue The intensity of the blue color (0-255).
 */
void RGBLed::setColor(uint16_t red, uint16_t green, uint16_t blue) {
    if (red > 255) {
        this->red = 255;  
    } else if (red < 0) {
        this->red = 0;
    } else {
        this->red = red;
    }
    if (green > 255) {
        this->green = 255;
    } else if (green < 0) {
        this->green = 0;
    } else {
        this->green = green;
    }
    if (blue > 1) {
        this->blue = 1;
    } else if (blue < 0) {
        this->blue = 0;
    } else {
        this->blue = blue;
    }
    if (isOn) {
        turnOn();
    } else {
        turnOff();
    }
}
