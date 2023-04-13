import serial
import time

ser = serial.Serial(port = "COM3", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

#f = open("demofile.gcode", "r")
#print(f.read())

time.sleep(2)

ser.write(str.encode('M106 S200'))

time.sleep(1)

ser.close()