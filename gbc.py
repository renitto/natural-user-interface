
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'f2.ui'
#
# Created: Tue Apr  5 21:33:39 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import os,sys,csv
class Ui_MainWindow(QtGui.QMainWindow):
    def __init__(self):
	QtGui.QMainWindow.__init__(self)
	self.setupUi(self)
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 375)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(250, 20, 151, 41))
        self.label.setStyleSheet("background-color: rgb(85, 85, 127);")
        self.label.setObjectName("label")
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(540, 0, 51, 31))
        self.pushButton.setObjectName("pushButton")
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 100, 161, 21))
        self.label_2.setStyleSheet("background-color: rgb(85, 85, 127);")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(450, 100, 141, 21))
        self.label_3.setStyleSheet("background-color: rgb(85, 85, 127);\n")
        self.label_3.setObjectName("label_3")
        self.comboBox = QtGui.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(20, 140, 161, 27))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox_2 = QtGui.QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(450, 140, 141, 31))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(20, 190, 161, 21))
        self.label_4.setStyleSheet("background-color: rgb(85, 85, 127);")
        self.label_4.setObjectName("label_4")
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(450, 190, 141, 21))
        self.label_5.setStyleSheet("background-color: rgb(85, 85, 127);")
        self.label_5.setObjectName("label_5")
        self.comboBox_3 = QtGui.QComboBox(self.centralwidget)
        self.comboBox_3.setGeometry(QtCore.QRect(20, 230, 161, 27))
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(450, 230, 141, 27))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton_3 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(275, 140, 98, 27))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(260, 230, 125, 27))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(100, 300, 121, 27))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(240, 300, 141, 27))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_7 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(400, 300, 161, 27))
        self.pushButton_7.setObjectName("pushButton_7")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 411, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
	QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("clicked()"), self.quit)
        QtCore.QObject.connect(self.pushButton_3, QtCore.SIGNAL("clicked()"), self.storesettings)
	QtCore.QObject.connect(self.pushButton_4, QtCore.SIGNAL("clicked()"), self.storedefsettings)
	QtCore.QObject.connect(self.pushButton_5, QtCore.SIGNAL("clicked()"), self.launchgbc)
 	QtCore.QObject.connect(self.pushButton_6, QtCore.SIGNAL("clicked()"), self.launchab)
	QtCore.QObject.connect(self.pushButton_7, QtCore.SIGNAL("clicked()"), self.pptviewer)

    def storesettings(self):
	wr=csv.writer(open('gbc.csv','wb'), delimiter=' ', quotechar='|',quoting=csv.QUOTE_MINIMAL)
	mp=self.comboBox.currentText().__str__()
	mpl=["Totem Movie Player","VLC Media Player", "Xine Media Player", "GNOME MPlayer"]
	mpc=["totem", "vlc", "xine", "gnome-mplayer"]
	for i in range(0,len(mpl)):
		if mp==mpl[i]:
			wr.writerow([str(mpc[i])])
			break
	iv=self.comboBox_2.currentText().__str__()
	ivl=["Eye Of GNOME","F-Spot Photo Manager","Shotwell Photo Manager", "Inkscape", "GIMP"]
	ivc=["eog", "f-spot","shotwell", "inkscape","gimp"]
	
	for i in range(0,len(ivl)):
		if iv==ivl[i]:
			#print ivc[i]
			wr.writerow([str(ivc[i])])
			break
	bv=self.comboBox_3.currentText().__str__()
	brl=["Chromium","Opera","Mozilla Firefox","Sea Monkey"]
	brc=["chromium-browser","opera","firefox","seamonkey"]
	
	for i in range(0,len(brl)):
		if bv==brl[i]:
			#print brc[i]
			wr.writerow([str(brc[i])])
			break
	el=self.lineEdit.text().__str__()
	
	wr.writerow([str(el)])

    def storedefsettings(self):
	
	wr=csv.writer(open('gbc.csv','wb'), delimiter=' ', quotechar='|',quoting=csv.QUOTE_MINIMAL)
	mp="totem"
	iv="eog"
	bv="chromium-browser"
	el="~"
	self.lineEdit.setText(el)
	
	wr.writerow([mp])
	wr.writerow([iv])
	wr.writerow([bv])
	wr.writerow([el])
	
    
    def quit(self):
	os.system('pkill python')
	os.system('pkill WorldOfGoo.bin32')
	sys.exit(0)

    def launchgbc(self):
	print "Start Gestures"
	os.system('python ~/gbc/gestures.py &')
   
    def pptviewer(self):
	print"Launching Ppt viwer"
	os.system('python ~/gbc/ppt.py &')
	

    def launchab(self):
	print"Launching Angry Birds"
	os.system('python ~/gbc/ab.py &')
        


    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Gesture Based Computing", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600; color:#ffffff;\">Settings Manager</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">Media Player</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">Image Viewer</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(0, QtGui.QApplication.translate("MainWindow", "Totem Movie Player", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(1, QtGui.QApplication.translate("MainWindow", "VLC Media Player", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(2, QtGui.QApplication.translate("MainWindow", "Xine Media Player", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(3, QtGui.QApplication.translate("MainWindow", "GNOME MPlayer", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_2.setItemText(0, QtGui.QApplication.translate("MainWindow", "Eye Of GNOME", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_2.setItemText(1, QtGui.QApplication.translate("MainWindow", "GIMP", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_2.setItemText(2, QtGui.QApplication.translate("MainWindow", "F-Spot Photo Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_2.setItemText(3, QtGui.QApplication.translate("MainWindow", "Shotwell Photo Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_2.setItemText(4, QtGui.QApplication.translate("MainWindow", "Inkscape", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">Browser</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">Explorer Location</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_3.setItemText(0, QtGui.QApplication.translate("MainWindow", "Chromium Browser", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_3.setItemText(1, QtGui.QApplication.translate("MainWindow", "Opera", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_3.setItemText(2, QtGui.QApplication.translate("MainWindow", "Mozilla Firefox", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_3.setItemText(3, QtGui.QApplication.translate("MainWindow", "Sea Monkey", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit.setText(QtGui.QApplication.translate("MainWindow", "~", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_3.setText(QtGui.QApplication.translate("MainWindow", "Apply", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_4.setText(QtGui.QApplication.translate("MainWindow", "Reset To Defaults", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_5.setText(QtGui.QApplication.translate("MainWindow", "Start Gesturing", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_6.setText(QtGui.QApplication.translate("MainWindow", "Start Angry Birds", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_7.setText(QtGui.QApplication.translate("MainWindow", "Pptviwer", None, 
QtGui.QApplication.UnicodeUTF8))

app=QtGui.QApplication(sys.argv)
obj=Ui_MainWindow()
obj.show()
sys.exit(app.exec_())
