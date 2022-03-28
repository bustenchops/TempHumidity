# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'TempHumid3507rjLNpQ.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide6.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1300, 800)

        #Setup action for selection data folder
        self.actionData_Folder = QAction(MainWindow)
        self.actionData_Folder.setObjectName(u"actionData_Folder")
        # Setup action for selection of climate file
        self.actionClimate_File = QAction(MainWindow)
        self.actionClimate_File.setObjectName(u"actionClimate_File")
        # Setup action for starting the update of the climate data
        self.action_Update_Climate_Data = QAction(MainWindow)
        self.action_Update_Climate_Data.setObjectName(u"action_Update_Climate_Data")
        # Setup action for clickable options to graph
        self.actionTemp = QAction(MainWindow)
        self.actionTemp.setObjectName(u"actionTemp")
        self.actionTemp.setCheckable(True)
        self.actionHumid = QAction(MainWindow)
        self.actionHumid.setObjectName(u"actionHumid")
        self.actionHumid.setCheckable(True)
        self.actionBaro = QAction(MainWindow)
        self.actionBaro.setObjectName(u"actionBaro")
        self.actionBaro.setCheckable(True)
        # Setup action for initiating graph
        self.actionGRAPH = QAction(MainWindow)
        self.actionGRAPH.setObjectName(u"actionGRAPH")
        # Setup action for selection of HDF file
        self.actionHDF_File = QAction(MainWindow)
        self.actionHDF_File.setObjectName(u"actionHDF_File")

        # Setup central widget and layout
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 10, 1300, 800))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        #Put graph widget 1 here
        self.lineEdit = QLineEdit(self.verticalLayoutWidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)

        #Put graph wigdet 2 here
        self.lineEdit_2 = QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.verticalLayout.addWidget(self.lineEdit_2)

        #Init the central widget
        MainWindow.setCentralWidget(self.centralwidget)

        #Setup toolbar
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.toolBar.addAction(self.actionHDF_File)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionData_Folder)
        self.toolBar.addSeparator()
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionGRAPH)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionTemp)
        self.toolBar.addAction(self.actionHumid)
        self.toolBar.addAction(self.actionBaro)
        self.toolBar.addSeparator()
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionClimate_File)
        self.toolBar.addSeparator()
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_Update_Climate_Data)

        #Setup status bar
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)



        self.retranslateUi(MainWindow)
        self.actionTemp.changed.connect(self.lineEdit.clear)

        app = QApplication(sys.argv)
        w = MainWindow()
        w.show()
        app.exec_()


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Room 3507 - Environment Data", None))
        self.actionData_Folder.setText(QCoreApplication.translate("MainWindow", u"Data Folder", None))
        self.actionClimate_File.setText(QCoreApplication.translate("MainWindow", u"Climate File", None))
        self.action_Update_Climate_Data.setText(QCoreApplication.translate("MainWindow", u"!Update Climate Data!", None))
#if QT_CONFIG(tooltip)
        self.action_Update_Climate_Data.setToolTip(QCoreApplication.translate("MainWindow", u"Update Climate Data", None))
#endif // QT_CONFIG(tooltip)
        self.actionTemp.setText(QCoreApplication.translate("MainWindow", u"Temp", None))
        self.actionHumid.setText(QCoreApplication.translate("MainWindow", u"Humid", None))
#if QT_CONFIG(tooltip)
        self.actionHumid.setToolTip(QCoreApplication.translate("MainWindow", u"Humid", None))
#endif // QT_CONFIG(tooltip)
        self.actionBaro.setText(QCoreApplication.translate("MainWindow", u"Baro", None))
#if QT_CONFIG(tooltip)
        self.actionBaro.setToolTip(QCoreApplication.translate("MainWindow", u"Baro", None))
#endif // QT_CONFIG(tooltip)
        self.actionGRAPH.setText(QCoreApplication.translate("MainWindow", u"GRAPH", None))
        self.actionHDF_File.setText(QCoreApplication.translate("MainWindow", u"HDF File", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

