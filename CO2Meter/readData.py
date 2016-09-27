#TODO Delete all print statements
#TODO add proper logging

from dronekit import connect, Vehicle
import argparse
import sys
from VV.vermont_vehicle import vermont_vehicle #Customised vehicle class
from VV import use_DK as uDk
#Setup configurations:
#dataDir="/home/jwyngaard/work/DRONES/vermont.git/TESTDATADIR/"
dataDir="/home/pi/DATA_STORE/"

datafile="CO2Meter_GPS.csv"
#datafile="CO2Meter_GPS.jsn"

logfile ="log.log"


#Set up option parsing
parser = argparse.ArgumentParser(description='Capture Iris and sensor flight data ')
parser.add_argument("-s", "--sitl", help="Use the sitl simulator instead of connecting to the Pixhawk, also disables CO2 meter reading", action="store_true")
args = parser.parse_args()

while (1):
	#Create Data and Log Files
	ND=uDk.mk_ND(dataDir)
	fd = open(ND+datafile,"w")
	fl = open(ND+logfile,"w")
	fd.write("CO2 (PPM), Latitude, Longitude, Altitude, Air Speed (m/s), Mode, Fixed Satellites, Available Satellites,voltage,current,level,id")
	fl.write("Created log file")

	#If simulator specified, start SITL and run vermont_vehicle
	if args.sitl:
		vv,sitl = uDk.start_sitl(vermont_vehicle)
	#############################
	#    import dronekit_sitl
	#    print "HERE1"
	#    sitl = dronekit_sitl.start_default()
	#    print "HERE2"
	#    connection_string = sitl.connection_string()
	#    print('Connecting to vehicle in sitl')
	#    vv = connect(connection_string, wait_ready=True, vehicle_class=vermont_vehicle)

	#############################
		outcome=uDk.runSITL(vv,fd,fl)
		if not outcome:
			sitl.stop()
	#    vehicle.add_attribute_listener('scaled_pressure', raw_imu_callback)
	#     time.sleep(3)
	#     vehicle.remove_message_listener

	# Else Connect to the Vehicle
	else:
		fl.write("\nConnecting to pilot in Iris")
		sys.stdout.flush()
		print ('Connecting to pilot in Iris')
		vv = connect('/dev/ttyAMA0', wait_ready=True, vehicle_class=vermont_vehicle,baud=57600)
		pilotV = vv.wait_ready('autopilot_version')
		outcome=uDk.runREAL(vv,fd,fl)

	if not outcome:
		fl.write("\nSystem unarmed, closing down and saving data")
		fd.close()
		fl.close()
		vv.close()

