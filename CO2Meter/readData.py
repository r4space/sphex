from dronekit import connect, VehicleMode
import time
import struct, array, time, io, fcntl, sys

I2C_SLAVE=0x0703

ADDR = 0x68

bus=1
fr = io.open("/dev/i2c-"+str(bus), "rb", buffering=0)
fw = io.open("/dev/i2c-"+str(bus), "wb", buffering=0)

# set device address
fcntl.ioctl(fr, I2C_SLAVE, ADDR)
fcntl.ioctl(fw, I2C_SLAVE, ADDR)
time.sleep(1) #StartUp

s = [0x22,0x00,0x08,0x2A]
s2 = bytearray( s )

for i in range(30):
	time.sleep(0.5)
	
#REQUEST
	try:
		fw.write( s2 ) #sending config register bytes
	except IOError,e:
		e = sys.exc_info()

	time.sleep(0.02)
	
#RECEIVE
	try:
		data = fr.read(4) #read 4 bytes
		buf = array.array('B', data)
		if buf[1]!=255:
			print "CO2Vaue: ",(buf[1]*256+buf[2])
			print buf
		else:
			print "bullshit result"
			print buf

	except IOError,e:
		e = sys.exc_info()
		print "10Unexpected error2s: ",e

