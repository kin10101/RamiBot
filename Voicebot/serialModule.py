import serial


# Sends a message to the Arduino
def sendSerialMessage(message):
    ser = serial.Serial('/dev/USB0', 9600, timeout=1)  # Change port when needed
    ser.write(message)
    ser.close()
