import datetime
import time
import os
import h5py
import numpy as np
import matplotlib.pyplot as plt
import glob
from dateutil.relativedelta import relativedelta
import pandas as pd

# LEGEND FOR HDF5FILE
# 0 unixtime for downloaded climate data
# 1 temp for downloaded climate data
# 2 humidity for downloaded climate data
# 3 baro for downloaded climate data
# 4 time from dataset
# 5 temp from dataset
# 6 humidity from dataset
# 7 baro from dataset

class hdf5compile():

    def __init__(self):
        self.prebarodatafileloc = '/home/pi/climatedata/datafilesold/'
        self.barodatafileloc = '/home/pi/climatedata/datafiles/'
        self.h5pyclimatefile = '/home/pi/climatedata/climatedata.hdf5'
        self.filelist = None
        self.climateunixdata = []
        self.firsttimeentry = None
        self.datasetoldtemp = None
        self.datasetoldhumid = None
        self.nearestvalue = None
        self.timeentryindex = None
        self.timeentryindex_temp = None
        self.datasetoldtime = None
        self.datasetoldbaro = None

    def complileprebaro(self):
        #this is list comprehension
        print('compiling list of pre-baro reading hdf5 files')
        self.filelist = [file for file in glob.glob(self.prebarodatafileloc + '*.hdf5')]
        print('sort files ascending')
        self.filelist.sort()
        print(self.filelist)
        with h5py.File(self.h5pyclimatefile, 'a') as f:
            self.climateunixdata = f['compiled_data'][:, 0]
            for dataset in self.filelist:
                with h5py.File(dataset, 'a') as b:
                    self.firsttimeentry = b['dailydata/temperature_C'][0,0]
                    print('first time entry:')
                    print(self.firsttimeentry)
                    self.nearestvalue = self.climateunixdata[min(range(len(self.climateunixdata)), key = lambda i: abs(self.climateunixdata[i]-self.firsttimeentry))]
                    print('nearest entry in climatedata:')
                    print(self.nearestvalue)
                    self.timeentryindex_temp = np.where(self.climateunixdata == self.nearestvalue)
                    self.timeentryindex = self.timeentryindex_temp[0][0]
                    print('nearest entry index location:')
                    print(self.timeentryindex)
                    for datapoints in range(len(b['dailydata/temperature_C'])):
                        print('data entry:')
                        print(datapoints)
                        print('at:')
                        print(self.timeentryindex)
                        self.datasetoldtime = b['dailydata/temperature_C'][datapoints, 0]
                        self.datasetoldtemp = b['dailydata/temperature_C'][datapoints,1]
                        self.datasetoldhumid = b['dailydata/humidity'][datapoints,1]
                        f['compiled_data'][self.timeentryindex, 4] = self.datasetoldtime
                        f['compiled_data'][self.timeentryindex, 5] = self.datasetoldtemp
                        f['compiled_data'][self.timeentryindex, 6] = self.datasetoldhumid
                        self.timeentryindex += 1
                    b.close()
        f.close()

    def complilepostbaro(self):
        #this is list comprehension
        print('compiling list of pre-baro reading hdf5 files')
        self.filelist = [file for file in glob.glob(self.barodatafileloc + '*.hdf5')]
        print('sort files ascending')
        self.filelist.sort()
        print(self.filelist)
        with h5py.File(self.h5pyclimatefile, 'a') as f:
            self.climateunixdata = f['compiled_data'][:, 0]
            for dataset in self.filelist:
                with h5py.File(dataset, 'a') as b:
                    self.firsttimeentry = b['dailydata/temperature_C'][0,0]
                    print('first time entry:')
                    print(self.firsttimeentry)
                    self.nearestvalue = self.climateunixdata[min(range(len(self.climateunixdata)), key = lambda i: abs(self.climateunixdata[i]-self.firsttimeentry))]
                    print('nearest entry in climatedata:')
                    print(self.nearestvalue)
                    self.timeentryindex_temp = np.where(self.climateunixdata == self.nearestvalue)
                    self.timeentryindex = self.timeentryindex_temp[0][0]
                    print('nearest entry index location:')
                    print(self.timeentryindex)
                    for datapoints in range(len(b['dailydata/temperature_C'])):
                        print('data entry:')
                        print(datapoints)
                        print('at:')
                        print(self.timeentryindex)
                        self.datasetoldtime = b['dailydata/temperature_C'][datapoints, 0]
                        self.datasetoldtemp = b['dailydata/temperature_C'][datapoints,1]
                        self.datasetoldhumid = b['dailydata/humidity'][datapoints,1]
                        f['compiled_data'][self.timeentryindex, 4] = self.datasetoldtime
                        f['compiled_data'][self.timeentryindex, 5] = self.datasetoldtemp
                        f['compiled_data'][self.timeentryindex, 6] = self.datasetoldhumid
                        f['compiled_data'][self.timeentryindex, 7] = self.datasetoldbaro
                        self.timeentryindex += 1
                    b.close()
        f.close()

class climatefile():

    def __init__(self):
        self.inputfilename = 'weatherstats_ottawa_hourly.csv'
        self.h5pyclimate = 'climatedata.hdf5'
        self.filenameloc = '/home/pi/climatedata/'

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
        self.climate_time_local = None
        self.climate_temp = None
        self.climate_humid = None
        self.climate_baro = None

        self.searchrange = None

    def initclimateupdate(self):
        print('download climate hourly file from: https://ottawa.weatherstats.ca/download.html to /home/pi/climatedata/')
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
                data_type = np.dtype('float')
                self.climatehdf5entry = f.create_dataset('compiled_data', shape=(1, 8), maxshape=(None, 8), dtype=data_type)
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


# ############### PROGRAM ########################

beginprogram = input('1. Update climate records; 2. Compile HDF5 data pre barometric reading; 3. Compile HDF5 data post barometric reading')
if beginprogram == '1':
    print('1: init class')
    runupdate = climatefile()
    print('master - initclimateupdate')
    runupdate.initclimateupdate()
    print('master - climatehdf5size - get size and init if needed')
    runupdate.climatehdf5size()
    print('master - climateupdateserach - see if the update overlaps with the old')
    runupdate.climateupdatesearch()
    print('master - climateupdatecompile - get the data I need from the weather service into hdf5')
    runupdate.climateupdatecompile()
if beginprogram == '2':
    print('2: init class')
    olddatacompile = hdf5compile()
    print('compile old data')
    olddatacompile.complileprebaro()
if beginprogram == '3':
    print('2: init class')
    olddatacompile = hdf5compile()
    print('compile old data')
    olddatacompile.complilepostbaro()


