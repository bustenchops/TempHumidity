import smbus2
import bme280

port = 1
address = 0x76
bus = smbus2.SMBus(port)

calibration_params = bme280.load_calibration_params(bus, address)

# the sample method will take a single reading and return a
# compensated_reading object
data = bme280.sample(bus, address, calibration_params)

# the compensated_reading class has the following attributes
print(data.id)
print(data.timestamp)
print(data.temperature)
print(data.pressure)
print(data.humidity)

# there is a handy string representation too
print(data)

print('AFTER data manip')
class getdata():  # get required data in 1 call
    def __init__(self):
        self.sampledata = bme280.sample(bus, address, calibration_params)
        self.timedata = self.sampledata.timestamp
        self.tempdata = self.sampledata.temperature
        self.humiddata = self.sampledata.humidity
        self.barodata_init = self.sampledata.pressure
        self.barodata = None
        self.baro_data = None
        self.humid_data = None
        self.temp_data = None

    def doit(self):
        self.temp_data = '{:3.2f}'.format(self.tempdata / 1.)
        self.humid_data = '{:3.2f}'.format(self.humiddata / 1.)
        self.barodata = '{:3.2f}'.format(self.barodata_init / 10.)
        self.baro_data = float(self.barodata)
        return self.temp_data, self.humid_data, self.barodata

getting_data=getdata()
temperature, humidity, barometer = getting_data.doit()
print(temperature)
print(humidity)
print(barometer)
