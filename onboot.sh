#!/bin/bash
exec &>/tmp/my.log
echo "hello log"
sleep 60
echo "ok made through 60ec"

sudo modprobe -r i2c_bcm2708
sudo modprobe i2c_bcm2708 baudrate=9600

echo "ok starting py script"
python /home/pi/vermont/CO2Meter/readData.py &
echo "ok excited py script"
