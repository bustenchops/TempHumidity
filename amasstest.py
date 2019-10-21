import datetime
import time
import os
import h5py
import threading
import numpy as np
import matplotlib.pyplot as plt
import glob



class amassdata():

    def __init__(self):
        self.delta_j = datetime.timedelta(days=4)
        self.time_j = datetime.datetime.now() - self.delta_j

    def joina(self, settype):
        self.timepan = settype
        self.dest_j = '/home/pi/data/'
        self.daily_j = self.dest_j + 'daily/'
        self.dailyplot_j = self.dest_j + 'dailyplot/'
        self.weeklyplot_j = self.dest_j + 'weeklyplot/'
        self.monthlyplot_j = self.dest_j + 'monthlyplot/'
        self.yearlyplot_j = self.dest_j + 'yearlyplot/'

        if self.timepan == 'weekly':
            self.year_j = datetime.date.strftime(self.time_j, '%Y')
            self.week_j = datetime.date.strftime(self.time_j, '%U')
            quickname = self.daily_j + self.year_j + '*-week_' + self.week_j + '.hdf5'
            self.name_j = datetime.date.strftime(self.time_j, '%Y-week_%U_data.hdf5')
            self.filename_ = self.weeklyplot_j + self.name_j
            self.glob_data = glob.glob(quickname)

        if self.timepan == 'monthly':
            self.year_j = datetime.date.strftime(self.time_j, '%Y')
            self.month_j = datetime.date.strftime(self.time_j, '%m')
            quickname = self.daily_j + self.year_j + '-' + self.month_j + '*.hdf5'
            self.name_j = datetime.date.strftime(self.time_j, '%Y-%m_data.hdf5')
            self.filename_ = self.monthlyplot_j + self.name_j
            self.glob_data = glob.glob(quickname)

        if self.timepan == 'yearly':
            self.year_j = datetime.date.strftime(self.time_j, '%Y')
            quickname = self.daily_j + self.year_j + '*.hdf5'
            self.name_j = datetime.date.strftime(self.time_j, '%Y_data.hdf5')
            self.filename_ = self.yearlyplot_j + self.name_j
            self.glob_data = glob.glob(quickname)

        with h5py.File(self.filename_, 'a') as i:
            dt = np.dtype('i4')
            dataforday_ = i.create_group('dailydata')
            datatemp_stamp_ = dataforday_.create_dataset('temperature_C', shape=(1, 2), maxshape=(None, 2), dtype=dt)
            datahumid_stamp = dataforday_.create_dataset('humidity', shape=(1, 2), maxshape=(None, 2), dtype=dt)
            i.close()

        self.spac_ = 0

        for k in self.glob_data:
            with h5py.File(k, 'a') as g:
                self.num_timestamp = len(g['dailydata/temperature_C'])
                self.datset1 = g.get('dailydata/temperature_C')
                self.allvals1 = np.array(self.datset1)
                self.x1 = self.allvals1[:, 0]
                self.y1 = self.allvals1[:, 1]
                self.datset2 = g.get('dailydata/humidity')
                self.allvals2 = np.array(self.datset2)
                self.x2 = self.allvals2[:, 0]
                self.y2 = self.allvals2[:, 1]
                g.close()

                with h5py.File(self.filename_, 'a') as h:
                    h['dailydata/temperature_C'].resize((h['dailydata/temperature_C'].shape[0] + self.num_timestamp, h['dailydata/temperature_C'].shape[1]))
                    h['dailydata/humidity'].resize((h['dailydata/humidity'].shape[0] + self.num_timestamp, h['dailydata/humidity'].shape[1]))

                    for w in range(self.num_timestamp):
                        h['dailydata/temperature_C'][self.spac_, 0] = self.x1[w]
                        h['dailydata/temperature_C'][self.spac_, 1] = self.y1[w]
                        h['dailydata/humidity'][self.spac_, 0] = self.x2[w]
                        h['dailydata/humidity'][self.spac_, 1] = self.y2[w]
                        self.spac_ = self.spac_ + 1
                        self.size_final = len(h['dailydata/temperature_C'])
                    h.close()


r = amassdata()
r.joina('weekly')
