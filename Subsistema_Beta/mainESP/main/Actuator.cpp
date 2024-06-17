/**
 * @file Actuator.cpp
 * @brief Implementation of the Actuator class.
 * @author Fabio Antonio Valente
 */

#include "Actuator.h"
#include "esp32-hal-timer.h"
#include "esp32-hal-ledc.h"


/**
 * @brief Constructs an Actuator object with the specified buzzer pin and RGB LED pins.
 * 
 * @param buzzer_pin The pin connected to the buzzer.
 * @param redPin The pin number for the red color of the RGB LED.
 * @param greenPin The pin number for the green color of the RGB LED.
 * @param bluePin The pin number for the blue color of the RGB LED.
 */
Actuator::Actuator(uint8_t buzzer_pin, uint8_t redPin, uint8_t greenPin, uint8_t bluePin) {
    this->buzzer_pin = buzzer_pin;
    pinMode(buzzer_pin, OUTPUT);
    this->_buzzerIsOn = false;
    this->frequency = 0;
    this->duration = 0;
    this->redPin = redPin;
    this->greenPin = greenPin;
    this->bluePin = bluePin;
    this->red = 0;
    this->green = 0;
    this->blue = 0;
    this->RGBIsOn = false;
    ledcAttach(redPin, 12000, 8);
    ledcAttach(bluePin, 12000, 8);
    ledcAttach(greenPin, 12000, 8);
}

/**
 * @brief Constructs an Actuator object.
 */
Actuator::Actuator() {
    this->buzzer_pin = 0;
    this->_buzzerIsOn = false;
    this->frequency = 0;
    this->duration = 0;
    this->redPin = 0;
    this->greenPin = 0;
    this->bluePin = 0;
}
/**
 * @brief Destructor for the Actuator class.
 */
Actuator::~Actuator() {
    // Destructor
    turnOffBuzzer();
    turnOffRGB();
    ledcDetach(redPin);
    ledcDetach(bluePin);
    ledcDetach(greenPin);
}

/**
 * @brief Turns off the buzzer.
 */
void Actuator::turnOffBuzzer(void) {
    noTone(buzzer_pin);
    this->_buzzerIsOn = false;
}

/**
 * @brief Turns on the buzzer with the specified frequency and duration.
 */
void Actuator::turnOnBuzzer(void) {
    tone(buzzer_pin, frequency, duration);
    this->_buzzerIsOn = true;
}

/**
 * @brief Sets the frequency of the buzzer.
 * @param frequency The frequency to set.
 */
void Actuator::setBuzzerFrequency(unsigned int frequency) {
    this->frequency = frequency;
    if(_buzzerIsOn) {
        turnOnBuzzer();
    } else {
        turnOffBuzzer();
    }
}

/**
 * @brief Sets the duration of the buzzer.
 * @param duration The duration to set.
 */
void Actuator::setBuzzerDuration(unsigned int duration = 0) {
    this->duration = duration;
}

/**
 * @brief Checks if the buzzer is currently on.
 * @return True if the buzzer is on, false otherwise.
 */
bool Actuator::buzzerIsOn(void) {
    return this->_buzzerIsOn;
}

/**
 * @brief Turns on the RGB LED with the current color settings.
 */
void Actuator::turnOnRGB() {
    ledcWrite(redPin, red);
    ledcWrite(greenPin, green);
    ledcWrite(bluePin, blue);
    this->RGBIsOn = true;
}

/**
 * @brief Turns off the RGB LED.
 */
void Actuator::turnOffRGB() {
    ledcWrite(redPin, 0);
    ledcWrite(greenPin, 0);
    ledcWrite(bluePin, 0);
    this->RGBIsOn = false;
}

/**
 * @brief Sets the color of the RGB LED.
 * 
 * @param red The intensity of the red color (0-255).
 * @param green The intensity of the green color (0-255).
 * @param blue The intensity of the blue color (0-255).
 */
void Actuator::setRGBColor(uint16_t red, uint16_t green, uint16_t blue) {
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
    if (blue > 255) {
        this->blue = 255;
    } else if (blue < 0) {
        this->blue = 0;
    } else {
        this->blue = blue;
    }
    if (RGBIsOn) {
        turnOnRGB();
    } else {
        turnOffRGB();
    }
}