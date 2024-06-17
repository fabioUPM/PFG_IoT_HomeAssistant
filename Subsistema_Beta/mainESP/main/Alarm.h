#ifndef ALARM_H
#define ALARM_H

#include "esp32-hal-timer.h"
#include "esp32-hal-ledc.h"
#include "Actuator.h"

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
     * @brief Activates the Flame Detectionalarm.
     * 
     * This method activates the Flame alarm system.
     */
    void activateFlameAlarm();  // Método para activar la alarma

    /**
     * @brief Deactivates the alarm.
     * 
     * This method deactivates the alarm system.
     */
    void deactivateFlameAlarm();  // Método para desactivar la alarma

    /**
     * @brief Gets the activation state of the alarm.
     * 
     * This method returns the current activation state of the alarm.
     * 
     * @return true if the alarm is activated, false otherwise.
     */
    bool getIsFlameActivated(); // Método para obtener el estado de la alarma

    /**
     * @brief Activates the Motion Detectionalarm.
     * 
     * This method activates the Motion alarm system.
     */
    void activateMotionAlarm();  // Método para activar la alarma

    /**
     * @brief Deactivates the Motion alarm.
     * 
     * This method deactivates the Motion alarm system.
     */
    void deactivateMotionAlarm();  // Método para desactivar la alarma

    /**
     * @brief Gets the activation state of the alarm.
     * 
     * This method returns the current activation state of the alarm.
     * 
     * @return true if the alarm is activated, false otherwise.
     */
    bool getIsMotionActivated(); // Método para obtener el estado de la alarma

    /**
     * @brief Configures the alarm actuator.
     * 
     * This method configures the alarm actuator.
     * 
     * @param actuator The actuator to configure.
     */
    void configureAlarmActuator(Actuator &actuator);  

private:
    bool isFlameActivated; // Flame alarm activation state
    bool isMotionActivated; // Motion alarm activation state
};

#endif