import serial


def SerialRead(port):
    ser = serial.Serial(port, 9600, timeout=None)

    if ser.isOpen():
        ser.readline()
        output = ser.readline().decode("utf-8")
        ser.close()
    return output

