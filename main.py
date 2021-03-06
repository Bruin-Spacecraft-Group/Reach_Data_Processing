#TODO save data

import time
import serial
import socket
import math
import numpy as np

from gps.GPS import GPSInit, saveCoor, processCoordinates, calcVelGPS
from communication.sendUDP import initSocket, sendPacket, killSocket
from altimeter.altitudeCalculation import altitudeCalc
import accel
#from accel import findInertialFrameAccel

try:
	print "Opening Serial Port..."
	#initiate serial port to read data from
	SERIAL_PORT = 'COM4'
	ser = serial.Serial(
	    port=SERIAL_PORT,
	    baudrate=9600,
	    timeout=3, #give up reading after 3 seconds
	    parity=serial.PARITY_ODD,
	    stopbits=serial.STOPBITS_TWO,
	    bytesize=serial.SEVENBITS
	)
	print "connected to port " + SERIAL_PORT
except:
	print "<==Error connecting to " + SERIAL_PORT + "==>"
	exit()

'''
#initiate socket to push data to raspberry pi
#wlan0 address of pi:
SEND_TO_IP = '192.168.1.12'
#SEND_TO_IP = '10.10.10.193'
SEND_TO_PORT = 5005
try:
	print "Connecting to server..."
	sock = initSocket(SEND_TO_IP, SEND_TO_PORT)
	print "Connected to server at " + SEND_TO_IP + "on Port " + SEND_TO_PORT 
except:
	print "<== Error could not connect to server at " + SEND_TO_IP + "==>" 
	exit()
'''
#Initiate variables
FIRST = True

lat2 = 0
lon2 = 0
GPSInit()
velocity = np.matrix([0,0,0]).T
position = np.matrix([0,0,0]).T

#TODO function for dynamicaly assessing calibration constants
ACCX_CALIB = 0
ACCY_CALIB = 0
ACCZ_CALIB = 0

#set positions of data in incoming csv packet
TIMESTAMP = 0
ACCELX = 1
ACCELY = 2
ACCELZ = 3
GYROX = 4
GYROY = 5
GYROZ = 6
GPSLAT = 7
GPSLON = 8
GPSALT = 9
GPSHOUR = 10
GPSMIN = 11
GPSSEC = 12
#MAGX = 7
#MAGY = 8
#MAGZ = 9
#MAGHEAD = 10
TEMP = 13
PRES = 14
ALTITUDE = 15
BAROTEMP = 16

tots_not_launch = 1
count = 0


#TODO 
while ser.isOpen():
	#get data
	dataString = ser.readline()
	print 'Received: ' + dataString + '/n'
	'''
	LAST YEAR'S ORDER LEFT FOR REFERENCE, IS NOT USED
	parse string 
	create array with elements deliminated by spaces
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
	data[9] = gps Time
	data[10] = lon
	data[11] = lat
	data[12] = gpsAlt
	data[13] = speed
	data[14] = course
	'''
	data = dataString.split(",")

	if(count<6):
		print 'Calibrating...'
		ACCX_CALIB += data[ACCELX]
		ACCY_CALIB += data[ACCELY]
		ACCZ_CALIB += data[ACCELZ]
		count+=1
	else:
		if(count==6):
			ACCX_CALIB = ACCX_CALIB/6
			ACCY_CALIB = ACCY_CALIB/6
			ACCZ_CALIB = ACCZ_CALIB/6
			count+=1
			print 'Calibration: ' + str(ACCX_CALIB) + ', ' + str(ACCY_CALIB) + ', ' + str(ACCZ_CALIB)
	
		#had problems with only reading in a few data 
		if (len(data) < 6):
			print "not enough data"
			continue
	
		#establish spacecraft time
		if(FIRST == True):
			FIRST = False
			oldtime = float(data[TIMESTAMP])
			#since dt cannot be established, skip
			#TODO save first data packet's raw data
			continue
	
		#DO STUFF WITH DATA
		#convert from string type
		for i in range(len(data)-1):
			data[i] = float(data[i])
		'''
		if (len(data) < 12):
			gpsRecieved = False
			print "no coordinates"
		else: 
			gpsRecieved = True
		'''
		#establish time elapsed
		dt = (data[TIMESTAMP] - oldtime)/1000 #convert ms to s
		oldtime = data[TIMESTAMP]
	
		#append altitude calculated from pressure
		#data.append(altitudeCalc(data[1]))
	
		#process acceleration
		acceleration = accel.findInertialFrameAccel(data[ACCELX], data[ACCELY], data[ACCELZ], data[GYROX], data[GYROY], data[GYROZ], dt, [ACCX_CALIB, ACCY_CALIB, ACCZ_CALIB])
		
		#integrate to find velocity
		velocity = velocity+acceleration*dt
	
		#integrate to find position
		position = position + velocity*dt
	
		#append inertial frame acceleration velocity 
		#and position data to transmitted data
		data.append(acceleration.item(0))
		data.append(acceleration.item(1))
		data.append(acceleration.item(2))
		data.append(velocity.item(0)) 
		data.append(velocity.item(1))
		data.append(velocity.item(2))
		data.append(position.item(0))
		data.append(position.item(1))
		data.append(position.item(2))
	
		
		#Process GPS coordinates
		if data[GPSSEC] != oldGPSTime:
			longitude = data[GPSLON]
			latitude = data[GPSLAT]
			latDeg = math.floor(latitude)
			lonDeg = math.floor(longitude)
	
			latMin = float(latitude) - latDeg
			lonMin = float(longitude) - lonDeg
		    
			lat = float(latDeg)+float(latMin)/60
		 	lon = float(lonDeg)-float(lonMin)/60
		    
			saveCoor(lon, lat, data[GPSALT])
		    
		    #speed calculation from gps data:
			#push the last new value to the old and then set the new value 
			lat1 = lat2
		 	lat2 = lat
			lon1 = lon2
			lon2 = lon

			dt = data[GPSSEC] - oldGPSTime
			if dt < 0:
				dt = data[GPSSEC] + 60 - oldGPSTime
			#specific to GPS because GPS not expected as often
			oldGPSTime = data[GPSSEC]
			#calcVelGPS(lat1, lon1, lat2, lon2, dt)
	
			print "sending:"
		
		
		#append absolute time
		data.append(time.time())
		
		finalData = ""
		for i in range(len(data)-1):
			#print data[i]
			finalData = finalData + str(data[i]) + ", "
			'''
			finalData contents should be as follows, 
			as a string separated by commas:
			relative spacecraft time 
			raw accelX
			raw accelY
			raw accelZ
			gyroX
			gyroY
			gyroZ
			magX
			magY
			magZ
			magHead
			temp(C)
			altitude
			inertial accelX
			inertial accelY
			inertial accelZ
			velX
			velY
			velZ
			posX
			posY
			posZ
			absTime
			'''
		print finalData
		#sock.sendto(finalData, (SEND_TO_IP, SEND_TO_PORT))
#killSocket(sock)
