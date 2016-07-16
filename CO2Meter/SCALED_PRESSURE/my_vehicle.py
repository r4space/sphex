#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
© Copyright 2015-2016, 3D Robotics.

my_vehicle.py:

Custom Vehicle subclass to add IMU data.
"""

from dronekit import Vehicle


class RawIMU(object):
    """
    The RAW IMU readings for the usual 9DOF sensor setup. 
    This contains the true raw values without any scaling to allow data capture and system debugging.
    
    The message definition is here: https://pixhawk.ethz.ch/mavlink/#RAW_IMU
    
    :param time_boot_us: Timestamp (microseconds since system boot). #Note, not milliseconds as per spec
    :param xacc: X acceleration (mg)
    :param yacc: Y acceleration (mg)
    :param zacc: Z acceleration (mg)
    :param xgyro: Angular speed around X axis (millirad /sec)
    :param ygyro: Angular speed around Y axis (millirad /sec)
    :param zgyro: Angular speed around Z axis (millirad /sec)
    :param xmag: X Magnetic field (milli tesla)
    :param ymag: Y Magnetic field (milli tesla)
    :param zmag: Z Magnetic field (milli tesla)    
    """
    def __init__( self, time_boot_ms=None,press_abs=None, press_diff=None, temperature=None):
        """
        RawIMU object constructor.
        """
        self.time_boot_ms = time_boot_ms
        self.press_abs=press_abs
        self.press_diff=press_diff
        self.temperature=temperature
        
    def __str__(self):
        """
        String representation used to print the RawIMU object. 
        """
        return "SCALED_PRESSURE:time_boot_ms={},press_abs={},press_diff={},temperature={}".format(self.time_boot_ms,self.press_abs,self.press_diff,self.temperature)

   
class MyVehicle(Vehicle):
    def __init__(self, *args):
        super(MyVehicle, self).__init__(*args)

        # Create an Vehicle.raw_imu object with initial values set to None.
        self._raw_imu = RawIMU()

        # Create a message listener using the decorator.   
        @self.on_message('SCALED_PRESSURE')
        def listener(self, name, message):
            """
            The listener is called for messages that contain the string specified in the decorator,
            passing the vehicle, message name, and the message.
            
            The listener writes the message to the (newly attached) ``vehicle.raw_imu`` object 
            and notifies observers.
            """
            
            self._raw_imu.time_boot_ms = message.time_boot_ms
            self._raw_imu.press_abs=message.press_abs
            self._raw_imu.press_diff=message.press_diff
            self._raw_imu.temperature=message.temperature

            # Notify all observers of new message (with new value)
            #   Note that argument `cache=False` by default so listeners
            #   are updated with every new message
            self.notify_attribute_listeners('scaled_pressure', self._raw_imu) 

    @property
    def raw_imu(self):
        return self._raw_imu
