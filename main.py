import time
from GPS import GPSInit saveCoor processCoordinates
from serial import readFromSerial
from sendTCP import 

GPS.GPSInit()

while serial:
	data = serial.readFromSerial()
	#parse string
	GPS.processCoordinates(coordinates, timestamp)
