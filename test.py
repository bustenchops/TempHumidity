import glob

location = '/home/pi/'

fileset = [file for file in glob.glob(location + "*.txt")]

for file in fileset:
    print(file)
