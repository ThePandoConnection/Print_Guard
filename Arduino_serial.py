import serial


def SerialRead(port, output):
    ser = serial.Serial(port, 9800, timeout=1)

    if ser.isOpen():
        print('Connection to Arduino Successful')
        output.append(ser.readline().decode("utf-8"))

