#ifndef ALARM_H
#define ALARM_H

#include "RGB.h"
#include "Buzzer.h"
#include "TimerOne.h"

/**
 * @brief The Alarm class represents an alarm system.
 * 
 * This class provides methods to activate and deactivate the alarm, configure the alarm LEDs and buzzer,
 * and get the current state of the alarm.
 */
class Alarm {
public:
    /**
     * @brief Constructs an Alarm object.
     */
    Alarm();  // Constructor

    /**
     * @brief Destroys the Alarm object.
     */
    ~Alarm();  // Destructor

    /**
     * @brief Activates the alarm.
     * 
     * This method activates the alarm system.
     */
    void activateAlarm();  // Método para activar la alarma

    /**
     * @brief Deactivates the alarm.
     * 
     * This method deactivates the alarm system.
     */
    void deactivateAlarm();  // Método para desactivar la alarma

    /**
     * @brief Configures the LEDs of the alarm.
     * 
     * This method configures the LEDs of the alarm system.
     * 
     * @param RGB The RGBLed object representing the LEDs of the alarm.
     */
    void configureAlarmLEDs(RGBLed &RGB);  // Método para configurar los LEDs de la alarma

    /**
     * @brief Configures the buzzer of the alarm.
     * 
     * This method configures the buzzer of the alarm system.
     * 
     * @param buzzer The Buzzer object representing the buzzer of the alarm.
     */
    void configureAlarmBuzzer(Buzzer &buzzer);  // Método para configurar el buzzer de la alarma

    /**
     * @brief Gets the activation state of the alarm.
     * 
     * This method returns the current activation state of the alarm.
     * 
     * @return true if the alarm is activated, false otherwise.
     */
    bool getIsActivated(); // Método para obtener el estado de la alarma

private:
    bool isActivated;  // Indicador de si la alarma está activada o no
};

#endif