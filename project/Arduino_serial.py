import serial


def SerialRead(port):
    ser = serial.Serial(port, 9600, timeout=None)

    if ser.isOpen():
        ser.readline()
        output = ser.readline().decode("utf-8")
        ser.close()
    return output


def SerialWrite(port):
    success = False
    ser = serial.Serial(port, 9600, timeout=None)

    if ser.isOpen():
        ser.readline()
        ser.write(10)
        ser.close()
        success = True
    return success

