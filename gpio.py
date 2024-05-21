import fake_rpigpio.RPi

try:
    import RPi.GPIO as GPIO
except (RuntimeError, ModuleNotFoundError):
    from fake_rpigpio.RPi import GPIO
def set_gpio_pin(pin, state):
    # Set mode and pin
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    # Set the pin to the specified state
    GPIO.output(pin, state)
    print('set gpio pin '+ str(pin), 'to'+ str(state))

def read_gpio_pin(pin):
    # Set mode and pin
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.IN)
    # Read the state of the pin
    #state = GPIO.input(pin)
    state = 0
    #print('Read state of GPIO pin', pin, ':', state)
    return state

'''
int = read_gpio_pin(7)
if int != 1:
    pass
    else:
'''



'''
set_gpio_pin(4, GPIO.HIGH)
time.sleep(5)
GPIO.cleanup()
'''