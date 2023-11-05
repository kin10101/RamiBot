import serial.tools.list_ports
import time

ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()
portList = []

for onePort in ports:
    portList.append(str(onePort))
    print(str(onePort))

serialInst.baudrate = 9600
serialInst.port = "/dev/ttyUSB0"
serialInst.open()

def sendSerialMessage(command):
    serialInst.write(command.encode('utf-8'))

#while True:
#    sendSerialMessage('1')
#   time.sleep(1)
#   sendSerialMessage('2')
#   time.sleep(1)
