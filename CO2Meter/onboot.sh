#!/bin/bash

sudo modprobe -r i2c_bcm2708
sudo modprobe i2c_bcm2708 baudrate=9600

python /home/jwyngaard/work/DRONES/vermont.git/CO2Meter/readData.py &
