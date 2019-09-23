import datetime
import time
import os


def savedate():
    with open('textsave.txt', 'w') as time_text:
        checktime = datetime.datetime.now()
        checktime_format = datetime.date.strftime(checktime, '%Y %m %d')
        print(checktime_format)
        time_text.write(checktime_format)
        time_text.close()

def recall():
    with open('textsave.txt', 'r') as time_read:
        text = time_read.read()
        recalldate = datetime.datetime.strptime(text, '%Y %m %d')
        time_read.close()
    print('sending recalldate')
    return recalldate

def process(ittoit):
    week_data1 = datetime.date.strftime(ittoit, '%U')
    return week_data1

savedate()
fart = recall()
print(fart)
turd = process(fart)
print(turd)
