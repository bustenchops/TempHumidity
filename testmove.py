import datetime
import time
import os
import h5py
import threading
import numpy as np
import glob


dest = '/home/pi/climatedata/datafiles/'
fileglob = glob.glob('*.hdf5')
print(fileglob)
if os.path.exists(dest):
    print('daily directory exists')
    print(dest)
    todaytemp = datetime.datetime.now().strftime("%Y-%m-%d")
    todaytime = datetime.datetime.strptime(todaytemp, "%Y-%m-%d")
    for i in fileglob:
        print('file:', i)
        names, ext = os.path.splitext(i)
        namedateobj = datetime.datetime.strptime(names, '%Y-%m-%d-week_%U')
        if namedateobj < todaytime:
            print('file is from previous day')
            print('moving to /home/pi/Gits/TempHumidity/' + i + ' ' + dest)
            os.system('mv /home/pi/Gits/TempHumidity/' + i + ' ' + dest)