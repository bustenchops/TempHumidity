import glob
import os

location = '/home/pi/'

fileset = [file for file in glob.glob(location + "*.hdf5")]

for file in fileset:
    print(file)

fileset.sort(reverse=True)
for file in fileset:
    print(file)
