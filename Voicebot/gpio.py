# need sudo to run this script
import RPi.GPIO as GPIO
import time

def set_gpio_pin(pin, state):
    # Set mode and pin
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)

    # Set the pin to the specified state
    GPIO.output(pin, state)

# Usage:
# Set pin 17 high
set_gpio_pin(17, GPIO.HIGH)
time.sleep(1)

# Set pin 17 low
set_gpio_pin(17, GPIO.LOW)
time.sleep(1)

# Clean up GPIO on exit
GPIO.cleanup()