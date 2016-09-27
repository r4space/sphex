- Ensure /home/pi/DATA_STORE/ contains no old flights you no longer want or at least note the last flight number so you know what number you are starting on

- On boot the pi will automatically begin running the datalogging script this script will begin logging CO2 readings from when the Iris is armed, and will store these values to file when unarmed.

- A second flight can be begun without power cycling, however if you encounter anomalies simply power cycle the system.

- Error logs and basic logs of operation of the data logging can be found both in the /home/pi/DATASTORE/Flight00x directory for a given flight and in /tmp/mylog. This latter file stores the log for a given power cycle and therefore could contain data from multiple flights but is lost on reboot. 


