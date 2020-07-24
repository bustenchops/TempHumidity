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

    def __init__(self):
        self.lookforfile = None
        self.length_olddata = None
        self.last_olddata = None
        self.data_stamp = None

    def climatehdf5(self, climate_name, climate_time, climate_temp, climate_humid, climate_baro):
        try:
            # checks to see if the file already exist - if the file exists open it and determine the size of the range.
            os.path.isfile(climate_name)
            print('opening file')
            lookforfile = os.path.isfile(climate_name)
            print('if HD5F file present')
            print(lookforfile)
            with h5py.File(climate_name, 'a') as f:
                self.length_olddata = len(f['dailydata/climate_data'])
                print('size of the climate HD5F array')
                print(self.length_olddata)
                self.last_olddata = f[] # stopped here....get the recent data from the climate update and compare to the oldest in file needs to be 3100<>4100 and then can add otherwise tell to get a better list. also needs to scrollthrough





                f['dailydata/climate_data'].resize(
                    (f['dailydata/climate_data'].shape[0] + 1, f['dailydata/climate_data'].shape[1]))
                f['dailydata/climate_data'][loc_timestamp, 0] = climate_time
                f['dailydata/climate_data'][loc_timestamp, 1] = climate_temp
                f['dailydata/climate_data'][loc_timestamp, 2] = climate_humid
                f['dailydata/climate_data'][loc_timestamp, 3] = climate_baro
                print('closing file')
                f.close()
        except IOError:
            print('making file')
            # if the file does not exist - create it and set up
            with h5py.File(climate_name, 'a') as u:
                climate_data = u.create_group('dailydata')
                dt = np.dtype('i4')
                self.data_stamp = dataforday.create_dataset('climate_data', shape=(1, 4), maxshape=(None, 4), dtype=dt)
                self.data_stamp[0, 0] = loc_timestamp
                self.data_stamp[0, 1] = climate_temp
                self.data_stamp[0, 2] = climate_humid
                self.data_stamp[0, 3] = climate_baro
                self.length_olddata = len(u['dailydata/climate_temperature'])
                print(self.length_olddata)
                print('closing file after create')
                u.close()


class climatefile():

    def __init__(self):
        self.h5pyclimate = 'climatedata.hdf5'
        self.inputfilename = 'weatherstats_ottawa_hourly.csv'
        self.inputone = None
        self.climatedataupdate = None
        self.climateupdate_size = None
        self.filenameloc = None

    def updateclimate(self):
        print('download climate hourly file from: https://ottawa.weatherstats.ca/download.html to /home/climatedata')
        self.inputone = input('Is the file name weatherstats_ottawa_hourly.csv ? (y or n)')
        if self.inputone == 'n':
            self.inputfilename = input('What is the full name of the file?')
            self.filenameloc = './home/climatedata/' + self.inputfilename
        if self.inputone == 'y':
            self.filenameloc = './home/climatedata/'+self.inputfilename

        print('filename is' + ' ' + self.inputfilename)
        self.climatedataupdate = pd.read_csv(self.filenameloc, index_col='date_time_local')
        self.climateupdate_size = self.climatedataupdate.shape

        print(self.climateupdate_size)
        print(self.climatedataupdate.unixtime[5])


runupdate = climatefile()
runupdate.updateclimate()


