import serial

ser = serial.Serial('COM4', 9800, timeout=1)
if ser.isOpen():
    print('Connection to Arduino Successful')
while 1:
    ser.readline().decode("utf-8")
