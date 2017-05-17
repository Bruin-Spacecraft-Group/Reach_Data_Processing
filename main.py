import time
from GPS import GPSInit saveCoor processCoordinates
from readSerial import readFromSerial
from sendTCP import 

GPS.GPSInit()

ser = serial.Serial(
    port='COM4',
    baudrate=9600,
    #I DONT KNOW WHAT THESE MEAN PLEASE CHANGE
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

while ser.isOpen():
	#get data
	dataString = ser.readline()
	#parse string 
	#create array with elements deliminated by spaces
	"""
	contents should be as follows
	data[0] = pressure
	data[1] = temperature
	data[2] = gyroX
	data[3] = gyroY
	data[4] = gyroZ
	data[5] = accelX
	data[6] = accelY
	data[7] = accelZ
	"""
	data = dataString.split(" ")

	


	GPS.processCoordinates(coordinates, timestamp)
