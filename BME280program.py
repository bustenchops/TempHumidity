import datetime
import time
import os
import h5py
import threading
import numpy as np
import glob

import smbus2
import bme280

# set up the BME
port = 1
address = 0x76
bus = smbus2.SMBus(port)
calibration_params = bme280.load_calibration_params(bus, address)


class getdata():  # get required data in 1 call
    def __init__(self):
        self.sampledata = bme280.sample(bus, address, calibration_params)
        self.timedata = self.sampledata.timestamp
        self.tempdata = self.sampledata.temperature
        self.humiddata = self.sampledata.humidity
        self.barodata_init = self.sampledata.pressure
        self.barodata = None
        self.humid_data = None
        self.temp_data = None

    def doit(self):
        self.temp_data = self.tempdata
        self.humid_data = self.humiddata
        self.barodata = self.barodata_init / 10
        return self.temp_data, self.humid_data, self.barodata

    #takes timestamp from the BME280 code, converts to unixtime and puts it as an int
    def int_current_time(self):
        self.current_time = datetime.datetime.timestamp(self.timedata)
        time_data = int(self.current_time)
        print('time from getdata init')
        print(time_data)
        return time_data

# parse out the date from the data and return it to be used in the hd5 file
    def string_current_date(self):
        currentdate = time.strftime("%Y-%m-%d-week_%U", time.localtime(self.current_time))
        return str(currentdate)

# full epoch variable to be used by timer
    def timer_time(self):
        data_time = self.timedata
        interval_time = datetime.timedelta(seconds=3598)
        # 543598 because at 3600s the intervals are 2 sec too long
        target_time = data_time + interval_time
        return (target_time)

    def dating(self):
        checktime = datetime.datetime.now()
        return(checktime)

    def save_date(self):
        with open('/home/pi/Gits/TempHumidity/textsave.txt', 'w') as time_text:
            checktime = datetime.datetime.now()
            checktime_format = datetime.date.strftime(checktime, '%Y %m %d')
            print('date from save_date')
            print(checktime_format)
            time_text.write(checktime_format)
            time_text.close()

    def date_recall(self):
        try:
            os.path.isfile('/home/pi/Gits/TempHumidity/textsave.txt')
            with open('textsave.txt', 'r') as time_read:
                text = time_read.read()
                recalldate = datetime.datetime.strptime(text, '%Y %m %d')
                time_read.close()
            print('sending recalldate from date_recall')
            return recalldate
        except:
            with open('/home/pi/Gits/TempHumidity/textsave.txt', 'w') as time_text:
                checktime = datetime.datetime.now()
                checktime_format = datetime.date.strftime(checktime, '%Y %m %d')
                time_text.write(checktime_format)
                time_text.close()
            print('sending date from function: date_recall exception')
            return checktime
# Function not part of the class but is called in the program immediately after
# the above class
def hd5file(fname, hdftime, hdftemp, hdfhumidy, hdfbaro):
    try:
        # checks to see if the file already exist - if the file exists open it and determine the size of the range.
        os.path.isfile(fname)
        print('opening file')
        aft = os.path.isfile(fname)
        print('if HD5F file present')
        print(aft)
        with h5py.File(fname, 'a') as f:
            num_timestamp = len(f['dailydata/temperature_C'])
            print('size of the HD5F array')
            print(num_timestamp)
            f['dailydata/temperature_C'].resize((f['dailydata/temperature_C'].shape[0] + 1, f['dailydata/temperature_C'].shape[1]))
            f['dailydata/humidity'].resize((f['dailydata/humidity'].shape[0] + 1, f['dailydata/humidity'].shape[1]))
            f['dailydata/pressure'].resize((f['dailydata/pressure'].shape[0] + 1, f['dailydata/pressure'].shape[1]))
            f['dailydata/temperature_C'][num_timestamp, 0] = hdftime
            f['dailydata/temperature_C'][num_timestamp, 1] = hdftemp
            f['dailydata/humidity'][num_timestamp, 0] = hdftime
            f['dailydata/humidity'][num_timestamp, 1] = hdfhumidy
            f['dailydata/pressure'][num_timestamp, 0] = hdftime
            f['dailydata/pressure'][num_timestamp, 1] = hdfbaro
            print('closing file')
            f.close()
    except:
        print('making file')
# if the file does not exist - create it and set up
        with h5py.File(fname, 'a') as u:
            dataforday = u.create_group('dailydata')
            dt = np.dtype('float')
            datatemp_stamp = dataforday.create_dataset('temperature_C', shape=(1, 2), maxshape=(None, 2), dtype=dt)
            datahumid_stamp = dataforday.create_dataset('humidity', shape=(1, 2), maxshape=(None, 2), dtype=dt)
            databaro_stamp = dataforday.create_dataset('pressure', shape=(1, 2), maxshape=(None, 2), dtype=dt)
            datatemp_stamp[0, 0] = hdftime
            datatemp_stamp[0, 1] = hdftemp
            datahumid_stamp[0, 0] = hdftime
            datahumid_stamp[0, 1] = hdfhumidy
            databaro_stamp[0, 0] = hdftime
            databaro_stamp[0, 1] = hdfbaro
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
    def timerthreadinit(self, target_time_1):
        self.t_target = target_time_1
        self.timerthread = threading.Thread(target=self.threadtimer)
        self.timerthread.start()

    def waittime(self):  # acquires the current time epoch and compares to the datatimestamp
        timertime = datetime.datetime.now()
        print('compare time to target')
        if self.t_target > timertime:
            return True
        elif self.t_target <= timertime:
            return False

# while loop that repeatedly checks the wait time and sets the inter-interval check time
    def threadtimer(self):
        print('Starting...')
        second_count = 0
        while self.waittime() is True:
            print('waiting for timer round: ', second_count)
            second_count += 1
            time.sleep(1)

        print('DING FRIES ARE DONE')

# quick method to print out the variables to see if things are working
# def testoutputs():
#     print(datars)
#     print(timestamp_)
#     print(filedate)
#     print(filenamealpha)

# ####################  sort the data, make the folders and store it is in the right place #####
class dailystore():

    def __init__(self):
        self.dest = '/home/pi/climatedata/datafiles/'
        self.todaytemp = None
        self.todaytime = None
        self.names = None
        self.ext = None
        self.namedateobj = None
        self.fileglob = None

    def movedata(self):
        self.fileglob = glob.glob('*.hdf5')
        print(self.fileglob)
        if os.path.exists(self.dest):
            print('daily directory exists')
            print(self.dest)
            self.todaytemp = datetime.datetime.now().strftime("%Y-%m-%d")
            self.todaytime = datetime.datetime.strptime(self.todaytemp, "%Y-%m-%d")
            for i in self.fileglob:
                print('file:' , i)
                self.names, self.ext = os.path.splitext(i)
                self.namedateobj = datetime.datetime.strptime(self.names, '%Y-%m-%d-week_%U')
                if self.namedateobj < self.todaytime:
                    print('file is from previous day')
                    print('moving to /home/pi/Gits/TempHumidity/' + i + ' ' + self.dest)
                    os.system('mv /home/pi/Gits/TempHumidity/' + i + ' ' + self.dest)
        else:
            os.makedirs(self.dest)
            print('making directory')
            print(self.dest)
            for i in self.fileglob:
                self.names, self.ext = os.path.splitext(i)
                self.namedateobj = datetime.datetime.strptime(self.names, '%Y-%m-%d-week_%U')
                self.todaytime = datetime.datetime.strptime(self.todaytemp, "%Y-%m-%d")
                if self.namedateobj < self.todaytime:
                    print('file is from previous day')
                    os.system('mv /home/pi/Gits/TempHumidity/' + i + ' ' + self.dest)

# #################___PROGRAM___################################

while True:
    try:
        datars = getdata()
        # inits the sensor and gets baro temp, humid and time
        temptemp, temphumidy, tempbaro = datars.doit()
        #returns the data points as strings
        print('temp reading is')
        print(temptemp)
        print('humidity reading is')
        print(temphumidy)
        print('h4pressure reading is')
        print(tempbaro)

        temptime = datars.int_current_time()
        # returns the timepoint
        print('time reading is')
        print(temptime)

        filedate = datars.string_current_date()
        # returns the date for the file name
        print(filedate)

        filenamealpha = filedate + '.hdf5'
        # add extension to the date for filename
        print(filenamealpha)

        hd5file(filenamealpha, temptime, temptemp, temphumidy, tempbaro)
        # puts the data into HDF5 file

        time_interval = datars.timer_time()
        # return the time data was acquired plus 3600 seconds for timerthread

        waittime_ = countdown()
        waittime_.timerthreadinit(time_interval)
        # sets up the timer in a thread waits for set time from timestamp
        waittime_.timerthread.join()
        # waits for thread to finish


        first_date = datars.date_recall()
        print("first date")
        # recalls the date from the text file
        next_date = datars.dating()
        print('time now:', next_date)
        subdate = datetime.timedelta(hours=25)
        print('delta time:', subdate)
        overday = next_date - subdate
        print('25h ago:', overday)

        if overday > first_date:
            transfer_files = dailystore()
            transfer_files.movedata()
            print('copying the climatedata folder to Onedrive')
            os.system('rclone copy /home/pi/climatedata/datafiles odrive:/Room3507stats')
            datars.save_date()

    except (KeyboardInterrupt, SystemExit):
        print ('keyboardinterrupt found!')
        print ('...Program Stopped Manually!')
        raise
    except:
        print('stop!')
        raise
