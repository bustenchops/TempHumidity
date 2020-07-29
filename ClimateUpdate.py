import datetime
import time
import os
import h5py
import numpy as np
import matplotlib.pyplot as plt
import glob
from dateutil.relativedelta import relativedelta
import pandas as pd

class hdf5compile():

    def __init__(self):
        pass

class climatefile():

    def __init__(self):
        self.inputfilename = 'weatherstats_ottawa_hourly.csv'
        self.h5pyclimate = 'climatedata.hdf5'
        self.filenameloc = './home/climatedata/'

        self.inputone = None
        self.inputname = None
        self.inputconfirm = None
        self.inputbackup = None

        self.climatedataupdate = None
        self.climateupdate_size = None

        self.savefile = None
        self.lookforfile = None

        self.length_olddata = None
        self.climatehdf5entry = None

        self.lastnum_olddata = None
        self.lastentry_olddata = None
        self.searchdata = 1
        self.updatesearch = None



        self.climate_time = None
        self.climate_temp = None
        self.climate_humid = None
        self.climate_baro = None

        self.searchrange = None

    def initclimateupdate(self):
        print('download climate hourly file from: https://ottawa.weatherstats.ca/download.html to /home/climatedata/')
        print('MAKE SURE THE FILE YOU WISH TO ADD OVERLAPS DATAPOINTS WITH THE HDF5 ENTRY')
        self.inputbackup = input('Backup the original HDF5 file before continuing - press ENTER to continue')
        self.inputone = input('Is the file name weatherstats_ottawa_hourly.csv ? (y or n)')
        if self.inputone == 'n':
            self.inputfilename = input('What is the full name of the file?')
        self.inputname = self.filenameloc + self.inputfilename
        print('filename to update from is ' + ' ' + self.inputname)
        print('updating file ' + self.h5pyclimate)

        #take CVS update file and put in Pandas array - determine size
        self.climatedataupdate = pd.read_csv(self.inputname, index_col='date_time_local')
        self.climateupdate_size = self.climatedataupdate.shape[0]

        # checks to see if the file already exist - if the file does not exist make it and put data in.
        self.savefile = self.filenameloc + self.h5pyclimate
        self.lookforfile = os.path.isfile(self.savefile)
        print('Is HD5F file present?')
        print(self.lookforfile)


    def climatehdf5size(self):
        if os.path.isfile(self.savefile):
            print('Opening HDF5 file')
            with h5py.File(self.savefile, 'a') as f:
                self.length_olddata = len(f['compiled_data'])
                print('size of the climate HD5F array')
                print(self.length_olddata)
                print('closing file after size check')
                f.close()
        else:
            print('making HDF5 file')
            # if the file does not exist - create it and set up
            with h5py.File(self.savefile, 'a') as f:
                data_type = np.dtype('i4')
                self.climatehdf5entry = f.create_dataset('compiled_data', shape=(1, 7), maxshape=(None, 7), dtype=data_type)
                self.length_olddata = len(f['compiled_data'])
                print('size of the climate HD5F array')
                print(self.length_olddata)
                print('closing file after create')
                f.close()


    def climateupdatesearch(self):
        if os.path.isfile(self.savefile):
            print('Opening HDF5 file')
            self.lastnum_olddata = self.length_olddata - 1
            with h5py.File(self.savefile, 'a') as f:
                self.lastentry_olddata = f['compiled_data'][self.lastnum_olddata, 0]
                f.close()
            # scan the unix time to see if new number is there
            while self.searchdata == 1:
                self.climateupdate_size = self.climateupdate_size - 1
                if self.climateupdate_size < 0:
                    self.searchdata = 2
                    print('the update file does not go back far enough for consistent data, re-download with more rows')
                    print('if this is a new file then continue')
                    self.inputconfirm = input('Do you want to continue? (y or n)')
                    if self.inputconfirm == 'y':
                        self.climateupdate_size = self.climatedataupdate.shape[0] - 1
                        print('size to use is:')
                        print(self.climateupdate_size)
                    else:
                        return()
                self.updatesearch = self.climatedataupdate.unixtime[self.climateupdate_size]
                if self.updatesearch == self.lastentry_olddata:
                    self.searchdata = 2
                    print('Starting entry ')
                    print(self.climateupdate_size)
                    self.climateupdate_size = self.climateupdate_size - 1
                    with h5py.File(self.savefile, 'a') as f:
                        self.lastnum_olddata = len(f['compiled_data'])
                        f['compiled_data'].resize((f['compiled_data'].shape[0] + 1, f['compiled_data'].shape[1]))
                        f.close()
                    print('entry location')
                    print(self.lastnum_olddata)


    def climateupdatecompile(self):
        if os.path.isfile(self.savefile):
            print('Opening HDF5 file')
            with h5py.File(self.savefile, 'a') as f:
                self.lastnum_olddata = len(f['compiled_data']) - 1
                print('using location in existing')
                print(self.lastnum_olddata)
                self.searchrange = self.climateupdate_size + 1
                for passnum in range(self.searchrange):
                    print('defined range:')
                    print(self.searchrange)
                    print('search range passnum:')
                    print(passnum)
                    if self.climateupdate_size < 0:
                        print('complete')
                    else:
                        print('location within update array')
                        print(self.climateupdate_size)
                        self.climate_time = self.climatedataupdate.unixtime[self.climateupdate_size]
                        self.climate_temp = self.climatedataupdate.temperature[self.climateupdate_size]
                        self.climate_humid = self.climatedataupdate.relative_humidity[self.climateupdate_size]
                        self.climate_baro = self.climatedataupdate.pressure_station[self.climateupdate_size]
                        self.climateupdate_size -= 1
                        f['compiled_data'][self.lastnum_olddata, 0] = self.climate_time
                        f['compiled_data'][self.lastnum_olddata, 1] = self.climate_temp
                        f['compiled_data'][self.lastnum_olddata, 2] = self.climate_humid
                        f['compiled_data'][self.lastnum_olddata, 3] = self.climate_baro
                        print('entering climate data location lastnum_olddata')
                        print(self.lastnum_olddata)
                        self.lastnum_olddata += 1
                        if passnum < self.searchrange - 1:
                            f['compiled_data'].resize((f['compiled_data'].shape[0] + 1, f['compiled_data'].shape[1]))
                f.close()

beginprogram = input('1. Update climate records; 2. Compile HDF5 data pre barometric reading; 3. Compile HDF5 data post barometric reading')
if beginprogram == 1:
    print('master - init class')
    runupdate = climatefile()
    print('master - initclimateupdate')
    runupdate.initclimateupdate()
    print('master - climatehdf5size - get size and init if needed')
    runupdate.climatehdf5size()
    print('master - climateupdateserach - see if the update overlaps with the old')
    runupdate.climateupdatesearch()
    print('master - climateupdatecompile - get the data I need from the weather service into hdf5')
    runupdate.climateupdatecompile()
if beginprogram == 2:




