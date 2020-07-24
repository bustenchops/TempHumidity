import datetime
import time
import os
import h5py
import numpy as np
import matplotlib.pyplot as plt
import glob
from dateutil.relativedelta import relativedelta
import pandas as pd

filename = './home/weatherstats_ottawa_hourly.csv'

class hdf5():

    def hd5file(self, fname, timestamp_s, hdftemp, hdfhumidy):
        try:
            # checks to see if the file already exist - if the file exists open it and determine the size of the range.
            os.path.isfile(fname)
            print('opening file')
            aft = os.path.isfile(fname)
            print('if HD5F file present')
            print(aft)
            with h5py.File(fname, 'a') as f:
                # temptemp = 100
                # temphumidy = 100
                num_timestamp = len(f['dailydata/temperature_C'])
                print('size of the HD5F array')
                print(num_timestamp)
                f['dailydata/temperature_C'].resize((f['dailydata/temperature_C'].shape[0] + 1, f['dailydata/temperature_C'].shape[1]))
                f['dailydata/humidity'].resize((f['dailydata/humidity'].shape[0] + 1, f['dailydata/humidity'].shape[1]))
                f['dailydata/temperature_C'][num_timestamp, 0] = timestamp_s
                f['dailydata/temperature_C'][num_timestamp, 1] = hdftemp
                f['dailydata/humidity'][num_timestamp, 0] = timestamp_s
                f['dailydata/humidity'][num_timestamp, 1] = hdfhumidy
                print('closing file')
                f.close()
        except IOError:
            print('making file')
    # if the file does not exist - create it and set up
            with h5py.File(fname, 'a') as u:
                # temptemp = 99
                # temphumidy = 99
                dataforday = u.create_group('dailydata')
                dt = np.dtype('i4')
                datatemp_stamp = dataforday.create_dataset('temperature_C', shape=(1, 2), maxshape=(None, 2), dtype=dt)
                datahumid_stamp = dataforday.create_dataset('humidity', shape=(1, 2), maxshape=(None, 2), dtype=dt)
                datatemp_stamp[0, 0] = timestamp_s
                datatemp_stamp[0, 1] = hdftemp
                datahumid_stamp[0, 0] = timestamp_s
                datahumid_stamp[0, 1] = hdfhumidy
                num_timestamp = len(u['dailydata/temperature_C'])
                print(num_timestamp)
                print('closing file again')
                u.close()

class climatefile():

    def __init__(self):
        self.h5pyclimate = 'climatedata.hdf5'
        self.inputfilename = 'weatherstats_ottawa_hourly.csv'
        self.inputone = None

    def updateclimate(self):
        print('download climate hourly file from: https://ottawa.weatherstats.ca/download.html to /home/climatedata')
        self.inputone = input('Is the file name weatherstats_ottawa_hourly.csv ? (y or n)')
        if self.inputone == 'n':
            self.inputfilename = input('What is the full name of the file?')
            return (self.inputfilename)
        if self.inputone == 'y':
            return (self.inputfilename)




df = pd.read_csv(filename, index_col='date_time_local')
print(df.unixtime[0:5])

