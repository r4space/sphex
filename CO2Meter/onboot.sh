#!/bin/bash

sleep 60
sudo modprobe -r i2c_bcm2708
sudo modprobe i2c_bcm2708 baudrate=9600

python /home/pi/vermont/CO2Meter/readData.py &
