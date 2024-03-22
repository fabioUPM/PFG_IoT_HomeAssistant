/**
 * @file Alarm.cpp
 * @brief Implementation of the Alarm class.
 * @author Fabio Antonio Valente
 */
#include "Alarm.h"

RGBLed _RGB(0, 0, 0);  // Instancia de la clase RGBLed
Buzzer _buzzer(0);  // Instancia de la clase Buzzer

static bool changeColor = false;  // Indicador de cambio de color

static void blinkLEDsBuzzer();  // Prototipo de la función blinkLEDs

/**
 * @brief Constructor for the Alarm class.
 * 
 * This constructor is responsible for initializing the Alarm object.
 * It sets the isActivated flag to false.
 */
Alarm::Alarm() {
    isActivated = false;
}

/**
 * @brief Destructor for the Alarm class.
 * 
 * This destructor is responsible for cleaning up resources used by the Alarm object.
 * It detaches the interrupt from Timer1, stops Timer1, turns off the RGB LED, and turns off the buzzer.
 */
Alarm::~Alarm() {
    // Destructor
    Timer1.detachInterrupt();
    Timer1.stop();
    _RGB.turnOff();
    _buzzer.turnOff();
}

/**
 * @brief Activates the alarm.
 * 
 * This function activates the alarm by setting the isActivated flag to true.
 * It initializes Timer1 with a period of 1 second and attaches the blinkLEDsBuzzer function to the interrupt.
 */
void Alarm::activateAlarm() {
    isActivated = true;
    Timer1.initialize(100000);  // Inicializa el temporizador a 1 segundo
    Timer1.attachInterrupt(blinkLEDsBuzzer);  // Asocia la interrupción a la función blinkLEDs
}

/**
 * @brief Deactivates the alarm.
 * 
 * This function deactivates the alarm by setting the isActivated flag to false.
 * It detaches the interrupt from Timer1, stops Timer1, turns off the RGB LED, and turns off the buzzer.
 */
void Alarm::deactivateAlarm() {
    isActivated = false;
    Timer1.detachInterrupt();  // Desasocia la interrupción de la función blinkLEDs
    Timer1.stop();  // Detiene el temporizador
    _RGB.turnOff();  // Apaga los LEDs
    _buzzer.turnOff();  // Apaga el buzzer
}

/**
 * @brief Configures the RGB LED for the alarm.
 * 
 * This function configures the RGB LED used for the alarm by assigning it to the _RGB member variable.
 * 
 * @param RGB The RGBLed object to be used for the alarm.
 */
void Alarm::configureAlarmLEDs(RGBLed &RGB) {
    _RGB = RGB;
}

/**
 * @brief Configures the buzzer for the alarm.
 * 
 * This function configures the buzzer used for the alarm by assigning it to the _buzzer member variable.
 * 
 * @param buzzer The Buzzer object to be used for the alarm.
 */
void Alarm::configureAlarmBuzzer(Buzzer &buzzer) {
    _buzzer = buzzer;
}

/**
 * @brief Gets the activation status of the alarm.
 * 
 * This function returns the current activation status of the alarm.
 * 
 * @return True if the alarm is activated, false otherwise.
 */
bool Alarm::getIsActivated() {
    return isActivated;
}

/**
 * @brief Blinks the LEDs and sounds the buzzer.
 * 
 * This function is called by the Timer1 interrupt and is responsible for blinking the LEDs and sounding the buzzer.
 * It alternates between two colors and frequencies based on the changeColor flag.
 */
void blinkLEDsBuzzer() {
    _RGB.turnOn();
    _buzzer.turnOn();
    if(changeColor) {
        _buzzer.setFrequency(1000);
        _RGB.setColor(255, 0, 0);
        changeColor = false;
    } else {
        _buzzer.setFrequency(700);
        _RGB.setColor(0, 0, 255);
        changeColor = true;
    }
}