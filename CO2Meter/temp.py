
#Set up option parsing to get connection string
import argparse  
parser = argparse.ArgumentParser(description='Capture Iris and sensor flight data ')
parser.add_argument("-s", "--sitl", help="Use the sitl simulator instead of connecting to the Pixhawk", action="store_true")
args = parser.parse_args()


#Start SITL if no connection string specified
if args.sitl:
    print ("yes")
else:
    print ("no")
