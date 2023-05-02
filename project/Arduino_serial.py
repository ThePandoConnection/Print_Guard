import serial


def SerialRead(port, output):
    ser = serial.Serial(port, 9600, timeout=None)

    while ser.isOpen():
        print('Connection to Arduino Successful')
        ser.readline()
        return ser.readline().decode("utf-8")
        output.append(ser.readline().decode("utf-8"))
        ser.close()

