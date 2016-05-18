#TODO
#from dronekit import connect, VehicleMode
import time
import struct, array, time, io, fcntl, sys
#CONFIGS
filename="/home/jwyngaard/Desktop/CO2Readings.csv"

#I2C Setup
def i2c_config():
    print ("CONFIGUREING I2C")
    I2C_SLAVE=0x0703
    ADDR = 0x68
    bus=1
    fr = io.open("/dev/i2c-"+str(bus), "rb", buffering=0)
    fw = io.open("/dev/i2c-"+str(bus), "wb", buffering=0)
    fcntl.ioctl(fr, I2C_SLAVE, ADDR)
    fcntl.ioctl(fw, I2C_SLAVE, ADDR)
    s = [0x22,0x00,0x08,0x2A]
    return bytearray( s )

#Mavlink Setup
def mavlink_setup():
#TODO
    pass

def readCO2meter(CMD):

    #REQUEST
	try:
		fw.write( CMD ) #sending config register bytes
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
    return(buf)

#MainLoop
#Delay for StartUp of CO2Meter
#TODO
#time.sleep(60)
f = open(filename,"w")
CMD = i2c_config()

for i in range(10):
#while(ARMED):
    print(i)
    value = readCO2meter(CMD)
    f.write(str(value)+"/n")
    time.sleep(0.5)

f.close()


