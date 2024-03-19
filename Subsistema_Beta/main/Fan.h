#ifndef FAN_H
#define FAN_H
#include "Arduino.h"

/**
 * @brief Enumeration for fan direction.
 */
enum FanDirection {
    CLOCKWISE, /**< Clockwise direction. */
    COUNTER_CLOCKWISE /**< Counter-clockwise direction. */
};

/**
 * @brief Class representing a fan.
 */
class Fan {
private:
    uint8_t pin_enable; /**< Pin number for fan enable. */
    uint8_t pin_dir_cw; /**< Pin number for clockwise direction. */
    uint8_t pin_dir_ccw; /**< Pin number for counter-clockwise direction. */
    uint16_t speed; /**< Fan speed. */
    FanDirection direction; /**< Fan direction. */
    bool fanIsOn; /**< Flag indicating if the fan is turned on. */

public:
    /**
     * @brief Constructor for Fan class.
     * @param pin_enable The pin number for fan enable.
     * @param pin_dir_cw The pin number for clockwise direction.
     * @param pin_dir_ccw The pin number for counter-clockwise direction.
     */
    Fan(uint8_t pin_enable, uint8_t pin_dir_cw, uint8_t pin_dir_ccw);

    /**
     * @brief Destructor for Fan class.
     */
    ~Fan();

    /**
     * @brief Initializes the fan.
     */
    void initializeFan(void);

    /**
     * @brief Turns on the fan.
     */
    void turnOn(void);

    /**
     * @brief Turns off the fan.
     */
    void turnOff(void);

    /**
     * @brief Sets the speed of the fan.
     * @param speed The desired speed of the fan.
     */
    void setSpeed(uint16_t speed);

    /**
     * @brief Sets the direction of the fan.
     * @param direction The desired direction of the fan.
     */
    void setDirection(FanDirection direction);

    /**
     * @brief Checks if the fan is turned on.
     * @return True if the fan is turned on, false otherwise.
     */
    bool isOn(void);

    /**
     * @brief Gets the direction of the fan.
     * @return The direction of the fan.
     */
    FanDirection getDirection(void);

    /**
     * @brief Gets the speed of the fan.
     * @return The speed of the fan.
     */
    uint16_t getSpeed(void);
};

#endif

