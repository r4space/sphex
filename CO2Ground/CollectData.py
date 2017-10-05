#Collect data from CO2 meters on Pi3 USB ports via serial to FTDI cables
import serial, time, sys, datetime, argparse, os
#CONFIGURATION
DataDir="/home/pi/DATA/"


def SetSystemTime():
    """ Captures a date and time and sets the inputs as the system date and time.  Minimul date entry santitisation preformed
    """
    monthDict={1:'JAN', 2:'FEB', 3:'MAR', 4:'APR', 5:'MAY', 6:'JUN', 7:'JUL', 8:'AUG', 9:'SEP', 10:'OCT', 11:'NOV', 12:'DEC'}
    day=raw_input("Day: ")
    while not (int(day)>=1 and int(day)<=31):
        print "Invalid day value, please enter a number between 0 and 31"
        day=raw_input("Day: ")
    
    month=raw_input("Month: ")
    while not (int(month)>=1 and int(month)<=13):
        print "Invalid month, please enter a number between 1 and 12"
        month=raw_input("Month: ")
    M=monthDict[int(month)]
    
    year=raw_input("Year: ")
    
    H=raw_input("24 Hour: ")
    while not (int(H)>=0 and int(H)<=23):
        print "Invalid hour, please enter a number between 0 and 24"
        H=raw_input("24 Hour: ")

    minutes=raw_input("Minutes: ")
    while not (int(minutes)>=0 and int(minutes)<=60):
        print "Invalid minutes value, please enter a number between 0 and 60"
        minutes=raw_input("Minutes: ")

    seconds=raw_input("seconds: ")
    while not (int(seconds)>=0 and int(seconds)<=60):
        print "Invalid seconds value, please enter a number between 0 and 60"
        seconds=raw_input("seconds: ")

    DateTime="{0} {1} {2} {3}:{4}:{5}".format(day,M,year,H,minutes,seconds)
    print DateTime
    os.system("sudo date -s \"{}\" ".format(DateTime))


def OpenFiles(filename, directory):
    """Opens and initiates all the CO2 data file names passed in and returns the file handlers in an array
    """
    FileHandle = open(directory+filename,"w")
    FileHandle.write("Time stamp, CO2 ppm\n")
    return FileHandle

def OpenPorts(number):
    """ Tries to open as many /dev/ttyUSB<x> ports as user indicated were present
    """
    sockets=[]
    for port in range(number):
        ser = serial.Serial("/dev/ttyUSB{}".format(str(port)),baudrate =9600,timeout = .5)
        ser.flushInput()
        time.sleep(1)
        sockets.append(ser)
    return sockets

def ReadPPM(stream):
    """ Read data from a CO2 meter and return both the scaled result in ppm and a time stamp from when the reading was receieved
        stream = socket
        returns tuple of strings: time stamp, CO2 ppm value
    """
    stream.flushInput()
    stream.write("\xFE\x44\x00\x08\x02\x9F\x25")
    time.sleep(.5)
    resp = stream.read(7)
    stamp=datetime.datetime.now().strftime('%G-%m-%d-%T')
    try:
        high = ord(resp[3])
        low = ord(resp[4])
        co2 = (high*256) + low
    except IndexError as e:
        e = sys.exc_info()
        print "Unexpected errors reading from socket{0} \n Error: {1}".format(stream,e)
    return stamp,str(co2)

def PowerSaveMode():
    """Disable some high power draw components. """
    check=raw_input("The following operations will disable, bluetooth, the HDMI port, and the wifi.  Do you wish to continue y/n?")
    if str(check).lower()=='y':
        try:
            os.system("sudo /opt/vc/bin/tvservice -o")
            os.system("sudo ifconfig wlan0 down")
            os.system("dtoverlay=pi3-disable-bt")
        except:
            e = sys.exc_info()[0]
            print e



#MAIN
parser = argparse.ArgumentParser('Capture CO2 data')
parser.add_argument('-f','--filename',type=str,help="Enter the file name to store this collections in.",default="newfile")
parser.add_argument('-s','--sensors', help="Enter the number of CO2 sensors plugged in.",type=int,default=1)
parser.add_argument('-d','--duration', help="Enter the length of time you wish the sensors to log data for in minutes",type=float,default=0.1)
parser.add_argument('-p','--period', help="Enter the length of time you wish to elapse between samples",type=float,default=1.5)
parser.add_argument('-st','--settime',action='store_true', help="Use this flag if you wish to set the system date and time.  \nYou will be asked to enter desired values")
parser.add_argument('-sp', '--showprogress',action='store_true', help="Use this flag if you wish to monitor progress by having a log of elapsed time and values printed to screen during capture")
args = parser.parse_args()

if args.settime:
    SetSystemTime()

#SETUP
R='\033[31m'
W='\033[37m'

print "Setting up to read K-30 Via Serial over USB\n"
print "Capturing {0}{2}{1} sensors, at a rate of once every {0}{3}{1} seconds,for a total duration of {0}{4}{1} minutes.  Data will be stored in {0}{5}{1}. \n The current system time - which will be used to timestamp readings is: {0}{6}{1}".format(R,W,args.sensors, args.period, args.duration, DataDir+str(args.filename), os.popen('date').read())
#sensors=os.popen('ls /dev/ | grep USB').read().split('\n')[:-1]
FH=OpenFiles(args.filename,DataDir)
sockets=OpenPorts(int(args.sensors))
capture_duration = args.duration
start_time = time.time()
capture = True
PERIOD=float(args.period)-0.5*int(args.sensors)

#PRIMARY LOOP
while capture:
    try:
        latestPPMs=[]
        for s in sockets:
            values=ReadPPM(s)
            latestPPMs.append(values[1])
        FH.write("{0} , {1} \n".format(values[0] , ', '.join(latestPPMs)))
        elapsed_time = time.time() - start_time 
        
        #Report status
        if args.showprogress:
            print "Elapsed time: {0:.2f} seconds , ppms: {1}".format(elapsed_time,', '.join(latestPPMs))
            #print "Elapsed time: {0:.2f} minutes , ppms: {1}".format(elapsed_time/60,latestPPMs)
        
        #Check exit condition
        if elapsed_time/60 > capture_duration:
            capture = False

        #Wait
        time.sleep(PERIOD)
    except KeyboardInterrupt as e:
        print "Interrupted, closing down"
        FH.close()    
        for s in sockets:
            s.close()
        sys.exit()    

FH.close()    
for s in sockets:
    s.close()
sys.exit()    
