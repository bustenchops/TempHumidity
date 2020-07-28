import datetime
import time
import os
import h5py
import numpy as np
import matplotlib.pyplot as plt
import glob
from dateutil.relativedelta import relativedelta
import pandas as pd

filename = './home/climatedata/weatherstats_ottawa_hourly.csv'
df = pd.read_csv(filename, index_col='date_time_local')
print(df.unixtime[0:5])
howbig = df.shape[0]
print(howbig)