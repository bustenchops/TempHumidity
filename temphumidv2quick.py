import datetime
import time
import os
import h5py
import threading
import numpy as np
import matplotlib.pyplot as plt
import glob
import pigpio
import DHT22


# #################### make the hdf5 data and get the data ################
class getdata():  # get required data in 1 call
    def __init__(self):
        self.pi = pigpio.pi()
        self.sampledata = DHT22.sensor(self.pi, 4)
        print('start the sensor')
        print('trigger')
        #time.sleep(2)
        self.sampledata.trigger()
        time.sleep(2)
        print('trigger')
        self.sampledata.trigger()
        self.current = time.time()
        self.tempdata = '{:3.2f}'.format(self.sampledata.temperature() / 1.)
        self.humidata = '{:3.2f}'.format(self.sampledata.humidity() /1.)
        # self.sampledata.cancel()
        # self.pi.stop()

    def doit(self):
        ttt = float(self.tempdata)
        hhh = float(self.humidata)
        return hhh, ttt

# parse out the timestamp from the data and return it to be used in hd5 file
    # def times(self):
    #     currenttime = self.current - self.twentynineteen
    #     return currenttime

    def stringtime(self):
        goodtimestring = int(self.current)
        print(goodtimestring)
        return goodtimestring

# parse out the date form the data and return it to be used in the hd5 file
    def dates(self):
        currentdate = time.strftime("%Y-%m-%d-week_%U", time.localtime(self.current))
        return str(currentdate)

# full epoch variable to be used by timer
    def ticktock(self):
        ticktock_ = self.current
        return ticktock_

    def dating(self):
        checktime = datetime.datetime.now()
        return(checktime)

    def save_date(self):
        with open('textsave.txt', 'w') as time_text:
            checktime = datetime.datetime.now()
            checktime_format = datetime.date.strftime(day_data1, '%Y %m %d')
            print(checktime_format)
            time_text.write(checktime_format)
            time_text.close()

    def date_recall(self):
        try:
            os.path.isfile('textsave.txt')
            with open('textsave.txt', 'r') as time_read:
                text = time_read.read()
                recalldate = datetime.datetime.strptime(text, '%Y %m %d')
                time_read.close()
            return recalldate
        except:
            with open('textsave.txt', 'w') as time_text:
                checktime = datetime.datetime.now()
                checktime_format = datetime.date.strftime(checktime, '%Y %m %d')
                print('init of textsave')
                print(checktime_format)

                time_text.write(checktime_format)
                time_text.close()
            return checktime_format
# Function not part of the class but is called in the program immediately after
# the above class
def hd5file(fname, timestamp_s, hdftemp, hdfhumidy):
    try:
        # checks to see if the file already exist - if the file exists open it and determine the size of the range.
        os.path.isfile(fname)
        print('opening file')
        aft = os.path.isfile(fname)
        print(aft)
        with h5py.File(fname, 'a') as f:
            # temptemp = 100
            # temphumidy = 100
            num_timestamp = len(f['dailydata/temperature_C'])
            print(num_timestamp)
            f['dailydata/temperature_C'].resize((f['dailydata/temperature_C'].shape[0] + 1, f['dailydata/temperature_C'].shape[1]))
            f['dailydata/humidity'].resize((f['dailydata/humidity'].shape[0] + 1, f['dailydata/humidity'].shape[1]))
            f['dailydata/temperature_C'][num_timestamp, 0] = timestamp_s
            f['dailydata/temperature_C'][num_timestamp, 1] = hdftemp
            f['dailydata/humidity'][num_timestamp, 0] = timestamp_s
            f['dailydata/humidity'][num_timestamp, 1] = hdfhumidy
            print('closing file')
            f.close()
    except:
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

class countdown():
    # timer class initiallizes the variables and sets up a true/false scenario
    # for time. Compares newly aquired time to the datapoint timestamp plus a desired interval
    def __init__(self):
        self.t_start = None
        self.t_delta = None
        self.t_countdown = None

# initializes and starts a thread for the timer accepting the datatimestampe and delay in seconds
# calculates the end time
    def timerthreadinit(self, secon, datatim_):
        self.t_start = datatim_
        self.t_delta = secon
        self.t_countdown = self.t_start + self.t_delta
        self.timerthread = threading.Thread(target=self.threadtimer, args=(self.t_delta, self.t_start))  # argument here is the time in minutes between samples (starting at midnight)
        self.timerthread.start()

    def waittime(self):  # acquires the current time epoch and compares to the datatimestamp
        if self.t_countdown > time.time():
            return True
        elif self.t_countdown <= time.time():
            return False

# while loop that repeatedly checks the wait time and sets the inter-interval check time
    def threadtimer(self, delay_, datatim):
        print('Starting...')
        print('Here we go...')
        while self.waittime() is True:
            print('true')
            time.sleep(2)
        print('it works')

# quick method to print out the variables to see if things are working
# def testoutputs():
#     print(datars)
#     print(timestamp_)
#     print(filedate)
#     print(filenamealpha)

# ####################  sort the data, make the folders and store it is in the right place #####


class storedata():
    # checks to see if the right folders are in place and moves daily files
    # also runs rclone to copy data to grive
    # core from datastorev2

    def __init__(self):
        self.delta = datetime.timedelta(days=1)
        self.dest = '/home/pi/data/'
        self.daily = self.dest + 'daily'
        self.daily_ = self.dest + 'daily/'
        self.dailyplot = self.dest + 'dailyplot'
        self.dailyplot_ = self.dest + 'dailyplot/'
        self.weeklyplot = self.dest + 'weeklyplot'
        self.weeklyplot_ = self.dest + 'weeklyplot/'
        self.monthlyplot = self.dest + 'monthlyplot'
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
        if os.path.exists(self.daily):
            print('exists')
            if os.path.isfile(self.filedate_):
                os.system('mv /home/pi/PIGPIO/*.hdf5 ' + self.daily_)
        else:
            os.makedirs(self.daily)
            if os.path.isfile(self.filedate_):
                os.system('mv /home/pi/PIGPIO/*.hdf5 ' + self.daily_)

    def checkmake(self, epochs_):
        self.epoch_ = epochs_

        if self.epoch_ == 'daily':
            if os.path.exists(self.dailyplot):
                print('exists')
            # put daily plot here
            else:
                os.makedirs(self.dailyplot)
            # put daily plot here
        if self.epoch_ == 'weekly':
            if os.path.exists(self.weeklyplot_): #  + self.year_ + '/week_' + self.week_):
                print('exists')
            # put weekly plot here
            else:
                os.makedirs(self.weeklyplot_) #  + self.year_ + '/week_' + self.week_)
            # put weekly plot here

        if self.epoch_ == 'monthly':
            if os.path.exists(self.monthlyplot_ ): # + self.year_ + '/month_' + self.month_):
                print('exists')
            # put monthly plot here
            else:
                os.makedirs(self.monthlyplot_) # + self.year_ + '/month_' + self.month_)
            # put monthly plot here

        if self.epoch_ == 'yearly':
                    if os.path.exists(self.yearlyplot_): #  + self.year_):
                        print('exists')
            # put yearly plot here
                    else:
                        os.makedirs(self.yearlyplot_) #  + self.year_)
            # put yearly plot here

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
        self.delta_j = datetime.timedelta(days=1)
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
            # os.system('cp -R ' + self.dest_j + self.daily_j + self.year_j + '*-week_' + self.week_j + '.hdf5 /home/pi/data')
            # quickname = self.year_j + '*-week_' + self.week_j + '.hdf5'
            quickname = self.daily_j + self.year_j + '*-week_' + self.week_j + '.hdf5'
            self.name_j = datetime.date.strftime(self.time_j, '%Y-week_%U_data.hdf5')
            self.filename_ = self.weeklyplot_j + self.name_j
            self.glob_data = glob.glob(quickname)

        if self.timepan == 'monthly':
            self.year_j = datetime.date.strftime(self.time_j, '%Y')
            self.month_j = datetime.date.strftime(self.time_j, '%m')
            # os.system('cp -R ' + self.dest_j + self.daily_j + self.year_j + '-' + self.month_j + '*.hdf5 /home/pi/data')
            # quickname = self.year_j + '-' + self.month_j + '*.hdf5'
            quickname = self.daily_j + self.year_j + '-' + self.month_j + '*.hdf5'
            self.name_j = datetime.date.strftime(self.time_j, '%Y-%m_data.hdf5')
            self.filename_ = self.monthlyplot_j + self.name_j
            self.glob_data = glob.glob(quickname)

        if self.timepan == 'yearly':
            self.year_j = datetime.date.strftime(self.time_j, '%Y')
            # os.system('cp -R ' + self.dest_j + self.daily_j + self.year_j + '*.hdf5 /home/pi/data')
            # quickname = self.year_j + '*.hdf5'
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
        # print(self.time_plot)

    def plotprep(self, plotdate):
        self.timespan = plotdate

        if self.timespan is 'daily':
            self.glob_data_ = None
            self.day_data = datetime.date.strftime(self.time_plot, '%d')
            self.month_data = datetime.date.strftime(self.time_plot, '%m')
            self.year_data = datetime.date.strftime(self.time_plot, '%Y')
            fastname = '/home/pi/data/daily/' + self.year_data + '-' + self.month_data + '-' + self.day_data + '*.hdf5'
            # print(fastname)
            self.glob_data_ = glob.glob(fastname)
            self.name_data = '/home/pi/data/dailyplot/' + datetime.date.strftime(self.time_plot, 'plot_%Y-%m-%d-week_%U.hdf5')
            self.name_dataparse = '/home/pi/data/dailyplot/' + datetime.date.strftime(self.time_plot, 'plot_%Y-%m-%d-week_%U.pdf')
            self.plotit(self.name_dataparse)

        if self.timespan is 'weekly':
            self.glob_data_ = None
            # print(self.glob_data_)
            self.week_data = datetime.date.strftime(self.time_plot, '%U')
            self.month_data = datetime.date.strftime(self.time_plot, '%m')
            self.year_data = datetime.date.strftime(self.time_plot, '%Y')
            fastname = '/home/pi/data/weeklyplot/' + self.year_data + '*' + self.week_data + '*.hdf5'
            # print(fastname)
            self.glob_data_ = glob.glob(fastname)
            # print(self.glob_data_)
            self.name_data = '/home/pi/data/weeklyplot/' + datetime.date.strftime(self.time_plot, 'plot_%Y-week_%U.hdf5')
            # print(self.name_data)
            self.name_dataparse = '/home/pi/data/weeklyplot/' + datetime.date.strftime(self.time_plot, 'plot_%Y-week_%U.pdf')
            # print(self.name_dataparse)
            self.plotit(self.name_dataparse)

        if self.timespan is 'monthly':
            self.glob_data_ = None
            self.month_data = datetime.date.strftime(self.time_plot, '%m')
            self.year_data = datetime.date.strftime(self.time_plot, '%Y')
            fastname = '/home/pi/data/monthlyplot/' + self.year_data + '-' +  self.month_data + '*.hdf5'
            # print(fastname)
            self.glob_data_ = glob.glob(fastname)
            # print(self.glob_data_)
            self.name_data = '/home/pi/data/monthlyplot/' + datetime.date.strftime(self.time_plot, 'plot_%Y-%m.hdf5')
            self.name_dataparse = '/home/pi/data/monthlyplot/' + datetime.date.strftime(self.time_plot, 'plot_%Y-%m.pdf')
            self.plotit(self.name_dataparse)

        if self.timespan is 'yearly':
            self.glob_data_ = None
            self.year_data = datetime.date.strftime(self.time_plot, '%Y')
            # print(self.year_data)
            fastname = '/home/pi/data/yearlyplot/' + self.year_data + '*.hdf5'
            self.glob_data_ = glob.glob(fastname)
            # print(self.glob_data_)
            self.name_data = '/home/pi/data/yearlyplot/' + datetime.date.strftime(self.time_plot, 'plot_%Y.hdf5')
            self.name_dataparse = '/home/pi/data/yearlyplot/' + datetime.date.strftime(self.time_plot, 'plot_%Y.pdf')
            # print('working yearly')
            self.plotit(self.name_dataparse)

    def plotit(self, fname_plot):
        for o in self.glob_data_:
            print('working on glob')
            with h5py.File(o, 'a') as k:
                # print('....')
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
                print(self.npx1a[a])
                self.npstrx1a[a] = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime(self.npx1a[a]))
                print(self.npstrx1a)

            fig = plt.figure(figsize = (8,8)) #Sets figure size in inches
            ax = fig.add_subplot(2, 1, 1)
            ax.plot(self.npstrx1a,self.y1a, color = [0, 0, 0]) #Plots vectors x vs y; they must have the same dimension. I also put in a color argument (rgb).

            #Here we will set the x and y limits
            # ax.set_xlim([0, 1])
            # ax.set_ylim([0, 1])

            #Here we set x and y labels as strings, they can be whatever you want them to be
            # ax.set_xlabel('Time')
            # ax.set_ylabel('Temp oC')

            #Here we eliminate the top and righthand parts of the box enclosing the figure
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.yaxis.set_ticks_position('left')
            ax.xaxis.set_ticks_position('bottom')

            ax = fig.add_subplot(2, 1, 2)
            ax.plot(self.npstrx1a,self.y1a, color = [0, 0, 0]) #Plots vectors x vs y; they must have the same dimension. I also put in a color argument (rgb).

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
        print(temptemp)
        print(temphumidy)
        timestamp_ = datars.stringtime()  # recall temp/humidity data
        filedate = datars.dates()  # process epoch for date
        filenamealpha = filedate + ".hdf5"  # make the date filename
        tickytock = datars.ticktock() #get fullepoch for timerthread

        hd5file(filenamealpha, timestamp_, temptemp, temphumidy)

        waittime_ = countdown()
        waittime_.timerthreadinit(10, tickytock)
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
            gatherit.joina('daily')
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
