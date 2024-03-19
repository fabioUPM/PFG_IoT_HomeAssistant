#ifndef MOTIONSENSOR_H
#define MOTIONSENSOR_H
#include "Arduino.h"
#endif

/**
 * @class MotionSensor
 * @brief Represents a motion sensor.
 */
class MotionSensor {
    
public:
    /**
     * @brief Constructs a MotionSensor object with the specified pin.
     * @param pin_p The pin number to which the motion sensor is connected.
     */
    MotionSensor(uint8_t pin_p);

    /**
     * @brief Destroys the MotionSensor object.
     */
    ~MotionSensor();
    
    /**
     * @brief Checks if motion is currently detected.
     * @return True if motion is detected, false otherwise.
     */
    bool isMotionDetected(void);

    /**
     * @brief Checks if motion has ended.
     * @return True if motion has ended, false otherwise.
     */
    bool isMotionEnded(void);

    /**
     * @brief Enables motion detection.
     */
    void enableMotionDetection(void);

    /**
     * @brief Disables motion detection.
     */
    void disableMotionDetection(void);
};