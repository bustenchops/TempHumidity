import datetime
import time
import os
import h5py
import threading
import numpy as np
import matplotlib.pyplot as plt
import glob

# testtime = "2019-10-17"
# t1a = datetime.datetime.strptime(testtime, '%Y-%m-%d')
# print(t1a)
todaytemp = datetime.datetime.now().strftime("%Y-%m-%d")
todaytime = datetime.datetime.strptime(todaytemp, "%Y-%m-%d")

fileglob = glob.glob('*.hdf5')
for i in fileglob:
    print(i)
    names, ext = os.path.splitext(i)
    namedateobj = datetime.datetime.strptime(names, '%Y-%m-%d')
    if namedateobj < todaytime:
        print(todaytime)
        print("good")
        print(i)
#        os.system('mv /home/pi/' + i + ' /home/pi/data/daily/')
