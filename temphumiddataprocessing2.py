import datetime
import time
import os
import h5py
import numpy as np
import matplotlib.pyplot as plt
import glob
from dateutil.relativedelta import relativedelta

#DHT22 version

class rangeuserinput():

    def __init__(self):
        self.periodinput = None
        self.yearinput = None
        self.monthone = None
        self.monthtwo = None
        self.dayrange = None
        self.tickrange = None

    def definedtime(self):
        print('Indicate the period you what to process:')
        self.periodinput = input('(y) = year , (m) = sinlge or multiple months, (d) = span of days')
        return (self.periodinput)

    def defineyear(self):
        self.yearinput = input('What year?')
        print('Entered ' + self.yearinput)
        return(self.yearinput)

    def definemonths(self):
        if self.periodinput == 'm':
            print('Multiple months selected in year ' + self.yearinput)
            self.monthone = input('Starting month (numerical format)?')
            self.monthtwo = input('How many months to report?')
            print('Reporting from month ' + self.monthone + ' spanning ' + self.monthtwo + ' months')

        if self.periodinput == 'd':
             print('Day range selected in year ' + self.yearinput)
             self.monthone = input('Which month (numerical format)?')
             self.monthtwo = input('What day to start at?')
             print('Starting at month ' + self.monthone + ' day ' + self.monthtwo)

        return(self.monthone, self.monthtwo)

    def definedayrange(self):
        self.dayrange = input('How many days to span?')

        return(self.dayrange)

    def tickrangeinput(self):
        self.tickrange = input('Time between tick labels (in hours)?')

        return (self.tickrange)

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
        self.startm = datetime.datetime.strptime(self.multidateone, '%Y %m')
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

    def dayset(self, monthin, dayin, spanin):
        self.extraday = int(spanin)
        self.multiarray = []
        self.multidateone = self.yearinput  + ' ' + monthin + ' ' + dayin
        self.startm = datetime.datetime.strptime(self.multidateone, '%Y %m %d')
        self.delta_min = datetime.timedelta(seconds=1)
        self.startday = self.startm - self.delta_min
        self.endday = self.startm + relativedelta(days =+ self.extraday)
        print(self.startday)
        print(self.endday)
        for hdf5file in self.yeararray:
            head, tail = os.path.split(hdf5file)
            names, ext = os.path.splitext(tail)
            namedateobj = datetime.datetime.strptime(names, '%Y-%m-%d-week_%U')
            if namedateobj > self.startday and namedateobj < self.endday:
                self.multiarray.append(tail)
                self.multiarray.sort()
        print(self.multidateone)
        print(self.multiarray)

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

    def dotheplot(self, namefile_, nameplot, rangeoftick):
        rangeofint = int(rangeoftick)
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
        fig = plt.figure(figsize=(24, 28))

        ax = fig.add_subplot(2, 1, 1)
        ax.scatter(self.nptime2, self.ytemp, s=3, color=[0,0,0])
        # Here we set x and y labels as strings, they can be whatever you want them to be
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

        bx = fig.add_subplot(2, 1, 2)
        bx.scatter(self.nptime2, self.yhumid, s=3)
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
        plt.show()
        fig.savefig(location_p, tight_layout = True)

gotime = rangeuserinput()
rangereturn = gotime.definedtime()
yearreturn = gotime.defineyear()

if rangereturn == 'y':
    tickrange_ = gotime.tickrangeinput()
    yearfiles = findandplot()
    yearfiles.yearfileset(yearreturn)
    nameyf = yearreturn + '_data.hdf5'
    nameyp = yearreturn + '_plot.pdf'
    yearfiles.assimilate(nameyf)
    yearfiles.dotheplot(nameyf, nameyp, tickrange_)

if rangereturn == 'm':
    monthonereturn, monthtworeturn = gotime.definemonths()
    tickrange_ = gotime.tickrangeinput()
    yearfiles = findandplot()
    yearfiles.yearfileset(yearreturn)
    yearfiles.multifileset(monthonereturn, monthtworeturn)
    nameyf = yearreturn + "_starting at_" + monthonereturn + "_spanning_" + monthtworeturn + "_months_data.hdf5"
    nameyp = yearreturn + "_starting at_" + monthonereturn + "_spanning_" + monthtworeturn + "_months_plot.pdf"
    yearfiles.assimilate(nameyf)
    yearfiles.dotheplot(nameyf, nameyp, tickrange_)

if rangereturn == 'd':
    monthonereturn, monthtworeturn = gotime.definemonths()
    spanningtime = gotime.definedayrange()
    tickrange_ = gotime.tickrangeinput()
    yearfiles = findandplot()
    yearfiles.yearfileset(yearreturn)
    yearfiles.dayset(monthonereturn, monthtworeturn, spanningtime)
    nameyf = yearreturn + "_starting at_" + monthonereturn + "_" + monthtworeturn  + "_spanning_" + spanningtime + "_days_data.hdf5"
    nameyp = yearreturn + "_starting at_" + monthonereturn + "_" + monthtworeturn  + "_spanning_" + spanningtime + "_days_data.pdf"
    yearfiles.assimilate(nameyf)
    yearfiles.dotheplot(nameyf, nameyp, tickrange_)
