import time
import serial
import socket
from gps.GPS import GPSInit, saveCoor, processCoordinates
#from communication.readSerial import readFromSerial
#from communication.sendTCP import initSocket, sendPacket, killSocket
from communication.sendUDP import initSocket, sendPacket, killSocket
from accel import findInertialFrameAccel

#initiate serial port to read from
SERIAL_PORT = 'COM3'
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

GPSInit()
velocity = [0,0,0]
position = [0,0,0]

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
	dt = data[0] - oldtime
	oldtime = data[0]

	acceleration = findInertialFrameAccel(data[6], data[7], data[8], data[3], data[4], data[7], dt)
	
	velocity[0] = velocity[0] + acceleration[0]*dt
	velocity[1] = velocity[1] + acceleration[1]*dt
	velocity[2] = velocity[2] + acceleration[2]*dt

	position[0] = position[0] + velocity[0]*dt
	position[1] = position[1] + velocity[1]*dt
	position[2] = position[2] + velocity[2]*dt

	#processCoordinates(data[0], data[9], data[10], data[11])
	
	#sendPacket(sock, finalData)
	data = BUFFER + data
	sock.sendto(data, (SEND_TO_IP, SEND_TO_PORT))
	#sendPacket(sock, data)
	
killSocket(sock)