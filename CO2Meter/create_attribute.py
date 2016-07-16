#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
© Copyright 2015-2016, 3D Robotics.

create_attribute.py:

Demonstrates how to create attributes from MAVLink messages within your DroneKit-Python script 
and use them in the same way as the built-in Vehicle attributes.

The code adds a new attribute to the Vehicle class, populating it with information from RAW_IMU messages 
intercepted using the message_listener decorator.

Full documentation is provided at http://python.dronekit.io/examples/create_attribute.html
"""

from dronekit import connect, Vehicle
from CustomV import CustomV
import time

# Connect to the Vehicle
# vehicle = connect(connection_string, wait_ready=True, vehicle_class=MyVehicle)
vehicle = connect('/dev/ttyAMA0', wait_ready=True, baud=57600, vehicle_class=CustomV)

# Add observer for the custom attribute

def raw_imu_callback(self, attr_name, value):
    # attr_name == 'raw_imu'
    # value == vehicle.raw_imu
    print value

vehicle.add_attribute_listener('raw_imu', raw_imu_callback)

print 'Display RAW_IMU messages for 5 seconds and then exit.'
time.sleep(5)

#The message listener can be unset using ``vehicle.remove_message_listener``

#Close vehicle object before exiting script
print "Close vehicle object"
vehicle.close()
