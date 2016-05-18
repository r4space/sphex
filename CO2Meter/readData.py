#TODO
#from dronekit import connect, VehicleMode
import os
import time
import struct, array, time, io, fcntl, sys

#CONFIGS:
dataDir="/home/pi/DATA_STORE/"
filename="CO2Meter_GPS.csv"
#Make next flight dir
def mkND(dataDir):
	a=os.listdir(dataDir)
	num=len(a)
	ND=dataDir+"Flight"+str(num+1).zfill(3)
	os.makedirs(ND)
	return ND+"/"


#Mavlink Setup
def mavlink_setup():
#TODO
	pass

def readCO2meter(fw):

	#REQUEST
	CMD = bytearray([0x22,0x00,0x08,0x2A])
	try:
		fw.write(CMD) #sending config register bytes
	except IOError as e:
		e = sys.exc_info()

	time.sleep(0.02)

	#RECEIVE
	buf=256
	try:
		data = fr.read(4) #read 4 bytes
		buf = array.array('B', data)
		#Returns the CO2 value in ppm by joining Byte1 and Byte2
		val=(buf[1]*256+buf[2])

	except IOError as e:
		e = sys.exc_info()
		print "10Unexpected error2s: ",e
	return val

#MainLoop
#Delay for StartUp of CO2Meter
#TODO
#time.sleep(60)

#Create Log File
ND=mkND(dataDir)
f = open(ND+filename,"w")
f.write("CO2 (PPM), Latitude, Longitude, Time")

#I2C Setup
print ("CONFIGUREING I2C")
I2C_SLAVE=0x0703
ADDR = 0x68
bus=1
fr = io.open("/dev/i2c-"+str(bus), "rb", buffering=0)
fw = io.open("/dev/i2c-"+str(bus), "wb", buffering=0)
fcntl.ioctl(fr, I2C_SLAVE, ADDR)
fcntl.ioctl(fw, I2C_SLAVE, ADDR)

#Mavlink setup

#Run
for i in range(10):
#while(ARMED):
	print(i)
	ppm = readCO2meter(fw)
	GPS = readPixHawk()
	f.write(str(ppm)+","+"GPS"\n")
	time.sleep(0.5)

f.close()


