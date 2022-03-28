import sys
from PySide6.QtWidgets import (
    QMainWindow, QApplication,
    QSpinBox, QToolBar, QStatusBar, QLabel,
    QFileDialog, QComboBox, QGridLayout, QWidget
)
from PySide6.QtGui import (
    QAction
)
from PySide6.QtCore import Qt
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

import pyabf
import re
import os
import numpy as np
from pathlib import Path

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        ## declared variables
        self.dir_path = "None selected"  # folder with data
        self.climatedata_path = "location of weatherstats_ottawa_hourly.csv"
        self.filelist = ["Select Folder"]
        self.filelistindex = None

        self.setWindowTitle("Room 3507 - environment data")

        layout = QGridLayout()

        toolbar = QToolBar("Function toolbar")
        self.addToolBar(toolbar)
        self.folderbuttonsetup()
        toolbar.addAction(self.folderbutton)
        self.setStatusBar(QStatusBar(self))

        self.filebox = QComboBox()
        self.filebox.addItems(self.filelist)
        layout.addWidget(self.filebox, 0, 0, 1, 2)

        self.tracelabel = QLabel("Sweep number :")
        layout.addWidget(self.tracelabel, 0, 2)

        self.sweepslider = QSpinBox()
        self.sweepslider.setMinimum(0)
        self.sweepslider.setSingleStep(1)
        layout.addWidget(self.sweepslider, 0, 3, 1, 2)

        self.pw = pg.PlotWidget(name='Clamp')  ## giving the plots names allows us to link their axes together
        layout.addWidget(self.pw, 1, 0, 2, 5)
        self.pw2 = pg.PlotWidget(name='ClampZoom')  ## giving the plots names allows us to link their axes together
        layout.addWidget(self.pw2, 1, 6, 2, 5)
        self.pw3 = pg.PlotWidget(name='Stim')
        layout.addWidget(self.pw3, 6, 0, 2, 5)
        self.pw3.setXLink(self.pw)
        self.pw4 = pg.PlotWidget(name='StimZoom')
        layout.addWidget(self.pw4, 6, 6, 2, 5)
        self.pw4.setXLink(self.pw2)

        self.pw.setBackground('w')
        self.pw2.setBackground('w')
        self.pw3.setBackground('w')
        self.pw4.setBackground('w')

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def folderbuttonsetup(self):
        self.folderbutton = QAction("Folder", self)
        self.folderbutton.setStatusTip(self.dir_path)
        self.folderbutton.triggered.connect(self.folderselect)

    def folderselect(self):
        print("click")
        print(self.dir_path)
        self.dir_path = QFileDialog.getExistingDirectory()
        self.folderbutton.setStatusTip(self.dir_path)
        print(self.dir_path)
        self.fileboxlist()

    def fileboxlist(self):
        print('Files within experiment date folder')
        print('ISOLATING ABF FILES...')
        self.dir_path_1 = self.dir_path[2:] + "/"
        self.fileinfolder = os.listdir(self.dir_path_1)
        self.abffiles = [extension for extension in self.fileinfolder if re.search("\.abf$", extension)]
        self.abffiles.sort()
        print('*.abf files in folder:')
        print(self.abffiles)
        self.filebox.clear()
        self.filebox.currentTextChanged.connect(self.fileselected)

        self.filelist = self.abffiles
        self.filebox.addItems(self.filelist)

    def fileselected(self, s):
        print("yo")
        print(s)
        self.fileselected_1 = self.dir_path_1 + s
        print(self.fileselected_1)

        self.pw.clear()
        self.pw2.clear()
        self.pw3.clear()
        self.pw4.clear()

        self.loadabf(self.fileselected_1)

    def loadabf(self, filetoload):
        print("load file")
        self.abf = pyabf.ABF(filetoload)
        self.numsweep = self.abf.sweepCount - 1
        self.sweepslider.cleanText()
        self.sweepslider.setMaximum(self.numsweep)
        self.sweepslider.valueChanged.connect(self.setsweep)

        self.pw.setLabel('left', self.abf.sweepLabelY)
        self.pw.setLabel('bottom', self.abf.sweepLabelX)
        self.pw2.setLabel('left', self.abf.sweepLabelY)
        self.pw2.setLabel('bottom', self.abf.sweepLabelX)
        self.pw3.setLabel('left', self.abf.sweepLabelY)
        self.pw3.setLabel('bottom', self.abf.sweepLabelX)
        self.pw4.setLabel('left', self.abf.sweepLabelY)
        self.pw4.setLabel('bottom', self.abf.sweepLabelX)

        self.zoomarea = pg.LinearRegionItem([0, 1])
        self.zoomarea.setZValue(-10)
        self.pw.addItem(self.zoomarea)

        for sweepnum in self.abf.sweepList:
            self.abf.setSweep(sweepnum, channel=0)
            self.pw.plot(self.abf.sweepX, self.abf.sweepY, pen=pg.mkPen('black', width=1))

        for sweepnum in self.abf.sweepList:
            self.abf.setSweep(sweepnum, channel=1)
            self.pw3.plot(self.abf.sweepX, self.abf.sweepC, pen=pg.mkPen('black', width=1))

        for sweepnum in self.abf.sweepList:
            self.abf.setSweep(sweepnum, channel=0)
            self.pw2.plot(self.abf.sweepX, self.abf.sweepY, pen=pg.mkPen('black', width=1))

        for sweepnum in self.abf.sweepList:
            self.abf.setSweep(sweepnum, channel=1)
            self.pw4.plot(self.abf.sweepX, self.abf.sweepC, pen=pg.mkPen('black', width=1))

        def updatePlot():
            self.pw2.setXRange(*self.zoomarea.getRegion(), padding=0)

        def updateRegion():
            self.zoomarea.setRegion(self.pw2.getViewBox().viewRange()[0])

        self.zoomarea.sigRegionChanged.connect(updatePlot)
        self.pw2.sigXRangeChanged.connect(updateRegion)
        updatePlot()

        self.currenttrace = self.pw.plot()
        self.currenttrace.setPen(pg.mkPen('r', width=2.5))
        self.currenttrace2 = self.pw2.plot()
        self.currenttrace2.setPen(pg.mkPen('r', width=2.5))
        self.currenttrace3 = self.pw3.plot()
        self.currenttrace3.setPen(pg.mkPen('r', width=2.5))
        self.currenttrace4 = self.pw4.plot()
        self.currenttrace4.setPen(pg.mkPen('r', width=2.5))

    def setsweep(self, numofsweep):
        print(numofsweep)
        self.currenttrace.clear()
        self.currenttrace2.clear()
        self.currenttrace3.clear()
        self.currenttrace4.clear()
        for sweepnum in self.abf.sweepList:
            self.abf.setSweep(sweepnum, channel=0)
            if sweepnum == numofsweep:
                self.currenttrace.setData(self.abf.sweepX, self.abf.sweepY)
        for sweepnum in self.abf.sweepList:
            self.abf.setSweep(sweepnum, channel=1)
            if sweepnum == numofsweep:
                self.currenttrace3.setData(self.abf.sweepX, self.abf.sweepC)
        for sweepnum in self.abf.sweepList:
            self.abf.setSweep(sweepnum, channel=0)
            if sweepnum == numofsweep:
                self.currenttrace2.setData(self.abf.sweepX, self.abf.sweepY)
        for sweepnum in self.abf.sweepList:
            self.abf.setSweep(sweepnum, channel=1)
            if sweepnum == numofsweep:
                self.currenttrace4.setData(self.abf.sweepX, self.abf.sweepC)



app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec_()
