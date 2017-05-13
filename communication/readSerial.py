import serial
import time

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='COM4',
    baudrate=9600,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

ser.isOpen()

print("connected to: " + ser.portstr)

with open('output.txt', 'w+') as output:
    output.write("")
for count in range(10):
    print ("running")
    line = ser.readline()
    print( str(count) + ":" + line )
    output = open('output.txt', 'a+')
    output.write(line + '\n')
    time.sleep(0.1)

ser.close()