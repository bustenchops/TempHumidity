import datetime
import time
import os


with open("textsave.txt", "w") as time_text:
    day_data1 = datetime.datetime.now()
    aaa = datetime.date.strftime(day_data1, '%Y %m %d')
    print(aaa)
    time_text.write(aaa)
    # (f"Purchase Amount: {aaa}", file=time_text)
    time_text.close()

with open("textsave.txt", "r") as time_read:
    text = time_read.read()
    simpleDate = datetime.datetime.strptime(text, '%Y %m %d')
    day_data2 = simpleDate + datetime.timedelta(days=1)
    week_data1 = datetime.date.strftime(simpleDate, '%U')
    if day_data2 > simpleDate:
        print(day_data2)
        print(week_data1)
        print(simpleDate)
    else:
        print('shits fucked yo')
    time_read.close()
