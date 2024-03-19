/**
 * @file Fan.cpp
 * @brief Implementation file for the Fan class.
 * @author Fabio Antonio Valente
 */

#include "Fan.h"

/**
 * @brief Constructor for the Fan class.
 * @param pin_enable The pin number for the enable pin of the fan.
 * @param pin_dir_cw The pin number for the clockwise direction pin of the fan.
 * @param pin_dir_ccw The pin number for the counter-clockwise direction pin of the fan.
 */
Fan::Fan(uint8_t pin_enable, uint8_t pin_dir_cw, uint8_t pin_dir_ccw) {
    // Constructor
    this->pin_enable = pin_enable;
    this->pin_dir_cw = pin_dir_cw;
    this->pin_dir_ccw = pin_dir_ccw;
    this->speed = 0;
    this->direction = CLOCKWISE;
    this->fanIsOn = false;
}

/**
 * @brief Destructor for the Fan class.
 * Turns off the fan and sets the direction and speed to 0.
 */
Fan::~Fan() {
    // Destructor
    digitalWrite(pin_enable, LOW);
    analogWrite(pin_dir_cw, 0);
    analogWrite(pin_dir_ccw, 0);
}

/**
 * @brief Initializes the fan by setting the pin modes and turning it off.
 */
void Fan::initializeFan() {
    // Lógica para inicializar el ventilador
    pinMode(pin_enable, OUTPUT);
    pinMode(pin_dir_cw, OUTPUT);
    pinMode(pin_dir_ccw, OUTPUT);

    // Inicializar el ventilador apagado
    turnOff();
    setSpeed(0);
}

/**
 * @brief Turns on the fan by setting the enable pin to HIGH.
 */
void Fan::turnOn() {
    // Lógica para encender el ventilador
    digitalWrite(pin_enable, HIGH);
    this->fanIsOn = true;
}

/**
 * @brief Turns off the fan by setting the enable pin to LOW.
 */
void Fan::turnOff() {
    // Lógica para apagar el ventilador
    digitalWrite(pin_enable, LOW);
    this->fanIsOn = false;
}

/**
 * @brief Sets the speed of the fan.
 * @param speed The desired speed of the fan (0-255).
 */
void Fan::setSpeed(uint16_t speed) {
    // Lógica para establecer la velocidad del ventilador
    this->speed = speed > 255 ? 255 : speed;
    if(this->direction == CLOCKWISE) {
        analogWrite(pin_dir_ccw, 0);
        analogWrite(pin_dir_cw, this->speed);
    } else {
        analogWrite(pin_dir_cw, 0);
        analogWrite(pin_dir_ccw, this->speed);
    }
}

/**
 * @brief Sets the direction of the fan.
 * @param direction The desired direction of the fan (CLOCKWISE or COUNTER_CLOCKWISE).
 */
void Fan::setDirection(FanDirection direction) {
    // Lógica para establecer la dirección del ventilador
    this->direction = direction;
    if(this->direction == CLOCKWISE) {
        analogWrite(pin_dir_ccw, 0);
        analogWrite(pin_dir_cw, this->speed);
    } else {
        analogWrite(pin_dir_cw, 0);
        analogWrite(pin_dir_ccw, this->speed);
    }
}

/**
 * @brief Gets the current speed of the fan.
 * @return The current speed of the fan.
 */
uint16_t Fan::getSpeed() {
    // Lógica para obtener la velocidad actual del ventilador
    return this->speed;
}

/**
 * @brief Gets the current direction of the fan.
 * @return The current direction of the fan.
 */
FanDirection Fan::getDirection() {
    // Lógica para obtener la dirección actual del ventilador
    return this->direction;
}

/**
 * @brief Checks if the fan is turned on.
 * @return True if the fan is turned on, false otherwise.
 */
bool Fan::isOn() {
    // Lógica para saber si el ventilador está encendido
    return this->fanIsOn;
}