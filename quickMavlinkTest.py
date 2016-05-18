from dronekit import connect
vehicle = connect('/dev/ttyAMA0', wait_ready=True, baud=57600)
print " GPS: %s" % vehicle.gps_0

vehicle.close()
