#TODO Delete all print statements
#TODO add proper logging

from dronekit import connect, Vehicle
import argparse
import sys
from VV.vermont_vehicle import vermont_vehicle #Customised vehicle class
from VV import use_DK as uDk
#Setup configurations:
dataDir="/home/pi/FLIGHTDATA/"

datafile="CO2Meter_GPS.csv"
#datafile="CO2Meter_GPS.jsn"

logfile ="log.log"

while (1):
	#Create Data and Log Files
	ND=uDk.mk_ND(dataDir)
	fd = open(ND+datafile,"w")
	fl = open(ND+logfile,"w")
	fd.write("CO2 (PPM), Latitude, Longitude, Altitude, Air Speed (m/s), Mode, Fixed Satellites, Available Satellites,voltage,current,level,id")
	fl.write("Created log file")
	fl.write("\nConnecting to pilot in Iris")
	sys.stdout.flush()
	print ('Connecting to pilot in Iris')
    vv = connect('/dev/serial0', wait_ready=True, vehicle_class=vermont_vehicle,baud=57600)
	pilotV = vv.wait_ready('autopilot_version')
	outcome=uDk.runREAL(vv,fd,fl)

	if not outcome:
		fl.write("\nSystem unarmed, closing down and saving data")
		fd.close()
		fl.close()
		vv.close()

