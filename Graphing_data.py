import datetime
import time
import os
import h5py
import numpy as np
import matplotlib.pyplot as plt
import glob
from dateutil.relativedelta import relativedelta
import pandas as pd


class rangeuserinput():

    def __init__(self):
        self.start_date = None
        self.end_date = None
        self.ticks = None

    def definedtime(self):
        print('Input start date yyyy-mm-dd')
        self.start_date = input('Input start date yyyy-mm-dd')
        self.end_date = input('Input end date (inclusive) yyyy-mm-dd')
        self.ticks = input('Input the interval for tick labels in hours')
        return (self.start_date, self.end_date, self.ticks)


class findandplot():

    def __init__(self):
        self.startlocation = './home/pi/climatedata/'
        self.file_name = './home/climatedata/climatedata.hdf5'
        self.day1 = None
        self.ending= None
        self.day1_formatted = None
        self.ending_formatted = None
        self.date_span_timedelta = None
        self.date_span = None
        self.file_name = None
        self.climate_unixdata = []
        self.date_span_short = None
        self.timestamp_start = None
        self.timestamp_end = None
        self.nearestvalue_start = None
        self.timeentryindex_temp_start = None
        self.timeentryindex_start = None
        self.nearestvalue_end = None
        self.timeentryindex_temp_end = None
        self.timeentryindex_end = None
        self.climate_time_array = []
        self.climate_temp_array = []
        self.climate_humidity_array = []
        self.climate_baro_array = []
        self.data_temp_array =[]
        self.data_humidity_array = []
        self.data_baro_array = []
        self.index_tracker = None

    def reporting_dataset(self, firstday, lastday):
        self.day1 = firstday
        self.ending = lastday
        # format the inputs to datetime objects
        self.day1_formatted = datetime.datetime.strptime(self.day1, '%Y-%m-%d')
        self.ending_formatted = datetime.datetime.strptime(self.ending, '%Y-%m-%d')
        self.date_span_timedelta = self.ending_formatted - self.day1_formatted + (datetime.timedelta(days=1))
        self.date_span = pd.Timedelta(self.date_span_timedelta)
        self.date_span_short = self.date_span.days
        print('day1: ', self.day1_formatted, ' lastday: ', self.ending_formatted, ' number days spanned: ', self.date_span_short)
        with h5py.File(self.file_name, 'a') as f:
            self.climate_unixdata = f['compiled_data'][:, 0]
            self.timestamp_start = int(datetime.datetime.timestamp(self.day1_formatted))
            self.timestamp_end = int(datetime.datetime.timestamp(self.ending_formatted))
            self.nearestvalue_start = self.climate_unixdata[min(range(len(self.climate_unixdata)), key=lambda i: abs(self.climate_unixdata[i] - self.timestamp_start))]
            self.timeentryindex_temp_start = np.where(self.climate_unixdata == self.nearestvalue_start)
            self.timeentryindex_start = self.timeentryindex_temp_start[0][0]
            print('nearest first entry in climatedata:',self.nearestvalue_start, ' at: ', self.timeentryindex_start)
            self.nearestvalue_end = self.climate_unixdata[min(range(len(self.climate_unixdata)), key=lambda i: abs(self.climate_unixdata[i] - self.timestamp_end))]
            self.timeentryindex_temp_end = np.where(self.climate_unixdata == self.nearestvalue_end)
            self.timeentryindex_end = self.timeentryindex_temp_end[0][0]
            print('nearest first entry in climatedata:', self.nearestvalue_end, ' at: ', self.timeentryindex_end)
            self.index_tracker = self.timeentryindex_start
            if self.timeentryindex_end > self.timeentryindex_start:
                self.climate_time_array_tempvalue = datetime.datetime.fromtimestamp(f['compiled_data'][self.index_tracker, 0])
                self.climate_time_array.append(self.climate_time_array_tempvalue.strftime('%Y-%m-%d_%Hh'))
                self.climate_temp_array.append(f['compiled_data'][self.index_tracker, 1])
                self.climate_humidity_array.append(f['compiled_data'][self.index_tracker, 2])
                self.climate_baro_array.append((f['compiled_data'][self.index_tracker, 3]))
                self.data_temp_array.append(f['compiled_data'][self.index_tracker, 5])
                self.data_humidity_array.append(f['compiled_data'][self.index_tracker, 6])
                self.data_baro_array.append(f['compiled_data'][self.index_tracker, 7])
                self.index_tracker += 1
            f.close()


    def dotheplot(self, namefile_, rangeoftick):
        rangeofint = int(rangeoftick)
        location_f = './home/climatedata/plots/' + namefile_

        # Sets figure size in inches
        fig = plt.figure(figsize=(8, 10))

        ax = fig.add_subplot(3, 1, 1)
        ax.scatter(self.climate_time_array, self.climate_temp_array, s=3, color=[0,0,0], label='weather station')
        ax.scatter(self.climate_time_array, self.data_temp_array, s=3, color=[0, 0, 255], label='room3507')
        # Here we set x and y labels as strings, they can be whatever you want them to be
        ax.set_xlabel('Time')
        ax.set_ylabel('Temp oC')


        # Here we eliminate the top and righthand parts of the box enclosing the figure
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')
        ax.xaxis.set_tick_params(rotation=45)

        tempaxis1 = ax.xaxis.get_ticklabels()
        tempaxis1 = list(set(tempaxis1) - set(tempaxis1[::rangeofint]))
        for label in tempaxis1:
            label.set_visible(False)

        bx = fig.add_subplot(3, 1, 2)
        bx.scatter(self.climate_time_array, self.climate_humidity_array, s=3, color=[0, 0, 0], label='weather station')
        bx.scatter(self.climate_time_array, self.data_humidity_array, s=3, color=[0, 0, 255], label='room3507')
        #Here we set x and y labels as strings, they can be whatever you want them to be
        bx.set_xlabel('Time')
        bx.set_ylabel('% Humidity')
        #Here we eliminate the top and righthand parts of the box enclosing the figure
        bx.spines['right'].set_visible(False)
        bx.spines['top'].set_visible(False)
        bx.yaxis.set_ticks_position('left')
        bx.xaxis.set_ticks_position('bottom')
        bx.xaxis.set_tick_params(rotation=45)

        tempaxis2 = bx.xaxis.get_ticklabels()
        tempaxis2 = list(set(tempaxis2) - set(tempaxis2[::rangeofint]))
        for label in tempaxis2:
            label.set_visible(False)

        dx = fig.add_subplot(3, 1, 2)
        dx.scatter(self.climate_time_array, self.climate_baro_array, s=3, color=[0, 0, 0], label='weather station')
        dx.scatter(self.climate_time_array, self.data_baro_array, s=3, color=[0, 0, 255], label='room3507')
        #Here we set x and y labels as strings, they can be whatever you want them to be
        dx.set_xlabel('Time')
        dx.set_ylabel('Pressure kPa')
        #Here we eliminate the top and righthand parts of the box enclosing the figure
        dx.spines['right'].set_visible(False)
        dx.spines['top'].set_visible(False)
        dx.yaxis.set_ticks_position('left')
        dx.xaxis.set_ticks_position('bottom')
        dx.xaxis.set_tick_params(rotation=45)

        tempaxis3 = dx.xaxis.get_ticklabels()
        tempaxis3 = list(set(tempaxis3) - set(tempaxis3[::rangeofint]))
        for label in tempaxis3:
            label.set_visible(False)

        plt.legend(loc='lower left')
        plt.show()
        fig.savefig(location_f, tight_layout = True)

####### PROGRAM #########

#input the date ragne and interval

gotime = rangeuserinput()
first_day, last_day, tick_interval = gotime.definedtime()

#pull the data from the dataset
pull_data_and_plot = findandplot()
pull_data_and_plot.reporting_dataset(first_day, last_day)
nameoftheplotfile= 'plot_' + first_day + '_to_' + last_day + ',hdf5'
pull_data_and_plot.dotheplot(nameoftheplotfile, tick_interval)

