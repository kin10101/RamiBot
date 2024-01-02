try:
    import RPi.GPIO as GPIO
except RuntimeError:
    import fake_rpigpio.RPi as GPIO

def set_gpio_pin(pin, state):
    # Set mode and pin
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)

    # Set the pin to the specified state
    GPIO.output(pin, state)
