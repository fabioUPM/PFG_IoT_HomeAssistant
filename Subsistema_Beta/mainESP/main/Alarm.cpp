#include "esp32-hal-timer.h"
/**
 * @file Alarm.cpp
 * @brief Implementation of the Alarm class.
 * @author Fabio Antonio Valente
 */
#include "Alarm.h"

Actuator _act;  // Actuator object
hw_timer_t * alarmTimer = NULL;

static bool changeColor = false;  // change color flag
static bool changeTone = false;  // change tone flag


/**
 * @brief Blinks the LEDs and the buzzer.
 * 
 * This function is called by the alarmTimer interrupt and is responsible for blinking the LEDs and the buzzer.
 * It alternates between two colors based on the changeColor flag.
 */
static void IRAM_ATTR blinkLEDsBuzzer() {

    if(changeColor) {
        _act.setBuzzerFrequency(1000);
        _act.setRGBColor(255, 0, 0);
        changeColor = false;
    } else {
        _act.setBuzzerFrequency(500);
        _act.setRGBColor(0, 0, 255);
        changeColor = true;
    }
}

/**
 * @brief Changes the tone of the buzzer.
 * 
 * This function is called by the alarmTimer interrupt and is responsible for changing the tone of the buzzer.
 * It alternates between two frequencies based on the changeTone flag.
 */
static void IRAM_ATTR changeBuzzerTone(){
      _act.turnOnBuzzer();
    if(changeTone){
        _act.setBuzzerFrequency(1000);
        changeTone = false;
    } else {
        _act.setBuzzerFrequency(500);
        changeTone = true;
    }
}

/**
 * @brief Constructor for the Alarm class.
 * 
 * This constructor is responsible for initializing the Alarm object.
 * It sets the isActivated flag to false.
 */
Alarm::Alarm() {
    isFlameActivated = false;
    isMotionActivated = false;
}

/**
 * @brief Destructor for the Alarm class.
 * 
 * This destructor is responsible for cleaning up resources used by the Alarm object.
 * It detaches the interrupt from alarmTimer, stops alarmTimer, turns off the RGB LED, and turns off the buzzer.
 */
Alarm::~Alarm() {
    // Destructor
    timerDetachInterrupt(alarmTimer);
    timerEnd(alarmTimer);
    _act.turnOffRGB();
    _act.turnOffBuzzer();
}

/**
 * @brief Activates the Flame alarm.
 * 
 * This function activates the Flame alarm by setting the flameIsActivated flag to true.
 * It initializes alarmTimer with a period of 1 second and attaches the blinkLEDsBuzzer function to the interrupt.
 */
void Alarm::activateFlameAlarm() {
    if(getIsMotionActivated()){
        deactivateMotionAlarm();
    }
    alarmTimer = timerBegin(1000000);
    timerAttachInterrupt(alarmTimer, &blinkLEDsBuzzer);
    timerAlarm(alarmTimer, 250000, true, 0);
    isFlameActivated = true;
    _act.setRGBColor(255, 0, 0);
    _act.setBuzzerFrequency(1000);
    _act.turnOnRGB();
    _act.turnOnBuzzer();
    changeColor = false;
}

/**
 * @brief Deactivates the Flame alarm.
 * 
 * This function deactivates the Flame alarm by setting the flameIsActivated flag to false.
 * It detaches the interrupt from alarmTimer, stops alarmTimer, turns off the RGB LED, and turns off the buzzer.
 */
void Alarm::deactivateFlameAlarm() {
    if(getIsFlameActivated()){
        isFlameActivated = false;
        timerDetachInterrupt(alarmTimer);
        timerEnd(alarmTimer);
        alarmTimer = NULL;
        _act.turnOffRGB();  // turn off the RGB LED
        _act.turnOffBuzzer();  // turn off the buzzer
    }
}

/**
 * @brief Activates the Motion alarm.
 * 
 * This function activates the MOtion alarm by setting the motionIsActivated flag to true.
 * It initializes alarmTimer with a period of 1 second and attaches the changeBuzzerTone function to the interrupt.
 */
void Alarm::activateMotionAlarm() {
    if(!getIsFlameActivated()){
        isMotionActivated = true;
        alarmTimer = timerBegin(1000000);
        timerAttachInterrupt(alarmTimer, &changeBuzzerTone);
        timerAlarm(alarmTimer, 250000, true, 0);
        _act.setBuzzerFrequency(1000);
        _act.turnOnBuzzer();
        changeTone = false;
    }
}

/**
 * @brief Deactivates the Motion alarm.
 * 
 * This function deactivates the Motion alarm by setting the motionIsActivated flag to false.
 * It detaches the interrupt from alarmTimer, stops alarmTimer, and turns off the buzzer.
 */
void Alarm::deactivateMotionAlarm() {
    if(getIsMotionActivated() && !getIsFlameActivated()){
        isMotionActivated = false;
        timerDetachInterrupt(alarmTimer);
        timerEnd(alarmTimer);
        alarmTimer = NULL;
        _act.turnOffBuzzer();  // turn off the buzzer
    }
}

/**
 * @brief Configures the alarm actuator.
 * 
 * This function configures the alarm actuator by setting the _act member variable to the actuator parameter.
 * 
 * @param actuator The actuator to configure.
 */
void Alarm::configureAlarmActuator(Actuator &actuator) {
    _act = actuator;
}

/**
 * @brief Gets the activation status of the Flame alarm.
 * 
 * This function returns the current activation status of the Flame alarm.
 * 
 * @return True if the Flame alarm is activated, false otherwise.
 */
bool Alarm::getIsFlameActivated() {
    return isFlameActivated;
}

/**
 * @brief Gets the activation status of the Motion alarm.
 * 
 * This function returns the current activation status of the Motion alarm.
 * 
 * @return True if the Motion alarm is activated, false otherwise.
 */
bool Alarm::getIsMotionActivated() {
    return isMotionActivated;
}
