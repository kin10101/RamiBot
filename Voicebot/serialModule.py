import serial
import time


def sendSerialMessage(command):
    serialInst.write(command.encode('utf-8'))


try:
    serialInst = serial.Serial("/dev/ttyACM0", 115200, timeout=1)

    while True:
        sendSerialMessage(input("input: S"))
        serialInst.flushInput()


except serial.SerialException as e:
    print(f"An error occurred: {e}")
finally:
    serialInst.close()
