import serial
import time


def printerConnect(port='COM3', baudrate=115200):
    ser = serial.Serial(port=port, baudrate=baudrate, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    print(ser.name + " is open")
    return ser


def loadGcode(file):
    f = open(file + '.gcode')
    return f


def runPrinter(f):
    return 0


if __name__ == "__main__":
    ser = printerConnect()
    time.sleep(2)

    ser.write(('G28\n').encode('ascii'))

    time.sleep(1)

    ser.close()
