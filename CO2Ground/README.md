This is a project wide readme relating to far more than just the attached code
#Running CO2 ground station collection
1. Power up Pi-Sensor systems
2. Wait ~15minutes for sensors to warm up
3. While waiting:
    ## Option for using 1 Pi:
        - connect ethernet cable from laptop to Pi
        $ ssh VT
        $ cd CO2Ground

    ## To get help on the options and what does what:
    $ python CollectData.py -h
    
    ## Here's an example of correctly calling the script including all optional parameters.  Both of the following will do exactly the same thing, the 2nd line simply uses the long form of the flags
    $ python CollectData.py -f FieldASite1_Monday_1_08_17.csv -s 2 -d 1.5 -p 5 -sp -st
    OR
    $ python CollectData.py --filename FieldASite1_Monday_1_08_17.csv --sensors 2 --duration 1.5 --period 5 --showprogress --settime

    ## To set script going and be able to disconnect and then later reconnect and still monitor the progress the following is suggested.
        But note that regardless the data will log and be saved in file unless you cancle it or unplug
        $ ssh VT    //Or however you are logging into Pi
        $ screen
            $ <run python CollectData.py scrip with -sp (show progress) so that captured values and time are printed to the screen
            - press ctrl a d    //This will detactch you from the bash screen session and you can now disconnect from the pi
        - When you want to reconnect to the pi:
        $ ssh VT    //Or however you are logging into Pi
        $ screen -r
        - You should now see your previous screen with logged data displaying

    ##To copy data off the Pi after you are finished:
        - on laptop:
            $ cd into directory you want data to be in on laptop
            $ scp pi@VT:/home/pi/GROUNDDATA/* ./
        

#Connecting CO2 to Pis:
- Connect the free pins end of the USB-to-serial cable to the CO2meter as follows:
    - Pin0 on the CO2meter is the tiny little square hole in the back row of holes along the side with the most holes (2 rows)
    - Counting left to right:
        - Pin1 = White wire (RX to TX on CO2 board)
        - Pin2 = Green wire (Tx to RX on CO2 board)
        - Pin3 = Red wire (5V supply)
        - Pin4 = Black wire (Ground)

#Connecting Pixhawk to Pis:
- Connect 1 of the custom made cables to a Telem port
- Configure the pixhawk (use mission planner/QGC)
    - set baud rate to 57600
    - set SERIAL<X>_PROTOCOL = 1  //X = Telem port number
- Connect the single ends to the Pi GPIO pins as follows 
[see [here](http://ardupilot.org/dev/docs/raspberry-pi-via-mavlink.html) for a picture
    Count on Pi from top left (with USB ports on your right)
        -- Telem Pin1 (red) - No Connection (cover in tape)
        -- Telem Pin2 to GPIO5
        -- Telem Pin3 to GPIO4
        -- Telem Pin4 - No Connection (cover in tape)
        -- Telem Pin5 - No Connection (cover in tape)
        -- Telem Pin6 to GPIO3


#How to configure a new Pi
- Create new SD card image:
    ## Format SDcard
        - Format new card with gparted to be 1 blank FAT32 partition, suggest labeling VT1 or something both digitally and with a sharpie on the outside:
            - Find the SD card on laptop
                $ df-h 
            - format it
                $ sudo gparted  
                - perform formating in GUI
                    -- if 32GB, format into 2 16GB partitions(1:16385 called VT<x>, and the rest called FREE)
            - Eject SD card and reinsert
    ## Write new image to formated SD card 
        $ umount </dev/sdb1>    #Or whatever the location is sdb<x>
        $ sudo dd bs=4M if=~/SDCardBackup.img of=/dev/sdb status=progress   #Note: If 16GB don't include any partition number, if 32GB, use the correct partition number. And, this will take quite a while (~30 minutes)
        $ sudo sync

- Boot and configure new image:
    - Boot new card in a Pi
    - ssh into new image:
        $ ssh pi@192.168.0.12   #Password is Vermont
        $ sudo raspi-config
        - follow instructions in the GUI that comes up to give it a new name, suggest VT<x> where x is an incremental number

#How to add a new wifi network to the Pi3
- Onboard the Pi:
$ sudo vim /etc/wpa_supplicant/wpa_supplicant.conf
>>> Go to the bottom of the file and add the following:
    network={
       ssid="<name of your network>"
        psk="<passowrd for your network>"
    }
>>> If the network has no security  - no password, do this instead:
    network={
        ssid="testing"
        key_mgmt=NONE
    }
