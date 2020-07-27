import datetime
import time
import os
import h5py
import numpy as np
import matplotlib.pyplot as plt
import glob
from dateutil.relativedelta import relativedelta
import pandas as pd

class hdf5():

    def __init__(self):
        self.lookforfile = None
        self.length_olddata = None
        self.last_olddata = None
        self.data_stamp = None
        self.savefile = None
        self.savefolder = './home/climatedata/'
        self.searchdata = None

    def climateupdatehdf5(self, climate_name, climate_time, climate_temp, climate_humid, climate_baro):
        try:
        # checks to see if the file already exist - if the file does not exist make it and put data in.
            self.savefile = self.savefolder + climate_name
            self.lookforfile = os.path.isfile(self.savefile)
            print('If HD5F file present?')
            print(lookforfile)
            os.path.isfile(self.savefile)

        except:
            print('making file')
        # if the file does not exist - create it and set up
            with h5py.File(self.savefile, 'a') as f:
                data_type = np.dtype('i4')
                self.data_stamp = f.create_dataset('compiled_data', shape=(1, 7), maxshape=(None, 7), dtype=data_type)
                self.data_stamp[0, 0] = climate_time
                self.data_stamp[0, 1] = climate_temp
                self.data_stamp[0, 2] = climate_humid
                self.data_stamp[0, 3] = climate_baro
                self.length_olddata = len(f['compiled_data'])
                print(self.length_olddata)
                print('closing file after create')
                f.close()

        print('Opening HDF5 file')
        with h5py.File(self.savefile, 'a') as f:
            self.length_olddata = len(f['compiled_data'])
            print('size of the climate HD5F array')
            print(self.length_olddata)
            #scan the unix time to see if new number is there
                for unixsearch in range(self.length_oldata):
                    self.searchdata = f['compiled_data'][unixserach, 0]
                    if self.searchdata = climate_time:
                        print('entry is in database - going to next entry')


            # pulls up the last item in the list to compare to item to be added
                self.last_olditem = self.length_olddata - 1
                self.last_olddata = f['compiled_data'][self.last_olditem,0]

                if climate_time - self.last_oldata = 3600:
                    print('data will be entered')
                    f['compiled_data'].resize((f['compiled_data'].shape[0] + 1, f['compiled_data'].shape[1]))
                    f['compiled_data'][self.length_olddata, 0] = climate_time
                    f['compiled_data'][self.length_olddata, 1] = climate_temp
                    f['compiled_data'][self.length_olddata, 2] = climate_humid
                    f['compiled_data'][self.length_olddata, 3] = climate_baro
                    print('data entered')
                    print('closing file')
                    f.close()




class climatefile():

    def __init__(self):
        self.h5pyclimate = 'climatedata.hdf5'
        self.inputfilename = 'weatherstats_ottawa_hourly.csv'
        self.filenameloc = './home/climatedata/'
        self.inputone = None
        self.climatedataupdate = None
        self.climateupdate_size = None
        self.inputname = None
        self.callDHF5 = None

    def updateclimate(self):
        print('download climate hourly file from: https://ottawa.weatherstats.ca/download.html to /home/climatedata')
        self.inputone = input('Is the file name weatherstats_ottawa_hourly.csv ? (y or n)')
        if self.inputone == 'n':
            self.inputfilename = input('What is the full name of the file?')
            self.inputname = self.filenameloc + self.inputfilename
        if self.inputone == 'y':
            self.inputname = self.filenameloc + self.inputfilename

        print('filename is' + ' ' + self.inputname)
        self.climatedataupdate = pd.read_csv(self.inputname, index_col='date_time_local')
        self.climateupdate_size = self.climatedataupdate.shape

        print(self.climateupdate_size)
        print(self.climatedataupdate.unixtime[5])


runupdate = climatefile()
runupdate.updateclimate()


