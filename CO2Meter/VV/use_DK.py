""" Shared tool functions for interacting with the vehicle"""


def get_position(vehicle):
    """Return vehicle position attributes in a list"""
    lat = vehicle.location.global_frame.lat
    long = vehicle.location.global_frame.lon
    alt = vehicle.location.global_frame.alt
    air_spd = vehicle.airspeed
    mode = str(vehicle.mode)
    mode=mode.split(":")[1]
    gps_stat = str(vehicle.gps_0)
    fix = gps_stat.split(":")[1].split(",")[0].split('=')[1]
    count = gps_stat.split(":")[1].split(",")[1].split('=')[1]
    return [lat,long,alt,air_spd,mode,fix,count]

# Add observer for the custom attribute
def raw_imu_callback(self, attr_name, value):
    # attr_name == 'raw_imu'
    # value == vehicle.raw_imu
    print (value)

def start_sitl(MyVehicle):
    """Start simulator and return connected vehicle"""
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()
    print ('Connecting to vehicle in sitl')
    vehicle = connect(connection_string, wait_ready=True, vehicle_class=MyVehicle)
    return vehicle
