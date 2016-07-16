#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dronekit import Vehicle

class GPIC(object):
    """ The filtered global position (e.g. fused GPS and accelerometers). The position is in GPS-frame (right-handed, Z-up).
        It is designed as scaled integer message since the resolution of float is not sufficient. NOTE: This message is intended for onboard networks / companion computers and higher-bandwidth links and optimized for accuracy and completeness. Please use the GLOBAL_POSITION_INT message for a minimal subset.
        The RAW IMU readings for the usual 9DOF sensor setup.
        The message definition is here: https://pixhawk.ethz.ch/mavlink/#63
        :param time_boot_ms:   uint32_t    Timestamp (milliseconds since system boot)
        :param time_utc:    uint64_t    Timestamp (microseconds since UNIX epoch) in UTC. 0 for unknown. Commonly filled by the precision time source of a GPS receiver.
        :param estimator_type:  uint8_t Class id of the estimator this estimate originated from.
        :param lat: int32_t Latitude, expressed as degrees * 1E7
        :param lon: int32_t Longitude, expressed as degrees * 1E7
        :param alt: int32_t Altitude in meters, expressed as * 1000 (millimeters), above MSL
        :param relative_alt:    int32_t Altitude above ground in meters, expressed as * 1000 (millimeters)
        :param vx:  float   Ground X Speed (Latitude), expressed as m/s
        :param vy:  float   Ground Y Speed (Longitude), expressed as m/s
        :param vz:  float   Ground Z Speed (Altitude), expressed as m/s
        :param covariance:  float[36]   Covariance matrix (first six entries are the first ROW, next six entries are the second row, etc.)
    """

    def __init__(self, time_boot_us=None, time_uc=None, estimator_type=None, lat=None, long=None, alt=None,
                 relative_alt=None, vx=None, vy=None, vz=none, covariance=None)
        """
        GPIC object constructor.
        """
        self.time_boot_us = time_boot_us
        self.time_utc = time_utc
        self.estimator_type = estimator_type
        self.lat = lat
        self.lon = lon
        self.alt = alt
        self.relative_alt = relative_alt
        self.vx = vx
        self.vy = vy
        self.covariance = covariance

    def __str__(self):
        """
        String representation used to print the GPIC object. 
        """
        return "GPIC: time_boot_us={},time_utc={},estimator_type={},lat={},lon={},alt={},relative_alt={},vx,={},vy={},vz={},covariance={}".format(
            self.time_boot_us, self.time_utc, self.estimator_type, self.lat, self.lon, self.relative_alt, self.vx,
            self.vy, self, vz, self.covariance)


class CustomV(Vehicle):
    def __init__(self, *args):
        super(CustomV, self).__init__(*args)

        # Create an Vehicle.GPIC object with initial values set to None.
        self._gpic = GPIC()

        # Create a message listener using the decorator.   
        @self.on_message('GPIC')
        def listener(self, name, message):
            """
            The listener is called for messages that contain the string specified in the decorator,
            passing the vehicle, message name, and the message.
            
            The listener writes the message to the (newly attached) ``vehicle.raw_imu`` object 
            and notifies observers.
            """
            self._gpic.time_boot_us = message.time_usec
            self._gpic.time_utc = message.time_utc
            self._gpic.estimator_type = message.estimator_type
            self._gpic.lat = message.lat
            self._gpic.lon = message.lon
            self._gpic.alt = message.alt
            self._gpic.relative_alt = message.relative_alt
            self._gpic.vx = message.vx
            self._gpic.vy = message.vy
            self._gpic.vz = message.vz
            self._gpic.covariance = message.covariance
            # Notify all observers of new message (with new value)
            #   Note that argument `cache=False` by default so listeners
            #   are updated with every new message
            self.notify_attribute_listeners('gpic', self._gpic)

    @property
    def raw_imu(self):
        return self._gpic
