# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TempHumid3507.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import datetime
import time
import os
import h5py
import numpy as np
import matplotlib.pyplot as plt
import glob
from dateutil.relativedelta import relativedelta
import pandas as pd
import sys
from PyQt5 import (
    QtCore, QtGui, QtWidgets
)
from PyQt5.QtWidgets import (
    QMessageBox, QDialog
)
import pyqtgraph as pg


class Ui_MainWindow(object):
    def __init__(self):
        #declare variables for GUI
        self.datadir_path = "none selected"
        self.hdffile_path = "none selected"
        self.climatefile_path = "none selected"

        #declare variables for climatedata update
        self.inputone = None
        self.inputname = None
        self.inputconfirm = None
        self.inputbackup = None

        self.climatedataupdate = None
        self.climateupdate_size = None

        # self.savefile = None
        self.lookforfile = None

        self.length_olddata = None
        self.climatehdf5entry = None

        self.lastnum_olddata = None
        self.lastentry_olddata = None
        self.searchdata = 1
        self.updatesearch = None

        self.climate_time = None
        self.climate_time_local = None
        self.climate_temp = None
        self.climate_humid = None
        self.climate_baro = None

        self.searchrange = None

        #declare variable for hdf5compile of all datasets
        # self.prebarodatafileloc = '/home/pi/climatedata/datafilesold/'
        self.barodatafileloc = None
        # self.h5pyclimatefile = '/home/pi/climatedata/climatedata.hdf5'
        self.filelist = None
        self.climateunixdata = []
        self.firsttimeentry = None
        self.datasetoldtemp = None
        self.datasetoldhumid = None
        self.nearestvalue = None
        self.timeentryindex = None
        self.timeentryindex_temp = None
        self.datasetoldtime = None
        self.datasetoldbaro = None

        #delcare variables for graphing - note some not used
        #self.startlocation = '/home/pi/climatedata/'
        #self.file_name = '/home/pi/climatedata/climatedata.hdf5'
        self.day1 = None
        self.ending = None
        self.day1_formatted = None
        self.ending_formatted = None
        self.date_span_timedelta = None
        self.date_span = None
        self.climate_unixdata = None
        self.date_span_short = None
        self.timestamp_start = None
        self.timestamp_end = None
        self.nearestvalue_start = None
        self.timeentryindex_temp_start = None
        self.timeentryindex_start = None
        self.nearestvalue_end = None
        self.timeentryindex_temp_end = None
        self.timeentryindex_end = None
        self.climate_time_array = []
        self.climate_temp_array = []
        self.climate_humidity_array = []
        self.climate_baro_array = []
        self.data_temp_array = []
        self.data_humidity_array = []
        self.data_baro_array = []
        self.index_tracker = None


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 1600, 800))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        #put graph 1 here
        self.maingraph = pg.PlotWidget(name='maingraph', axisItems={'bottom': pg.DateAxisItem()})
        self.maingraph.setBackground('white')
        self.verticalLayout.addWidget(self.maingraph)

        #put graph 2 here
        self.zoomgraph = pg.PlotWidget(name='zoomgraph', axisItems={'bottom': pg.DateAxisItem()})
        self.zoomgraph.setBackground('white')
        self.verticalLayout.addWidget(self.zoomgraph)

        self.zoomarea = pg.LinearRegionItem([0, 1])
        self.zoomarea.setZValue(-10)
        self.maingraph.addItem(self.zoomarea)

        MainWindow.setCentralWidget(self.centralwidget)
        # Setup toolbar
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        #setup toolbar actions
        self.actionData_Folder = QtWidgets.QAction(MainWindow)
        self.actionData_Folder.setObjectName("actionData_Folder")
        self.actionClimate_File = QtWidgets.QAction(MainWindow)
        self.actionClimate_File.setObjectName("actionClimate_File")
        self.action_Update_Climate_Data = QtWidgets.QAction(MainWindow)
        self.action_Update_Climate_Data.setObjectName("action_Update_Climate_Data")
        self.actionTemp = QtWidgets.QAction(MainWindow)
        self.actionTemp.setCheckable(True)
        self.actionTemp.setObjectName("actionTemp")
        self.actionHumid = QtWidgets.QAction(MainWindow)
        self.actionHumid.setCheckable(True)
        self.actionHumid.setObjectName("actionHumid")
        self.actionBaro = QtWidgets.QAction(MainWindow)
        self.actionBaro.setCheckable(True)
        self.actionBaro.setObjectName("actionBaro")
        self.actionGRAPH = QtWidgets.QAction(MainWindow)
        self.actionGRAPH.setCheckable(True)
        self.actionGRAPH.setObjectName("actionGRAPH")
        self.actionHDF_File = QtWidgets.QAction(MainWindow)
        self.actionHDF_File.setObjectName("actionHDF_File")
        self.actionDataUpdate = QtWidgets.QAction(MainWindow)
        self.actionDataUpdate.setObjectName("actionDataUpdate")

        #setup toolbar buttons
        self.toolBar.addAction(self.actionData_Folder)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionHDF_File)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionClimate_File)
        self.toolBar.addSeparator()
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionGRAPH)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionTemp)
        self.toolBar.addAction(self.actionHumid)
        self.toolBar.addAction(self.actionBaro)
        self.toolBar.addSeparator()
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_Update_Climate_Data)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionDataUpdate)

        # setup statusbar
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        #setup connections for toolbar buttons
        self.actionData_Folder.triggered.connect(self.datafolderselect)
        self.actionHDF_File.triggered.connect(self.HDFfileselect)
        self.actionClimate_File.triggered.connect(self.climatefileselect)
        self.action_Update_Climate_Data.triggered.connect(self.initclimateupdate)
        self.actionDataUpdate.triggered.connect(self.complilepostbaro)
        self.actionTemp.triggered.connect(self.tempgraph)
        self.actionHumid.triggered.connect(self.humidgraph)
        self.actionBaro.triggered.connect(self.barograph)
        self.actionGRAPH.triggered.connect(self.makegrph)
        # self.actionTemp.changed.connect(self.lineEdit.clear) # type: ignore

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Room 3507 - Environment Data"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionData_Folder.setText(_translate("MainWindow", "Data Folder"))
        self.actionClimate_File.setText(_translate("MainWindow", "Climate File"))
        self.action_Update_Climate_Data.setText(_translate("MainWindow", "!Update Climate Data!"))
        self.action_Update_Climate_Data.setToolTip(_translate("MainWindow", "Update Climate Data"))
        self.actionTemp.setText(_translate("MainWindow", "Temp"))
        self.actionHumid.setText(_translate("MainWindow", "Humid"))
        self.actionHumid.setToolTip(_translate("MainWindow", "Humid"))
        self.actionBaro.setText(_translate("MainWindow", "Baro"))
        self.actionBaro.setToolTip(_translate("MainWindow", "Baro"))
        self.actionGRAPH.setText(_translate("MainWindow", "GRAPH"))
        self.actionHDF_File.setText(_translate("MainWindow", "HDF File"))
        self.actionDataUpdate.setText(_translate("MainWindow", "!Update Data!"))

    def datafolderselect(self):
        print("click data folder")
        print(self.datadir_path)
        self.datadir_path = QtWidgets.QFileDialog.getExistingDirectory()
        self.actionData_Folder.setStatusTip(self.datadir_path)
        print(self.datadir_path)
        self.barodatafileloc = self.datadir_path + '/'
        print(self.barodatafileloc)
        # self.fileboxlist()

    def HDFfileselect(self):
        print("click hdf file")
        print(self.hdffile_path)
        self.hdffile_path, _ = QtWidgets.QFileDialog.getSaveFileName()
        print(self.hdffile_path)
        self.graphdone = 0
        self.actionGRAPH.setChecked(False)
        # self.fileboxlist()

    def climatefileselect(self):
        print("click climate file")
        print(self.climatefile_path)
        self.climatefile_path, _ = QtWidgets.QFileDialog.getOpenFileName()
        print(self.climatefile_path)
        # self.fileboxlist()

    def initclimateupdate(self):

        #take CVS update file and put in Pandas array - determine size
        print("opening weather file")
        self.climatedataupdate = pd.read_csv(self.climatefile_path, index_col='date_time_local')
        self.climateupdate_size = self.climatedataupdate.shape[0]

        # checks to see if the file already exist - if the file does not exist make it and put data in.
        #self.savefile = self.filenameloc + self.h5pyclimate
        #self.lookforfile = os.path.isfile(self.savefile)
        #print('Is HD5F file present?')
        #print(self.lookforfile)
        #self.savefile = self.hdffile_path
        self.climatehdf5size()

    def climatehdf5size(self):
        print("check hdf file path")
        if os.path.isfile(self.hdffile_path):
            print('Opening HDF5 file')
            with h5py.File(self.hdffile_path, 'a') as f:
                self.length_olddata = len(f['compiled_data'])
                print('size of the climate HD5F array')
                print(self.length_olddata)
                print('closing file after size check')
                f.close()
        else:
            print('making HDF5 file')
            # if the file does not exist - create it and set up
            with h5py.File(self.hdffile_path, 'a') as f:
                data_type = np.dtype('float')
                self.climatehdf5entry = f.create_dataset('compiled_data', shape=(1, 8), maxshape=(None, 8), dtype=data_type)
                self.length_olddata = len(f['compiled_data'])
                print('size of the climate HD5F array')
                print(self.length_olddata)
                print('closing file after create')
                f.close()
        self.climateupdatesearch()

    def climateupdatesearch(self):
        if os.path.isfile(self.hdffile_path):
            print('Opening HDF5 file')
            self.lastnum_olddata = self.length_olddata - 1
            with h5py.File(self.hdffile_path, 'a') as f:
                self.lastentry_olddata = f['compiled_data'][self.lastnum_olddata, 0]
                f.close()
            # scan the unix time to see if new number is there
            while self.searchdata == 1:
                self.climateupdate_size = self.climateupdate_size - 1
                if self.climateupdate_size < 0:
                    self.searchdata = 2
                    #print('the update file does not go back far enough for consistent data, re-download with more rows')
                    #print('if this is a new file then continue')
                    #self.inputconfirm = input('Do you want to continue? (y or n)')
                    self.climatedatasetalert()
                    if self.inputconfirm == 'OK':
                        self.climateupdate_size = self.climatedataupdate.shape[0] - 1
                        print('size to use is:')
                        print(self.climateupdate_size)
                    else:
                        return()
                self.updatesearch = self.climatedataupdate.unixtime[self.climateupdate_size]
                if self.updatesearch == self.lastentry_olddata:
                    self.searchdata = 2
                    print('Starting entry ')
                    print(self.climateupdate_size)
                    self.climateupdate_size = self.climateupdate_size - 1
                    with h5py.File(self.hdffile_path, 'a') as f:
                        self.lastnum_olddata = len(f['compiled_data'])
                        f['compiled_data'].resize((f['compiled_data'].shape[0] + 1, f['compiled_data'].shape[1]))
                        f.close()
                    print('entry location')
                    print(self.lastnum_olddata)
        self.climateupdatecompile()

    def climateupdatecompile(self):
        if os.path.isfile(self.hdffile_path):
            print('Opening HDF5 file')
            with h5py.File(self.hdffile_path, 'a') as f:
                self.lastnum_olddata = len(f['compiled_data']) - 1
                print('using location in existing')
                print(self.lastnum_olddata)
                self.searchrange = self.climateupdate_size + 1
                for passnum in range(self.searchrange):
                    print('defined range:')
                    print(self.searchrange)
                    print('search range passnum:')
                    print(passnum)
                    if self.climateupdate_size < 0:
                        print('complete')
                    else:
                        print('location within update array')
                        print(self.climateupdate_size)
                        self.climate_time = self.climatedataupdate.unixtime[self.climateupdate_size]
                        self.climate_temp = self.climatedataupdate.temperature[self.climateupdate_size]
                        self.climate_humid = self.climatedataupdate.relative_humidity[self.climateupdate_size]
                        self.climate_baro = self.climatedataupdate.pressure_station[self.climateupdate_size]
                        self.climateupdate_size -= 1
                        f['compiled_data'][self.lastnum_olddata, 0] = self.climate_time
                        f['compiled_data'][self.lastnum_olddata, 1] = self.climate_temp
                        f['compiled_data'][self.lastnum_olddata, 2] = self.climate_humid
                        f['compiled_data'][self.lastnum_olddata, 3] = self.climate_baro
                        print('entering climate data location lastnum_olddata')
                        print(self.lastnum_olddata)
                        self.lastnum_olddata += 1
                        if passnum < self.searchrange - 1:
                            f['compiled_data'].resize((f['compiled_data'].shape[0] + 1, f['compiled_data'].shape[1]))
                f.close()

    # LEGEND FOR HDF5FILE
    # 0 unixtime for downloaded climate data
    # 1 temp for downloaded climate data
    # 2 humidity for downloaded climate data
    # 3 baro for downloaded climate data
    # 4 time from dataset
    # 5 temp from dataset
    # 6 humidity from dataset
    # 7 baro from dataset


    def complilepostbaro(self):
        self.barodatafileloc = self.datadir_path + '/'
        #this is list comprehension
        print('compiling list of pre-baro reading hdf5 files')
        self.filelist = [file for file in glob.glob(self.barodatafileloc + '*.hdf5')]
        print('sort files ascending')
        self.filelist.sort()
        print(self.filelist)
        with h5py.File(self.hdffile_path, 'a') as f:
            print('open')
            self.climateunixdata = f['compiled_data'][:, 0]
            for dataset in self.filelist:
                with h5py.File(dataset, 'a') as b:
                    print('open data file')
                    self.datafileunix = b['dailydata/temperature_C'][:, 0]
                    lastarraypos = len(self.datafileunix) - 1
                    lastarrayval = self.datafileunix[lastarraypos]
                    print('array val found')
                    print(lastarrayval)
                    if lastarrayval >= 1596415861:
                        print('has baro')
                        self.firsttimeentry = b['dailydata/temperature_C'][0, 0]
                        print('first time entry:')
                        print(self.firsttimeentry)
                        self.nearestvalue = self.climateunixdata[min(range(len(self.climateunixdata)), key = lambda i: abs(self.climateunixdata[i]-self.firsttimeentry))]
                        print('nearest entry in climatedata:')
                        print(self.nearestvalue)
                        self.timeentryindex_temp = np.where(self.climateunixdata == self.nearestvalue)
                        self.timeentryindex = self.timeentryindex_temp[0][0]
                        print('nearest entry index location:')
                        print(self.timeentryindex)
                        for datapoints in range(len(b['dailydata/temperature_C'])):
                            print('data entry:')
                            print(datapoints)
                            print('at:')
                            print(self.timeentryindex)
                            self.datasetoldtime = b['dailydata/temperature_C'][datapoints, 0]
                            self.datasetoldtemp = b['dailydata/temperature_C'][datapoints,1]
                            self.datasetoldhumid = b['dailydata/humidity'][datapoints,1]
                            self.datasetoldbaro = b['dailydata/pressure'][datapoints, 1]
                            f['compiled_data'][self.timeentryindex, 4] = self.datasetoldtime
                            f['compiled_data'][self.timeentryindex, 5] = self.datasetoldtemp
                            f['compiled_data'][self.timeentryindex, 6] = self.datasetoldhumid
                            f['compiled_data'][self.timeentryindex, 7] = self.datasetoldbaro
                            self.timeentryindex += 1
                        b.close()
                    else:
                        print('no pressure')
                        self.firsttimeentry = b['dailydata/temperature_C'][0, 0]
                        print('first time entry:')
                        print(self.firsttimeentry)
                        self.nearestvalue = self.climateunixdata[min(range(len(self.climateunixdata)), key=lambda i: abs(self.climateunixdata[i] - self.firsttimeentry))]
                        print('nearest entry in climatedata:')
                        print(self.nearestvalue)
                        self.timeentryindex_temp = np.where(self.climateunixdata == self.nearestvalue)
                        self.timeentryindex = self.timeentryindex_temp[0][0]
                        print('nearest entry index location:')
                        print(self.timeentryindex)
                        for datapoints in range(len(b['dailydata/temperature_C'])):
                            print('data entry:')
                            print(datapoints)
                            print('at:')
                            print(self.timeentryindex)
                            self.datasetoldtime = b['dailydata/temperature_C'][datapoints, 0]
                            self.datasetoldtemp = b['dailydata/temperature_C'][datapoints, 1]
                            self.datasetoldhumid = b['dailydata/humidity'][datapoints, 1]
                            f['compiled_data'][self.timeentryindex, 4] = self.datasetoldtime
                            f['compiled_data'][self.timeentryindex, 5] = self.datasetoldtemp
                            f['compiled_data'][self.timeentryindex, 6] = self.datasetoldhumid
                            self.timeentryindex += 1
                        b.close()
        f.close()

    def climatedatasetalert(self):
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Information)

        self.msg.setText("Climate Data File does not go far enough back.")
        self.msg.setInformativeText("If this is a new HDF5 file then click ok")
        self.msg.setWindowTitle("Attention.")
        self.msg.setDetailedText("The update file does not go back far enough for consistent data, re-download with more rows")
        self.msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        self.msg.buttonClicked.connect(self.msgbtn)

        retval = self.msg.exec_()

    def msgbtn(self, i):
        print("Button pressed is:", i.text())
        self.inputconfirm = i.text()
        print(self.inputconfirm)

    def makegrph(self):
        if self.actionGRAPH.isChecked():
            if self.graphdone == 0:
                self.graphdone = 1
                print('clear old arrays')
                self.climate_time_array.clear()
                self.climate_temp_array.clear()
                self.climate_humidity_array.clear()
                self.climate_baro_array.clear()
                self.data_temp_array.clear()
                self.data_humidity_array.clear()
                self.data_baro_array.clear()
                self.actionTemp.setChecked(False)
                self.actionHumid.setChecked(False)
                self.actionBaro.setChecked(False)
                print('making the graph')
                self.index_tracker = 0
                with h5py.File(self.hdffile_path, 'a') as f:
                    self.climate_unixdata = f['compiled_data'][:, 0]
                    self.arraylen = len(self.climate_unixdata)
                    self.arraycount = len(self.climate_unixdata)
                    print('arraylength = ')
                    print(self.arraylen)
                    while self.index_tracker < self.arraylen:
                        print(str(self.index_tracker) + " of " + str(self.arraylen))
                        # self.climate_time_array_tempvalue = datetime.datetime.fromtimestamp(f['compiled_data'][self.index_tracker, 0])
                        self.climate_time_array.append(f['compiled_data'][self.index_tracker, 0])
                        self.climate_temp_array.append(f['compiled_data'][self.index_tracker, 1])
                        self.climate_humidity_array.append(f['compiled_data'][self.index_tracker, 2])
                        self.climate_baro_array.append((f['compiled_data'][self.index_tracker, 3]))
                        self.data_temp_array.append(f['compiled_data'][self.index_tracker, 5])
                        self.data_humidity_array.append(f['compiled_data'][self.index_tracker, 6])
                        self.data_baro_array.append(f['compiled_data'][self.index_tracker, 7])
                        self.index_tracker += 1
                        self.arraycount -= 1
                    f.close()
                self.statusbar.showMessage('Done compiling graphs')
            else:
                if self.graphdone == 1:
                    self.statusbar.showMessage('Graph compiling done already')
        else:
            self.statusbar.showMessage('Graph compiling done already')

    def tempgraph(self):
        if self.actionTemp.isChecked():
            self.statusbar.showMessage('Add temperature data')
            self.climatetempplot = self.maingraph.plot()
            self.climatetempplot.setPen(pg.mkPen('silver', width=2))
            self.climatetempplot.setData(self.climate_time_array, self.climate_temp_array)
            self.datatempplot = self.maingraph.plot()
            self.datatempplot.setPen(pg.mkPen('black', width=2))
            self.datatempplot.setData(self.climate_time_array, self.data_temp_array)
            self.climatetempplot2 = self.zoomgraph.plot()
            self.climatetempplot2.setPen(pg.mkPen('silver', width=2))
            self.climatetempplot2.setData(self.climate_time_array, self.climate_temp_array)
            self.datatempplot2 = self.zoomgraph.plot()
            self.datatempplot2.setPen(pg.mkPen('black', width=2))
            self.datatempplot2.setData(self.climate_time_array, self.data_temp_array)


            self.zoomed()
        else:
            print('cleartemp')
            self.statusbar.showMessage('Remove temperature data')
            self.climatetempplot.clear()
            self.datatempplot.clear()
            self.climatetempplot2.clear()
            self.datatempplot2.clear()
            self.zoomed()


    def humidgraph(self):
        if self.actionHumid.isChecked():
            self.statusbar.showMessage('Add humidity data')
            self.climatehumidplot = self.maingraph.plot()
            self.climatehumidplot.setPen(pg.mkPen('lightsalmon', width=2))
            self.climatehumidplot.setData(self.climate_time_array, self.climate_humidity_array)
            self.datahumidplot = self.maingraph.plot()
            self.datahumidplot.setPen(pg.mkPen('red', width=2))
            self.datahumidplot.setData(self.climate_time_array, self.data_humidity_array)
            self.climatehumidplot2 = self.zoomgraph.plot()
            self.climatehumidplot2.setPen(pg.mkPen('lightsalmon', width=2))
            self.climatehumidplot2.setData(self.climate_time_array, self.climate_humidity_array)
            self.datahumidplot2 = self.zoomgraph.plot()
            self.datahumidplot2.setPen(pg.mkPen('red', width=2))
            self.datahumidplot2.setData(self.climate_time_array, self.data_humidity_array)
            self.zoomed()
        else:
            print('cleartemp')
            self.statusbar.showMessage('Remove humidity data')
            self.climatehumidplot.clear()
            self.datahumidplot.clear()
            self.climatehumidplot2.clear()
            self.datahumidplot2.clear()
            self.zoomed()

    def barograph(self):
        if self.actionBaro.isChecked():
            self.statusbar.showMessage('Add pressure data')
            self.climatebaroplot = self.maingraph.plot()
            self.climatebaroplot.setPen(pg.mkPen('lightblue', width=2))
            self.climatebaroplot.setData(self.climate_time_array, self.climate_baro_array)
            self.databaroplot = self.maingraph.plot()
            self.databaroplot.setPen(pg.mkPen('blue', width=2))
            self.databaroplot.setData(self.climate_time_array, self.data_baro_array)
            self.climatebaroplot2 = self.zoomgraph.plot()
            self.climatebaroplot2.setPen(pg.mkPen('lightblue', width=2))
            self.climatebaroplot2.setData(self.climate_time_array, self.climate_baro_array)
            self.databaroplot2 = self.zoomgraph.plot()
            self.databaroplot2.setPen(pg.mkPen('blue', width=2))
            self.databaroplot2.setData(self.climate_time_array, self.data_baro_array)
            self.zoomed()
        else:
            print('cleartemp')
            self.statusbar.showMessage('Remove pressure data')
            self.climatebaroplot.clear()
            self.databaroplot.clear()
            self.climatebaroplot2.clear()
            self.databaroplot2.clear()
            self.zoomed()

    def zoomed(self):
        print('zoom')
        def updatePlot():
            self.zoomgraph.setXRange(*self.zoomarea.getRegion(), padding=0)

        def updateRegion():
            self.zoomarea.setRegion(self.zoomgraph.getViewBox().viewRange()[0])

        self.zoomarea.sigRegionChanged.connect(updatePlot)
        self.zoomgraph.sigXRangeChanged.connect(updateRegion)
        updatePlot()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
