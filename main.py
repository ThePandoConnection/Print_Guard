import serial
import time
import threading


class printThread(threading.Thread):
    def __init__(self, f, ser):
        threading.Thread.__init__(self)
        self.f = f
        self.ser = ser

    def run(self):
        print('Starting Print')
        runPrinter(self.f, self.ser)
        print('Print Finished')


def printerConnect(port='COM3', baudrate=115200):
    ser = serial.Serial(port=port, baudrate=baudrate, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    print(ser.name + " is open")
    return ser


def loadGcode(file):
    f = open(file + '.gcode')
    return f


def runPrinter(f, ser):
    for line in f:
        time.sleep(2)

        ser.write(line.encode('ascii'))

        time.sleep(1)
    return True


if __name__ == "__main__":
    f = loadGcode('test')
    ser = printerConnect()
    thread = printThread(f, ser)
    thread.start()
    print('test')

    ser.close()
