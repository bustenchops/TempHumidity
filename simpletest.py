import datetime
import time
import os
import h5py
import numpy as np
import matplotlib.pyplot as plt
import glob
from dateutil.relativedelta import relativedelta
import pandas as pd
import pytz

# filename = './home/climatedata/weatherstats_ottawa_hourly.csv'
# df = pd.read_csv(filename, index_col='date_time_local')
# print(df.unixtime[0:5])
# howbig = df.shape[0]
# print(howbig)

# h5pyclimatefile = './home/climatedata/climatedata.hdf5'
#
# with h5py.File(h5pyclimatefile, 'a') as a:
#     length_olddata = len(a['compiled_data'])
#     print('size of the climate HD5F array')
#     print(length_olddata)
#     aar = a['compiled_data'][:,0]
#     print(aar)
#     print('closing file after size check')
#     a.close()



# timedata = time.time()
# print('time from first acquire - full unixtime')
# print(timedata)
# goodtimestring = int(timedata)
# print('time from getdata init - unixtime to second')
# print(goodtimestring)
# currentdate = time.strftime("%Y-%m-%d-week_%U", time.localtime(timedata))
# print(currentdate)


checktime = datetime.datetime.now()
deltatime = datetime.timedelta(seconds=3600)
futuretime = checktime + deltatime
print(checktime)
checktime_format = datetime.date.strftime(checktime, '%Y %m %d')
print('date from save_date')
print(checktime_format)
timestamp = datetime.datetime.timestamp(checktime)
print(timestamp)
if futuretime > checktime:
    print('yes')

def date_recall():
    fart = datetime.datetime.now()
    fart_1 = datetime.timedelta(seconds=1111)
    fart_2 = fart + fart_1
    return (fart_2)

gotforit = date_recall()
print(gotforit)