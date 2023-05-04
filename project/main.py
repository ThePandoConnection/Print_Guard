import serial
import time
import threading
from threading import Thread

# from Arduino_serial import SerialRead
pause = False

class PrintThread(threading.Thread):
    def __init__(self, f, port, baudrate):
        threading.Thread.__init__(self)
        self.f = f
        self.port = port
        self.baudrate = baudrate

    def run(self):
        print('Starting Print')
        runPrinter(self.f, self.port, self.baudrate)
        print('Print Finished')


def loadGcode(file):
    f = open(file + '.gcode')
    return f


def runPrinter(f, port, baudrate):
    fail = False
    try:
        ser = serial.Serial(port=port, baudrate=baudrate)
    except:
        print('Error opening port, might be incorrect port')
        fail = True
    if not fail:
        if ser.isOpen():
            print(ser.name + " is open")
        else:
            print('An Error occurred with the port, trying again')
            ser.open()
        if ser.isOpen():
            print('Printing')

            ser.write("\r\n\r\n".encode())
            time.sleep(2)
            ser.flushInput()

            for line in f:
                while pause:
                    time.sleep(5)
                    print('paused')
                l = line.strip()  # Strip all EOL characters for streaming
                print('Sending: ' + l)
                ser.write((l + '\n').encode())  # Send g-code block to grbl
                try:
                    print('Received: ' + ser.readline().decode())
                except UnicodeDecodeError:
                    print('Received: ' + ser.readline().decode())
            ser.close()