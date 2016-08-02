#TODO Delete all print statements
from dronekit import connect, VehicleMode
import os
import time
import struct, array, time, io, fcntl, sys

#CONFIGS:
dataDir="/home/pi/DATA_STORE/"
datafile="CO2Meter_GPS.csv"
#datafile="CO2Meter_GPS.jsn"
logfile ="Pi_log.csv"
vehicle = connect('/dev/ttyAMA0', wait_ready=True, baud=57600)
pilotV = vehicle.wait_ready('autopilot_version')


#Make next flight dir
def mkND(dataDir):
	a=os.listdir(dataDir)
	num=len(a)
	ND=dataDir+"Flight"+str(num+1).zfill(3)
	os.makedirs(ND)
	return ND+"/"


def get_position(vehicle):
    lat = vehicle.location.global_frame.lat
    long = vehicle.location.global_frame.lon
    alt = vehicle.location.global_frame.alt
    air_spd = vehicle.airspeed

    mode = str(vehicle.mode)
    mode=mode.split(":")[1]

    gps_stat = str(vehicle.gps_0)
    fix= gps_stat.split(":")[1].split(",")[0].split('=')[1]
    count= gps_stat.split(":")[1].split(",")[1].split('=')[1]



    return [lat,long,alt,air_spd,mode,fix,count]


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

#Create Data and Log Files
ND=mkND(dataDir)
fd = open(ND+datafile,"w")
fl = open(ND+logfile,"w")
fd.write("CO2 (PPM), Latitude, Longitude, Altitude, Air Speed (m/s), Mode, Fixed Sats, Available Sats")

#I2C Setup
print ("CONFIGUREING I2C")
I2C_SLAVE=0x0703
ADDR = 0x68
bus=1
fr = io.open("/dev/i2c-"+str(bus), "rb", buffering=0)
fw = io.open("/dev/i2c-"+str(bus), "wb", buffering=0)
fcntl.ioctl(fr, I2C_SLAVE, ADDR)
fcntl.ioctl(fw, I2C_SLAVE, ADDR)







#Run
#TODO Uncomment
while not vehicle.armed:
	time.sleep(0.5)
	fl.write( "\rWaiting for arming")
	sys.stdout.flush()
	print "\rWaiting for arming"

print "ARMED"
fl.write("\nSystem armed, starting logs")

for i in range(10):
	try:
		time.sleep(0.5)
		ppm = readCO2meter(fw)
		stats = get_position(vehicle)

		fd.write("\n%s,%s,%s,%s,%s,%s,%s,%s" % (ppm,stats[0],stats[1],stats[2],stats[3],stats[4],stats[5],stats[6]))
		print("\n%s,%s,%s,%s,%s,%s,%s,%s" % (ppm,stats[0],stats[1],stats[2],stats[3],stats[4],stats[5],stats[6]))

		print " Battery: %s" % vehicle.battery

	except KeyboardInterrupt:

		e = sys.exc_info()
		fl.write("\n"+e)
		fd.close()
		fl.close()
		vehicle.close()

fl.write("\nSystem unarmed, closing down and saving data")
fd.close()
fl.close()
vehicle.close()
