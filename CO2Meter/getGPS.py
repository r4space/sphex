from dronekit import connect, VehicleMode
import time
vehicle = connect('/dev/ttyAMA0', wait_ready=True, baud=57600)


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



for i in range(5):
	stats=get_position(vehicle)
	print"%s,%s,%s,%s,%s,%s,%s" % (stats[0],stats[1],stats[2],stats[3],stats[4],stats[5],stats[6])
	time.sleep(0.5)



vehicle.close()


