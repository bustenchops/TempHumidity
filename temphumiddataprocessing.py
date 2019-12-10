import datetime
import time
import os
import h5py
import numpy as np
import matplotlib.pyplot as plt
import glob
from dateutil.relativedelta import relativedelta

class rangeuserinput():

    def __init__(self):
        self.periodinput = None
        self.yearinput = None
        self.monthone = None
        self.monthtwo = None

    def definedtime(self):
        print('Indicate the period you what to process:')
        self.periodinput = input('(y) = year , (m) = sinlge or multiple months')
        return (self.periodinput)

    def defineyear(self):
        print('Year or multiple months selected')
        self.yearinput = input('What year?')
        print('Entered ' + self.yearinput)
        return(self.yearinput)

    def definemonths(self):
        if self.periodinput == 'm':
            print('Multiple months selected in year ' + self.yearinput)
            self.monthone = input('Starting month (numerical format)?')
            self.monthtwo = input('How many months to report?')
            print('Reporting from month ' + self.monthone + ' spanning ' + self.monthtwo + ' months')

        # if self.periodinput == 'm':
        #     print('Single month selected in year ' + self.yearinput)
        #     print('Month selected')
        #     self.monthone = input('Which month (numerical format)?')
        #     self.monthtwo = 13
        #     print('Entered ' + self.monthone)

        return(self.monthone, self.monthtwo)

class findandplot():

    def __init__(self):
        self.startlocation = '/home/pi/'
        self.yeararray = []
        self.multiarray = []

    def yearfileset(self, yearinput_):
        self.yeararray = []
        self.yearinput = yearinput_
        print(self.yearinput)
        self.yfileset = [file for file in glob.glob(self.startlocation + '*' + yearinput_ + '*.hdf5')]
        self.yfileset.sort()
        for file in self.yfileset:
            head, tail = os.path.split(file)
            self.yeararray.append(tail)
            self.multiarray.append(tail)
        print(self.yeararray)

    def multifileset(self, firstmonth, lastmonth):
        self.extramonth = int(lastmonth)
        self.multiarray = []
        self.multidateone = self.yearinput  + ' ' + firstmonth
        # self.multidatetwo = self.yearinput  + ' ' + lastmonth
        self.startm = datetime.datetime.strptime(self.multidateone, '%Y %m')
        # self.endm = datetime.datetime.strptime(self.multidatetwo, '%Y %m')
        self.delta_min = datetime.timedelta(seconds=1)
        self.startmonth = self.startm - self.delta_min
        self.endmonth = self.startm + relativedelta(months =+ self.extramonth)
        print(self.startmonth)
        print(self.endmonth)
        for hdf5file in self.yeararray:
            head, tail = os.path.split(hdf5file)
            names, ext = os.path.splitext(tail)
            namedateobj = datetime.datetime.strptime(names, '%Y-%m-%d-week_%U')
            if namedateobj > self.startmonth and namedateobj < self.endmonth:
                self.multiarray.append(tail)
                self.multiarray.sort()
        print(self.multidateone)
        print(self.multiarray)

    # def monofileset(self, onlymonth):
    #     self.multidateone = self.yearinput  + ' ' + onlymonth
    #     self.startm = datetime.datetime.strptime(self.multidateone, '%Y %m')
    #     self.endm = datetime.datetime.strptime(self.multidateone, '%Y %m')
    #     self.delta_min = datetime.timedelta(seconds=1)
    #     self.startmonth = self.startm - self.delta_min
    #     self.endmonth = self.endm + relativedelta(months=+1)
    #     print(self.startmonth)
    #     print(self.endmonth)
    #     for hdf5file in self.yeararray:
    #         head, tail = os.path.split(hdf5file)
    #         names, ext = os.path.splitext(tail)
    #         namedateobj = datetime.datetime.strptime(names, '%Y-%m-%d-week_%U')
    #         if namedateobj > self.startmonth and namedateobj < self.endmonth:
    #             self.multiarray.append(tail)
    #             self.multiarray.sort()
    #     print(self.multidateone)
    #     print(self.multiarray)

    def assimilate(self, namefile):
        locationone_ = '/home/pi/data/' + namefile
        with h5py.File(locationone_, 'a') as j:
            dt = np.dtype('i4')
            dataforday_ = j.create_group('dailydata')
            datatemp_stamp_ = dataforday_.create_dataset('temperature_C', shape=(1, 2), maxshape=(None, 2), dtype=dt)
            datahumid_stamp = dataforday_.create_dataset('humidity', shape=(1, 2), maxshape=(None, 2), dtype=dt)
            j.close()

        self.spac_ = 0

        for i in self.multiarray:
            location_ = '/home/pi/' + i
            with h5py.File(location_, 'a') as g:
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

                with h5py.File(locationone_, 'a') as h:
                    h['dailydata/temperature_C'].resize((h['dailydata/temperature_C'].shape[0] + self.num_timestamp, h['dailydata/temperature_C'].shape[1]))
                    h['dailydata/humidity'].resize((h['dailydata/humidity'].shape[0] + self.num_timestamp, h['dailydata/humidity'].shape[1]))

                    for w in range(self.num_timestamp):
                        h['dailydata/temperature_C'][self.spac_, 0] = self.x1[w]
                        h['dailydata/temperature_C'][self.spac_, 1] = self.y1[w]
                        h['dailydata/humidity'][self.spac_, 0] = self.x2[w]
                        h['dailydata/humidity'][self.spac_, 1] = self.y2[w]
                        self.spac_ = self.spac_ + 1
                        self.size_final = len(h['dailydata/temperature_C'])
                        print(self.spac_)
                    h.close()
                print('file done')
        print('D-U-N....Done')

    def dotheplot(self, namefile_, nameplot):
        location_f = '/home/pi/data/' + namefile_
        location_p = '/home/pi/data/' + nameplot
        with h5py.File(location_f, 'a') as k:
            self.numberslots = len(k['dailydata/temperature_C'])
            self.tempdata = k.get('dailydata/temperature_C')
            self.allvaluestemp = np.array(self.tempdata)
            self.xtemp = self.allvaluestemp[:, 0]
            self.ytemp = self.allvaluestemp[:, 1]
            self.humiddata = k.get('dailydata/humidity')
            self.allvalueshumid = np.array(self.humiddata)
            self.yhumid = self.allvalueshumid[:, 1]
            self.nptime = np.array(self.xtemp, dtype='int')
            self.nptime2 = np.array(self.xtemp, dtype='U25')

        for a in range(len(self.nptime2)):
            self.nptime2[a] = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime(self.nptime[a]))

        # Sets figure size in inches
        fig = plt.figure(figsize=(8, 8))

        ax = fig.add_subplot(2, 1, 1)
        plt.scatter(self.nptime2, self.ytemp, color=[0,0,0])
        # Here we set x and y labels as strings, they can be whatever you want them to be
        ax.set_ylabel('Temp oC')
        # Here we eliminate the top and righthand parts of the box enclosing the figure
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')
        ax = fig.add_subplot(2, 1, 2)
        ax.scatter(self.nptime2, self.yhumid)
        #Here we set x and y labels as strings, they can be whatever you want them to be
        ax.set_xlabel('Time')
        ax.set_ylabel('% Humidity')
        #Here we eliminate the top and righthand parts of the box enclosing the figure
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')

        tempaxis = ax.xaxis.get_ticklabels()
        tempaxis = list(set(tempaxis) - set(tempaxis[::7]))
        for label in tempaxis:
            label.set_visible(False)
        plt.show()
        fig.savefig(location_p, tight_layout = True)

gotime = rangeuserinput()
rangereturn = gotime.definedtime()
yearreturn = gotime.defineyear()

if rangereturn == 'y':
    yearfiles = findandplot()
    yearfiles.yearfileset(yearreturn)
    nameyf = yearreturn + '_data.hdf5'
    nameyp = yearreturn + '_plot.pdf'
    yearfiles.assimilate(nameyf)
    yearfiles.dotheplot(nameyf, nameyp)

if rangereturn == 'm':
    monthonereturn, monthtworeturn = gotime.definemonths()
    yearfiles = findandplot()
    yearfiles.yearfileset(yearreturn)
    yearfiles.multifileset(monthonereturn, monthtworeturn)
    nameyf = yearreturn + "_starting at_" + monthonereturn + "_spanning_" + monthtworeturn + "_months_data.hdf5"
    nameyp = yearreturn + "_starting at_" + monthonereturn + "_spanning_" + monthtworeturn + "_months_plot.pdf"
    yearfiles.assimilate(nameyf)
    yearfiles.dotheplot(nameyf, nameyp)

# if rangereturn == 'm':
#     monthonereturn, monthtworeturn = gotime.definemonths()
#     yearfiles = findandplot()
#     yearfiles.yearfileset(yearreturn)
#     yearfiles.monofileset(monthonereturn)
#     nameyf = yearreturn + "-" + monthonereturn +  "_data.hdf5"
#     nameyp = yearreturn + "-" + monthonereturn +  "_plot.pdf"
#     yearfiles.assimilate(nameyf)
#     yearfiles.dotheplot(nameyf, nameyp)
