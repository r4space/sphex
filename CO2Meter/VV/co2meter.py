""" Shared tool functions for interacting with the external sensors"""
import array, time, io, fcntl, sys

def readCO2meter(fr,fw):

    #REQUEST
    CMD = bytearray([0x22,0x00,0x08,0x2A])
    try:
        fw.write(CMD) #sending config register bytes
    except IOError as e:
        e = sys.exc_info()

    time.sleep(0.02)

    #RECEIVE
    buf=256
    try:
        data = fr.read(4) #read 4 bytes
        buf = array.array('B', data)
        #Returns the CO2 value in ppm by joining Byte1 and Byte2
        val=(buf[1]*256+buf[2])

    except IOError as e:
        e = sys.exc_info()
        print "Unexpected I2C errors: ",e
    return val

#I2C Setup
def configI2C():
    """ Configure I2C for reading from CO2Meter, return tuple (fr,fw)"""
    print ("Configuring I2C")
    I2C_SLAVE=0x0703
    ADDR = 0x68
    bus=1
    fr = io.open("/dev/i2c-"+str(bus), "rb", buffering=0)
    fw = io.open("/dev/i2c-"+str(bus), "wb", buffering=0)
    fcntl.ioctl(fr, I2C_SLAVE, ADDR)
    fcntl.ioctl(fw, I2C_SLAVE, ADDR)
    return fr,fw