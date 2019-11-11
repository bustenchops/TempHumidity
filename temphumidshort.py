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
        print('trigger1')
        #time.sleep(2)
        self.sampledata.trigger()
        time.sleep(5)
        print('trigger2 5s later')
        self.sampledata.trigger()
        self.current = time.time()
        self.tempdata = '{:3.2f}'.format(self.sampledata.temperature() / 1.)
        self.humidata = '{:3.2f}'.format(self.sampledata.humidity() / 1.)
        self.sampledata.cancel()
        self.pi.stop()

    def doit(self):
        ttt = float(self.tempdata)
        hhh = float(self.humidata)
        return ttt, hhh

# parse out the timestamp from the data and return it to be used in hd5 file
    # def times(self):
    #     currenttime = self.current - self.twentynineteen
    #     return currenttime

    def stringtime(self):
        goodtimestring = int(self.current)
        print('time frome getdata init')
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
            checktime_format = datetime.date.strftime(checktime, '%Y %m %d')
            print('date from save_date')
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
            print('sending recalldate from date_recall')
            return recalldate
        except:
            with open('textsave.txt', 'w') as time_text:
                checktime = datetime.datetime.now()
                checktime_format = datetime.date.strftime(checktime, '%Y %m %d')
                time_text.write(checktime_format)
                time_text.close()
            print('sending date from date_recal exception')
            return checktime
# Function not part of the class but is called in the program immediately after
# the above class
def hd5file(fname, timestamp_s, hdftemp, hdfhumidy):
    try:
        # checks to see if the file already exist - if the file exists open it and determine the size of the range.
        os.path.isfile(fname)
        print('opening file')
        aft = os.path.isfile(fname)
        print('if HD5F file present')
        print(aft)
        with h5py.File(fname, 'a') as f:
            # temptemp = 100
            # temphumidy = 100
            num_timestamp = len(f['dailydata/temperature_C'])
            print('size of the HD5F array')
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
        while self.waittime() is True:
            print('waiting for timer')
            time.sleep(120)
        print('DING FRIES ARE DONE')

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
        self.dest = '/home/pi/data/'
        self.daily = self.dest + 'daily'

    def movedaily(self):
        fileglob = glob.glob('*.hdf5')
        if os.path.exists(self.daily):
            print('daily directory exists')
            todaytemp = datetime.datetime.now().strftime("%Y-%m-%d")
            todaytime = datetime.datetime.strptime(todaytemp, "%Y-%m-%d")
            for i in fileglob:
                names, ext = os.path.splitext(i)
                namedateobj = datetime.datetime.strptime(names, '%Y-%m-%d-week_%U')
                if namedateobj < todaytime:
                    os.system('mv /home/pi/' + i + ' /home/pi/data/daily/')
        else:
            os.makedirs(self.daily)
            for i in fileglob:
                names, ext = os.path.splitext(i)
                namedateobj = datetime.datetime.strptime(names, '%Y-%m-%d-week_%U')
                if namedateobj < todaytime:
                    os.system('mv /home/pi/' + i + ' /home/pi/data/daily/')

# #################___PROGRAM__################################3_

while True:
    try:
        datars = getdata()
        # inits the sensor and gets temp, humid and time - closes sensor
        temptemp, temphumidy = datars.doit()
        #returns the data points as strings
        print('temp reading is')
        print(temptemp)
        print('humidity reading is')
        print(temphumidy)
        timestamp_ = datars.stringtime()
        # returns the timepoint
        filedate = datars.dates()
        # returns the date for the file name
        filenamealpha = filedate + ".hdf5"
        # add extension to the date for filename
        tickytock = datars.ticktock()
        # returnt the current time for timerthread

        hd5file(filenamealpha, timestamp_, temptemp, temphumidy)
        # puts the data into HDF5 file

        waittime_ = countdown()
        waittime_.timerthreadinit(3600, tickytock)
        # sets up the timer in a thread waits for set time from timestamp
        waittime_.timerthread.join()
        # waits for thread to finish
        first_date = datars.date_recall()
        print("first date")
        # recalls the date from the text file
        next_date = datars.dating()
        subdate = datetime.timedelta(hours=26)
        overday = next_date - subdate

        if overday > first_date:
            dailystore = storedata()
            dailystore.movedaily()
            dailystore.checkmake('daily')
            os.system('rclone copy /home/pi/data Gdrive:/data')
            datars.save_date()

    except (KeyboardInterrupt, SystemExit):
        print ('keyboardinterrupt found!')
        print ('...Program Stopped Manually!')
        raise
    except:
        print('stop!')
        raise
