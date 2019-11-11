import datetime
import time
import os
import h5py
import numpy as np
import matplotlib.pyplot as plt
import glob


class storedata():

    def __init__(self):
        self.delta = datetime.timedelta(days=1)
        self.dest = '/home/pi/data/'
# self.daily = self.dest + 'daily'
        self.daily_ = self.dest + 'daily/'
# self.dailyplot = self.dest + 'dailyplot'
        self.dailyplot_ = self.dest + 'dailyplot/'
# self.weeklyplot = self.dest + 'weeklyplot'
        self.weeklyplot_ = self.dest + 'weeklyplot/'
# self.monthlyplot = self.dest + 'monthlyplot'
        self.monthlyplot_ = self.dest + 'monthlyplot/'
# self.yearlyplot = self.dest + 'yearlyplot'
        self.yearlyplot_ = self.dest + 'yearlyplot/'
        self.time_ = datetime.datetime.now() - self.delta
        print(self.time_)
        self.year_ = datetime.date.strftime(self.time_, '%Y')
        print(self.year_)
        self.month_ = datetime.date.strftime(self.time_, '%m')
        print(self.month_)
        self.week_ = datetime.date.strftime(self.time_, '%U')
        print(self.week_)
        self.filedate = datetime.date.strftime(self.time_, '%Y-%m-%d')
        self.filedate_ = self.filedate + ".hdf5"

    def movedaily(self):
        fileglob = glob.glob('*.hdf5')
        if os.path.exists(self.daily_):
            print('daily directory exists')
# todaytemp = datetime.datetime.now().strftime("%Y-%m-%d")
# todaytime = datetime.datetime.strptime(todaytemp, "%Y-%m-%d")
            for i in fileglob:
                names, ext = os.path.splitext(i)
                namedateobj = datetime.datetime.strptime(names, '%Y-%m-%d-week_%U')
# if namedateobj < todaytime:
# print(todaytime)
# print("good")
# print(i)
                os.system('mv /home/pi/' + i + ' /home/pi/data/')

        else:
            os.makedirs(self.daily_)
            for i in fileglob:
                names, ext = os.path.splitext(i)
                namedateobj = datetime.datetime.strptime(names, '%Y-%m-%d-week_%U')
# if namedateobj < todaytime:
# print(todaytime)
# print("good")
# print(i)
                os.system('mv /home/pi/' + i + ' /home/pi/data/')

    def checkmake(self, epochs_):
        self.epoch_ = epochs_

        if self.epoch_ == 'daily':
            if os.path.exists(self.dailyplot_):
                print('daily plot directory exists')
            else:
                os.makedirs(self.dailyplot_)

        if self.epoch_ == 'weekly':
            if os.path.exists(self.weeklyplot_): #  + self.year_ + '/week_' + self.week_):
                print('weekly plot directory exists')
            else:
                os.makedirs(self.weeklyplot_) #  + self.year_ + '/week_' + self.week_)

        if self.epoch_ == 'monthly':
            if os.path.exists(self.monthlyplot_ ): # + self.year_ + '/month_' + self.month_):
                print('montly plot directory exists')
            else:
                os.makedirs(self.monthlyplot_) # + self.year_ + '/month_' + self.month_)

        if self.epoch_ == 'yearly':
            if os.path.exists(self.yearlyplot_): #  + self.year_):
                print('yearly plot directory exists')
            else:
                os.makedirs(self.yearlyplot_) #  + self.year_)


# test excution code
# gotime = storedata()
# gotime.movedaily()
# gotime.checkmake('daily')
# gotime.checkmake('weekly')
# gotime.checkmake('monthly')
# gotime.checkmake('yearly')


# ############# use glob to agregate the data into one file ###########
class amassdata():

    def __init__(self):
        self.dest_j = '/home/pi/data/'
        self.daily_j = self.dest_j + 'daily/'
        self.dailyplot_j = self.dest_j + 'dailyplot/'
        self.weeklyplot_j = self.dest_j + 'weeklyplot/'
        self.monthlyplot_j = self.dest_j + 'monthlyplot/'
        self.yearlyplot_j = self.dest_j + 'yearlyplot/'
        fileglob = glob.glob('*.hdf5')
# self.delta_j = datetime.timedelta(days=4)
# self.time_j = datetime.datetime.now() - self.delta_j

    def joina(self, settype):
        self.timepan = settype

        if self.timepan == 'weekly':
# self.year_j = datetime.date.strftime(self.time_j, '%Y')
# self.week_j = datetime.date.strftime(self.time_j, '%U')
            quickname_w = self.dest_j + self.year_j + '*-week_' + self.week_j + '.hdf5'
            self.name_j = datetime.date.strftime(self.time_j, '%Y-week_%U_data.hdf5')
            self.filename_ = self.weeklyplot_j + self.name_j
            self.glob_data = glob.glob(quickname_w)

        if self.timepan == 'monthly':
# self.year_j = datetime.date.strftime(self.time_j, '%Y')
# self.month_j = datetime.date.strftime(self.time_j, '%m')
            quickname_m = self.dest_j + self.year_j + '-' + self.month_j + '*.hdf5'
            self.name_j = datetime.date.strftime(self.time_j, '%Y-%m_data.hdf5')
            self.filename_ = self.monthlyplot_j + self.name_j
            self.glob_data = glob.glob(quickname_m)

        if self.timepan == 'yearly':
# self.year_j = datetime.date.strftime(self.time_j, '%Y')
            quickname_y = self.dest_j + self.year_j + '*.hdf5'
            self.name_j = datetime.date.strftime(self.time_j, '%Y_data.hdf5')
            self.filename_ = self.yearlyplot_j + self.name_j
            self.glob_data = glob.glob(quickname_y)

        with h5py.File(self.filename_, 'a') as i:
            dt = np.dtype('i4')
            dataforday_ = i.create_group('dailydata')
            datatemp_stamp_ = dataforday_.create_dataset('temperature_C', shape=(1, 2), maxshape=(None, 2), dtype=dt)
            datahumid_stamp = dataforday_.create_dataset('humidity', shape=(1, 2), maxshape=(None, 2), dtype=dt)
            i.close()

        self.spac_ = 0

        for i in self.glob_data:
            with h5py.File(i, 'a') as g:
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


# r = amassdata()
# r.joina('monthly')

# ########## make the plots and save them #############################
class letsplot():
    def __init__(self):
        self.delta_plot = datetime.timedelta(days=1)
        self.time_plot = datetime.datetime.now() - self.delta_plot


    def plotprep(self, plotdate):
        self.timespan = plotdate

        if self.timespan is 'daily':
            self.glob_data_ = None
            self.day_data = datetime.date.strftime(self.time_plot, '%d')
            self.month_data = datetime.date.strftime(self.time_plot, '%m')
            self.year_data = datetime.date.strftime(self.time_plot, '%Y')
            fastname = '/home/pi/data/daily/' + self.year_data + '-' + self.month_data + '-' + self.day_data + '*.hdf5'

            self.glob_data_ = glob.glob(fastname)
            self.name_data = '/home/pi/data/dailyplot/' + datetime.date.strftime(self.time_plot, 'plot_%Y-%m-%d-week_%U.hdf5')
            self.name_dataparse = '/home/pi/data/dailyplot/' + datetime.date.strftime(self.time_plot, 'plot_%Y-%m-%d-week_%U.pdf')
            self.plotit(self.name_dataparse)

        if self.timespan is 'weekly':
            self.glob_data_ = None
            self.week_data = datetime.date.strftime(self.time_plot, '%U')
            self.month_data = datetime.date.strftime(self.time_plot, '%m')
            self.year_data = datetime.date.strftime(self.time_plot, '%Y')
            fastname = '/home/pi/data/weeklyplot/' + self.year_data + '*' + self.week_data + '*.hdf5'
            self.glob_data_ = glob.glob(fastname)
            self.name_data = '/home/pi/data/weeklyplot/' + datetime.date.strftime(self.time_plot, 'plot_%Y-week_%U.hdf5')
            self.name_dataparse = '/home/pi/data/weeklyplot/' + datetime.date.strftime(self.time_plot, 'plot_%Y-week_%U.pdf')
            self.plotit(self.name_dataparse)

        if self.timespan is 'monthly':
            self.glob_data_ = None
            self.month_data = datetime.date.strftime(self.time_plot, '%m')
            self.year_data = datetime.date.strftime(self.time_plot, '%Y')
            fastname = '/home/pi/data/monthlyplot/' + self.year_data + '-' +  self.month_data + '*.hdf5'
            self.glob_data_ = glob.glob(fastname)
            self.name_data = '/home/pi/data/monthlyplot/' + datetime.date.strftime(self.time_plot, 'plot_%Y-%m.hdf5')
            self.name_dataparse = '/home/pi/data/monthlyplot/' + datetime.date.strftime(self.time_plot, 'plot_%Y-%m.pdf')
            self.plotit(self.name_dataparse)

        if self.timespan is 'yearly':
            self.glob_data_ = None
            self.year_data = datetime.date.strftime(self.time_plot, '%Y')
            fastname = '/home/pi/data/yearlyplot/' + self.year_data + '*.hdf5'
            self.glob_data_ = glob.glob(fastname)
            self.name_data = '/home/pi/data/yearlyplot/' + datetime.date.strftime(self.time_plot, 'plot_%Y.hdf5')
            self.name_dataparse = '/home/pi/data/yearlyplot/' + datetime.date.strftime(self.time_plot, 'plot_%Y.pdf')
            self.plotit(self.name_dataparse)

    def plotit(self, fname_plot):
        for o in self.glob_data_:
            print('working on glob')
            with h5py.File(o, 'a') as k:
                self.num_timestamp = len(k['dailydata/temperature_C'])
                self.datset1a = k.get('dailydata/temperature_C')
                self.allvals1a = np.array(self.datset1a)
                self.x1a = self.allvals1a[:, 0]
                self.y1a = self.allvals1a[:, 1]
                self.datset2a = k.get('dailydata/humidity')
                self.allvals2a = np.array(self.datset2a)
                self.y2a = self.allvals2a[:, 1]
                # self.npx1a = np.array(self.x1a)
                self.npx1a = np.array(self.x1a, dtype='int')
                # self.npx1a = np.array(self.x1a, dtype='U25')

                self.npstrx1a = np.array(self.x1a, dtype='U25')
            for a in range(len(self.x1a)):
                # print(self.npx1a[a])
                self.npstrx1a[a] = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime(self.npx1a[a]))
                # print(self.npstrx1a)

            fig = plt.figure(figsize=(8, 8))
            # Sets figure size in inches
            ax = fig.add_subplot(2, 1, 1)
            ax.plot(self.npstrx1a, self.y1a, color=[0, 0, 0])
            # Plots vectors x vs y; they must have the same dimension. I also put in a color argument (rgb).

            # Here we will set the x and y limits
            # ax.set_xlim([0, 1])
            # ax.set_ylim([0, 1])

            # Here we set x and y labels as strings, they can be whatever you want them to be
            # ax.set_xlabel('Time')
            # ax.set_ylabel('Temp oC')

            # Here we eliminate the top and righthand parts of the box enclosing the figure
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.yaxis.set_ticks_position('left')
            ax.xaxis.set_ticks_position('bottom')

            ax = fig.add_subplot(2, 1, 2)
            ax.plot(self.npstrx1a,self.y2a, color = [0, 0, 0]) #Plots vectors x vs y; they must have the same dimension. I also put in a color argument (rgb).

            #Here we will set the x and y limits
            # ax.set_xlim([0, 1])
            # ax.set_ylim([0, 1])

            #Here we set x and y labels as strings, they can be whatever you want them to be
            ax.set_xlabel('Time')
            ax.set_ylabel('% Humidity')

            #Here we eliminate the top and righthand parts of the box enclosing the figure
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.yaxis.set_ticks_position('left')
            ax.xaxis.set_ticks_position('bottom')


            #Save the figure
            fig.savefig(fname_plot, tight_layout = True)


# test excution code
# gotime = letsplot()
# gotime.plotprep('yearly')

# #################___PROGRAM__################################3_
while True:
    try:
        datars = getdata()
        temptemp, temphumidy = datars.doit() #get time and the temp/umhidity data
        print('temp reading is')
        print(temptemp)
        print('humidity reading is')
        print(temphumidy)
        timestamp_ = datars.stringtime()  # recall temp/humidity data
        filedate = datars.dates()  # process epoch for date
        filenamealpha = filedate + ".hdf5"  # make the date filename
        tickytock = datars.ticktock() #get fullepoch for timerthread

        hd5file(filenamealpha, timestamp_, temptemp, temphumidy)

        waittime_ = countdown()
        waittime_.timerthreadinit(3600, tickytock)
        waittime_.timerthread.join()
        first_date = datars.date_recall()
        next_date = datars.dating()

        week_data1 = datetime.date.strftime(first_date, '%U')
        month_data1 = datetime.date.strftime(first_date, '%m')
        year_data1 = datetime.date.strftime(first_date, '%Y')
        day_data1 = datetime.date.strftime(first_date, '%d')

        week_data2 = datetime.date.strftime(next_date, '%U')
        month_data2 = datetime.date.strftime(next_date, '%m')
        year_data2 = datetime.date.strftime(next_date, '%Y')
        day_data2 = datetime.date.strftime(next_date, '%d')

        if day_data2 > day_data1:
            dailystore = storedata()
            dailystore.movedaily()
            dailystore.checkmake('daily')
            gatherit = amassdata()
            # gatherit.joina('daily')
            plotprep_ = letsplot()
            plotprep_.plotprep('daily')
            if week_data2 > week_data1:
                dailystore.checkmake('weekly')
                gatherit.joina('weekly')
                plotprep_.plotprep('weekly')
                if month_data2 > month_data1:
                    dailystore.checkmake('monthly')
                    gatherit.joina('monthly')
                    plotprep_.plotprep('monthly')
                    if year_data2 > year_data1:
                        dailystore.checkmake('yearly')
                        gatherit.joina('yearly')
                        plotprep_.plotprep('yearly')
            os.system('rclone copy /home/pi/data Gdrive:/data')
            datars.save_date()

    except (KeyboardInterrupt, SystemExit):
        print ('keyboardinterrupt found!')
        print ('...Program Stopped Manually!')
        raise
    except:
        print('stop!')
        raise
