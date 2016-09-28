#! /bin/bash

exec &>/tmp/my.log

echo "Hello log"

sudo modprobe -r i2c_bcm2708
sudo modprobe i2c_bcm2708 baudrate=9600

sleep 30
echo "ok made through 30 second delay"

python /home/pi/sphex/CO2Meter/readData.py


