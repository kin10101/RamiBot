import serial


# Sends a message to the Arduino
def sendSerialMessage(message):
    try:
        ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)  # Change port when needed
        ser.write(message)
        ser.close()
    except:
        pass
