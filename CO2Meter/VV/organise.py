""" Shared tool functions for operating readData"""
import os
import use_DK as DK
import co2meter as CO2

#Make next flight dir
def mk_ND(new_dir):
    """Make a new directory
    """
    try:
        a=os.listdir(new_dir)
        num=len(a)
        ND=dataDir+"Flight"+str(num+1).zfill(3)
        os.makedirs(ND)
    except OSError:
        pass

    return ND+"/"

def runREAL(vehicle):
    # Configure I2C if not a simulation
    fr, fw = CO2.configI2C()


    while not vehicle.armed:
        time.sleep(0.5)
        fl.write("\rWaiting for arming")
        sys.stdout.flush()
        print
        "\rWaiting for arming"

    print
    "ARMED"
    fl.write("\nSystem armed, starting logs")

    #TODO replace with check for arming
    for i in range(10):
        try:
            time.sleep(0.5)
            stats = DK.get_position(vehicle)

            ppm = readCO2meter(fr, fw)
            fd.write("\n%s,%s,%s,%s,%s,%s,%s,%s" % (
            ppm, stats[0], stats[1], stats[2], stats[3], stats[4], stats[5], stats[6]))
            print("\n%s,%s,%s,%s,%s,%s,%s,%s" % (
            ppm, stats[0], stats[1], stats[2], stats[3], stats[4], stats[5], stats[6]))

            print
            " Battery: %s" % vehicle.battery

        except KeyboardInterrupt:
            e = sys.exc_info()
            fl.write("\n" + e)
            fd.close()
            fl.close()
            vehicle.close()

def runSITL(vehicle):
    while not vehicle.armed:
        time.sleep(0.5)
        fl.write("\rWaiting for arming")
        sys.stdout.flush()
        print
        "\rWaiting for arming"

    print
    "ARMED"
    fl.write("\nSystem armed, starting logs")

    for i in range(10):
        try:
            time.sleep(0.5)
            stats = get_position(vehicle)

            if sim:
                fd.write(
                    "\n%s,%s,%s,%s,%s,%s,%s" % (stats[0], stats[1], stats[2], stats[3], stats[4], stats[5], stats[6]))
                print("\n%s,%s,%s,%s,%s,%s,%s" % (stats[0], stats[1], stats[2], stats[3], stats[4], stats[5], stats[6]))
            else:

                ppm = readCO2meter(fr, fw)
                fd.write("\n%s,%s,%s,%s,%s,%s,%s,%s" % (
                ppm, stats[0], stats[1], stats[2], stats[3], stats[4], stats[5], stats[6]))
                print("\n%s,%s,%s,%s,%s,%s,%s,%s" % (
                ppm, stats[0], stats[1], stats[2], stats[3], stats[4], stats[5], stats[6]))

            print
            " Battery: %s" % vehicle.battery

        except KeyboardInterrupt:

            e = sys.exc_info()
            fl.write("\n" + e)
            fd.close()
            fl.close()
            vehicle.close()
