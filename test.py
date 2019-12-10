import glob
import os
import datetime
import time
from dateutil.relativedelta import relativedelta
import h5py
import numpy as np

arr = []

location = '/home/pi/'

fileset = [file for file in glob.glob(location + '*.hdf5')]

for file in fileset:
    head, tail = os.path.split(file)
    arr.append(tail)

print(arr)


# fileset.sort()
# for file in fileset:
    # print(file)
