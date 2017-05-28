import time
import serial
from gps.GPS import GPSInit, saveCoor, processCoordinates
#from communication.readSerial import readFromSerial
#from communication.sendTCP import initSocket, sendPacket, killSocket
from communication.sendUDP import initSocket, sendPacket, killSocket

GPSInit()

#initiate serial port to read from
SERIAL_PORT = 'COM6'
ser = serial.Serial(
    port=SERIAL_PORT,
    baudrate=9600,
    #I DONT KNOW WHAT THESE MEAN PLEASE CHANGE
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

#initiate socket to push data to raspberry pi
#wlan0 address of pi:
SEND_TO_IP = '192.168.56.101'
SEND_TO_PORT = 5005
try:
	sock = initSocket(SEND_TO_IP, SEND_TO_PORT)
except:
	print "could not connect to rockets server"

while ser.isOpen():
	#get data
	dataString = ser.readline()
	#parse string 
	#create array with elements deliminated by spaces
	"""
	contents should be as follows
	data[0] = timestamp
	data[1] = pressure
	data[2] = temperature
	data[3] = gyroX
	data[4] = gyroY
	data[5] = gyroZ
	data[6] = accelX
	data[7] = accelY
	data[8] = accelZ
	data[9] = lon
	data[10] = lat
	data[11] = gpsAlt
	"""
	data = dataString.split(",")

	#DO STUFF WITH DATA
	
	#processCoordinates(data[0], data[9], data[10], data[11])
	
	#sendPacket(sock, finalData)
	sendPacket(sock, data)
	
killSocket(sock)