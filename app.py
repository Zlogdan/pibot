import serial

# change ACM number as found from ls /dev/tty/ACM*
ser = serial.Serial("/dev/ttyACM0", 9600)
ser.baudrate = 9600


while(True):
    data = input()
    bdata = str.encode(data) + b'\n'
    # print(bdata)
    ser.write(bdata)

    read_ser = ser.readline()
    print(read_ser.decode())
