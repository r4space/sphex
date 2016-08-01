#TODO Delete all print statements
#TODO add proper logging

from dronekit import connect, Vehicle
import argparse

from VV import vermont_vehicle as vv #Customised vehicle class
from VV import organise

#Setup configurations:
dataDir="/home/jwyngaard/work/DRONES/vermont.git/TESTDATADIR/"
#dataDir="/home/pi/DATA_STORE/"

datafile="CO2Meter_GPS.csv"
#datafile="CO2Meter_GPS.jsn"

logfile ="Pi_log.csv"


#Set up option parsing
parser = argparse.ArgumentParser(description='Capture Iris and sensor flight data ')
parser.add_argument("-s", "--sitl", help="Use the sitl simulator instead of connecting to the Pixhawk, also disables CO2 meter reading", action="store_true")
args = parser.parse_args()


#Create Data and Log Files
ND=organise.mk_ND(dataDir)
fd = open(ND+datafile,"w")
fl = open(ND+logfile,"w")
fd.write("CO2 (PPM), Latitude, Longitude, Altitude, Air Speed (m/s), Mode, Fixed Satellites, Available Satellites")


#If simulator specified, start SITL
if args.sitl:
    DK.start_sitl(vv)
    runSITL(vv)
    sitl.stop()

#Connect to a vehicle (sitl or real)
#    vehicle.add_attribute_listener('scaled_pressure', raw_imu_callback)
#     time.sleep(3)
#     vehicle.remove_message_listener

# Else Connect to the Vehicle
else:
    connection_string='/dev/ttyAMA0'
    print ('Connecting to pilot in Iris')
    vehicle = connect(connection_string, wait_ready=True, vehicle_class=MyVehicle,baud=57600)
    #vehicle = connect('/dev/ttyAMA0', wait_ready=True, baud=57600)
    pilotV = vehicle.wait_ready('autopilot_version')
    
    run(vehicle,sim=False)


fl.write("\nSystem unarmed, closing down and saving data")
fd.close()
fl.close()
vehicle.close()

