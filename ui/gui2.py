# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui2.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
import LexicalAnalysis


class Ui_MainWindow(QMainWindow):
    def __init__(self, MainWindow):
        super().__init__()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1339, 853)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(649, 29, 681, 581))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.tableView = QtWidgets.QTableView(self.gridLayoutWidget)
        self.tableView.setObjectName("tableView")
        self.gridLayout.addWidget(self.tableView, 2, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.tableView_2 = QtWidgets.QTableView(self.gridLayoutWidget)
        self.tableView_2.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.tableView_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.tableView_2.setGridStyle(QtCore.Qt.SolidLine)
        self.tableView_2.setObjectName("tableView_2")
        self.gridLayout.addWidget(self.tableView_2, 2, 0, 1, 1)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 131, 771))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.showDialog1)
        self.verticalLayout.addWidget(self.pushButton_2)
        self.pushButton_4 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.showDialog1)
        self.verticalLayout.addWidget(self.pushButton_4)
        self.pushButton_3 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout.addWidget(self.pushButton_3)
        self.CodeWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.CodeWidget.setGeometry(QtCore.QRect(150, 20, 481, 781))
        self.CodeWidget.setObjectName("CodeWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.tab)
        self.plainTextEdit.setGeometry(QtCore.QRect(0, 0, 471, 751))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.CodeWidget.addTab(self.tab, "")
        self.FA_table = QtWidgets.QWidget()
        self.FA_table.setObjectName("FA_table")
        self.tableView_3 = QtWidgets.QTableView(self.FA_table)
        self.tableView_3.setGeometry(QtCore.QRect(0, 0, 471, 751))
        self.tableView_3.setObjectName("tableView_3")
        self.CodeWidget.addTab(self.FA_table, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.CodeWidget.addTab(self.tab_2, "")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(650, 620, 671, 181))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(self.verticalLayoutWidget_2)
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        self.verticalLayout_2.addWidget(self.plainTextEdit_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1339, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSyntax = QtWidgets.QAction(MainWindow)
        self.actionSyntax.setObjectName("actionSyntax")
        self.actionRead_FA_File = QtWidgets.QAction(MainWindow)
        self.actionRead_FA_File.setObjectName("actionRead_FA_File")

        self.retranslateUi(MainWindow)
        self.CodeWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "词法分析结果"))
        self.label_2.setText(_translate("MainWindow", "符号表"))
        self.pushButton_2.setText(_translate("MainWindow", "词法分析"))
        self.pushButton_4.setText(_translate("MainWindow", "读取FA转换表"))
        self.pushButton_3.setText(_translate("MainWindow", "读取词法正则"))
        self.CodeWidget.setTabText(self.CodeWidget.indexOf(self.tab), _translate("MainWindow", "Source Code"))
        self.CodeWidget.setTabText(self.CodeWidget.indexOf(self.FA_table), _translate("MainWindow", "FA_Table"))
        self.CodeWidget.setTabText(self.CodeWidget.indexOf(self.tab_2), _translate("MainWindow", "Page"))
        self.label_3.setText(_translate("MainWindow", "错误信息"))
        self.actionSyntax.setText(_translate("MainWindow", "Syntax"))
        self.actionRead_FA_File.setText(_translate("MainWindow", "Read FA File"))

    def Lexical_a(self):
        pass

    # 定义打开文件夹目录的函数
    def showDialog1(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '.')
        if fname[0]:
            f = open(fname[0], 'r')
            with f:
                data = f.read()
                # self.textEdit.setText(data)
                self.plainTextEdit.setPlainText(data)

app = QApplication(sys.argv)
mainWindow = QMainWindow()
ui = Ui_MainWindow(mainWindow)
# ui.setupUi(mainWindow)
mainWindow.show()
sys.exit(app.exec_())