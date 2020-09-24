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
# df = pd.read_csv(filename, index_col='date')
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

# testin = input('date in format')
checktime = datetime.datetime.now()
# deltatime = datetime.timedelta(seconds=3600)
# futuretime = checktime + deltatime
# print('checktime')
# print(checktime)
# checktime_format = datetime.datetime.strftime(checktime, '%Y-%m-%d')
# print('checktime_format')
# print(checktime_format)
# timestamp = datetime.datetime.timestamp(checktime)
# print(timestamp)
# if futuretime > checktime:
#     print('yes future is greater')
checktime_format_manual = '2020-09-20'
tttt = datetime.datetime.strptime(checktime_format_manual, '%Y-%m-%d')
print('ttt trptime')
print(tttt)
ttttt = time.mktime(tttt.timetuple())
print(ttttt)
if checktime > tttt:
    print('yes it works')

#
# def date_recall():
#     fart = datetime.datetime.now()
#     fart_1 = datetime.timedelta(days=1)
#     fart_2 = fart + fart_1
#     return (fart_2)
#
#
# gotforit = date_recall()
# print(gotforit)
#
# fart_4 = datetime.timedelta(days=1)
# timestamp_datetime = datetime.datetime.fromtimestamp(1596056400)
# arr = []
# for x in range(5):
#     print('more timey stuff')
#     qqqq = timestamp_datetime.strftime('%Y-%m-%d_%Hh')
#     print(qqqq)
#     timestamp_datetime = timestamp_datetime + fart_4
#     arr.append(qqqq)
# print(arr)


# aaa = input('yyyy-mm-dd')
# bbb = input('yyyy-mm-dd')
# aaa1 = datetime.datetime.strptime(aaa, '%Y-%m-%d')
# print(aaa1)
# bbb1 = datetime.datetime.strptime(bbb, '%Y-%m-%d')
# print(bbb1)
# ccc1 = bbb1 - aaa1
# print(ccc1)
# ddd1 = pd.Timedelta(ccc1)
# print(ddd1.days)

# day1 = '2020-01-01'
# ending = '2020-01-03'
#
# day1_formatted = datetime.datetime.strptime(day1, '%Y-%m-%d')
# ending_formatted = datetime.datetime.strptime(ending, '%Y-%m-%d')
# date_span_timedelta = ending_formatted - day1_formatted + (datetime.timedelta(days=1))
# date_span = pd.Timedelta(date_span_timedelta)
# date_span_short = date_span.days
# print('day1: ', day1_formatted, ' lastday: ', ending_formatted, ' number days spanned: ', date_span_short)
# timestamp = int(datetime.datetime.timestamp(day1_formatted))
# print('unix format of day1 ', timestamp)

# todaytemp = datetime.datetime.now().strftime("%Y-%m-%d")
# todaytime = datetime.datetime.strptime(todaytemp, "%Y-%m-%d")
#
# print(todaytemp)
# print(todaytime)
# testfile = 'test.hdf5'
# hdftime = 1571892942
# hdftemp = 24.5458889797
#
#
# with h5py.File(testfile, 'a') as u:
#     dataforday = u.create_group('dailydata')
#     dt = np.dtype('float')
#     datatemp_stamp = dataforday.create_dataset('temperature_C', shape=(1, 2), maxshape=(None, 2), dtype=dt)
#     datatemp_stamp[0, 0] = hdftime
#     datatemp_stamp[0, 1] = hdftemp
#     print('closing file again')
#     u.close()