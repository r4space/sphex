""" Shared tool functions for interacting with the vehicle"""
import os
import sys
import time
import dronekit_sitl
from dronekit import connect

import co2meter as CO2

def get_stats(aVehicle):
    """Return vehicle attributes in a list"""
    lat = aVehicle.location.global_frame.lat
    long = aVehicle.location.global_frame.lon
    alt = aVehicle.location.global_frame.alt

    air_spd = aVehicle.airspeed
    mode = str(aVehicle.mode)
    mode=mode.split(":")[1]
    gps_stat = str(aVehicle.gps_0)
    fix = gps_stat.split(":")[1].split(",")[0].split('=')[1]
    count = gps_stat.split(":")[1].split(",")[1].split('=')[1]

    bat_stats = str(aVehicle.battery).split(",")
    voltage = (bat_stats[0].split("="))[-1]
    current = bat_stats[1].split("=")[-1]
    level = bat_stats[2].split("=")[-1]

    id = time.time()
    return [lat,long,alt,air_spd,mode,fix,count,voltage,current,level,id]

# Add observer for the custom attribute
def special_attribute_callback(self, attr_name, value):
    # attr_name == 'raw_imu'
    # value == vehicle.raw_imu
    print (value)

def start_sitl(aVehicle):
    """Start simulator and return connected vehicle"""
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()
    print ('Connecting to vehicle in sitl')
    this_v = connect(connection_string, wait_ready=True, vehicle_class=aVehicle)
    return this_v, sitl


#Make next flight dir
def mk_ND(new_dir):
    """Make a new directory
    """
    try:
        a=os.listdir(new_dir)
        num=len(a)
        ND=new_dir+"Flight"+str(num+1).zfill(3)
        os.makedirs(ND)
    except OSError:
        pass

    return ND+"/"

def runREAL(vehicle,datafile,logfile):
    # Configure I2C if not a simulation
    fr, fw = CO2.configI2C()
    logfile.write("Entered RunReal, connecting to iris"")
    sys.stdout.flush()

    while not vehicle.armed:
        time.sleep(0.5)
        logfile.write("\nWaiting for arming")
        sys.stdout.flush()
        print "\nWaiting for arming"

    print "ARMED"
    logfile.write("\nSystem armed, starting logs")
    sys.stdout.flush()

    # for i in range(10):
    while vehicle.armed:
        try:
            time.sleep(0.5)
            stats = get_stats(vehicle)

            ppm = CO2.readCO2meter(fr, fw)
            me
            datafile.write("\n%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (
            ppm, stats[0], stats[1], stats[2], stats[3], stats[4], stats[5], stats[6],stats[7],stats[8],stats[9],stats[10]))
            print("\n%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (
            ppm, stats[0], stats[1], stats[2], stats[3], stats[4], stats[5], stats[6],stats[7],stats[8],stats[9],stats[10]))


        except KeyboardInterrupt:
            e = sys.exc_info()
            logfile.write("\n" + e)
            sys.stdout.flush()
            datafile.close()
            logfile.close()
            vehicle.close()
            return 1
    return 0

def runSITL(vehicle, datafile, logfile):
    while not vehicle.armed:
        time.sleep(0.5)
        logfile.write("\nWaiting for arming")
        sys.stdout.flush()
        print "\nWaiting for arming"

    print "ARMED"
    logfile.write("\nSystem armed, starting logs")
    sys.stdout.flush()

    # for i in range(10):
    while vehicle.armed:
        try:
            time.sleep(0.5)
            stats = get_stats(vehicle)

            datafile.write("\n%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (
                stats[0], stats[1], stats[2], stats[3], stats[4], stats[5], stats[6],stats[7],stats[8],stats[9],stats[10]))
            print("\n%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (
                stats[0], stats[1], stats[2], stats[3], stats[4], stats[5], stats[6],stats[7],stats[8],stats[9],stats[10]))

            # Testing of custom attribute collection, unused for now
            # vehicle.add_attribute_listener('scaled_pressure', special_attribute_callback)
            # time.sleep(5)
            # vehicle.remove_message_listener


        except KeyboardInterrupt:

            e = sys.exc_info()
            print("Keyboard Interrupt, terminating")
            logfile.write("\nKeyboard Interrupt, terminating")
            sys.stdout.flush()
            datafile.close()
            logfile.close()
            vehicle.close()
            return 1

    print("Vechile disarmed, closing files")
    logfile.write("\nVehicle disarmed, closing files")
    return 0
