import serial
import time


def sendSerialMessage(command):
    serial.write(command.encode('utf-8'))

'''
try:
    ser = serial.Serial("/dev/ttyACM0", 9600, timeout=1)

    while True:
        sendSerialMessage(input("input: S"))

        break

    ser.close()


except serial.SerialException as e:
    print(f"An error occurred: {e}")
'''