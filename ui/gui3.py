# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui3.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from LexicalAnalysis import *
from SyntaxAnalysis import *
import pickle

# 太恶心了太恶心了，解决报错居然要把类定义原封不动复制过来
# 真的太恶心了
class _node:
    def __init__(self, order: int, number: int):
        self.order = order
        self.number = number
        self.next = {}

    def add_node(self, symbol: Edge, other_node):
        if symbol in self.next:
            self.next[symbol].append(other_node)
        else:
            self.next[symbol] = [other_node]

    def __repr__(self):
        return '-node_' + str(self.order) + '-' + str(self.number) + '-'

    def __str(self):
        return self.__repr__()

    def __eq__(self, other):
        return other.number == self.number and self.order == other.order

    def __hash__(self):
        return self.number + (self.order + 11221234) * 123

    def __lt__(self, other):
        if self.order == other.order:
            return self.number < other.number
        else:
            return self.order < other.order

    def __le__(self, other):
        if self.order == other.order:
            return self.number <= other.number
        else:
            return self.order <= other.order

    def __gt__(self, other):
        if self.order == other.order:
            return self.number > other.number
        else:
            return self.order > other.order

    def __ge__(self, other):
        if self.order == other.order:
            return self.number >= other.number
        else:
            return self.order >= other.order



class Ui_MainWindow(QMainWindow):
    def __init__(self, MainWindow):
        super().__init__()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1339, 853)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(649, 29, 681, 581))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.tableView = QtWidgets.QTableView(self.gridLayoutWidget)
        self.tableView.setObjectName("tableView")
        self.gridLayout.addWidget(self.tableView, 2, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
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
        self.pushButton_2.clicked.connect(self.Analyze)
        self.verticalLayout.addWidget(self.pushButton_2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.readCode)
        self.verticalLayout.addWidget(self.pushButton)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.pushButton_4 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.readFA)
        self.verticalLayout.addWidget(self.pushButton_4)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.pushButton_3 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout.addWidget(self.pushButton_3)
        spacerItem3 = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.label_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.CodeWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.CodeWidget.setGeometry(QtCore.QRect(150, 20, 481, 781))
        self.CodeWidget.setObjectName("CodeWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        # 源代码
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.tab)
        self.plainTextEdit.setGeometry(QtCore.QRect(0, 0, 471, 751))
        self.plainTextEdit.setFrameShape(QtWidgets.QFrame.Panel)
        self.plainTextEdit.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.CodeWidget.addTab(self.tab, "")

        # FA转换表
        self.FA_table = QtWidgets.QWidget()
        self.FA_table.setObjectName("FA_table")
        self.tableView_3 = QtWidgets.QTableView(self.FA_table)
        self.tableView_3.setGeometry(QtCore.QRect(0, 0, 471, 751))
        self.tableView_3.setObjectName("tableView_3")
        self.CodeWidget.addTab(self.FA_table, "")
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
        self.CodeWidget.setCurrentIndex(1)
        self.pushButton.clicked.connect(self.pushButton.showMenu)
        self.pushButton_4.clicked.connect(self.pushButton_4.showMenu)
        self.pushButton_3.clicked.connect(self.pushButton_3.showMenu)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def getLexAnalyzer(self, LA: e_NFA):
        self.Lexical_Analyzer = LA

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "符号表"))
        self.label.setText(_translate("MainWindow", "词法分析结果"))
        self.pushButton_2.setText(_translate("MainWindow", "词法分析"))
        self.pushButton.setText(_translate("MainWindow", "读取待分析代码"))
        self.pushButton_4.setText(_translate("MainWindow", "读取FA转换表"))
        self.pushButton_3.setText(_translate("MainWindow", "读取词法正则"))
        self.label_4.setText(_translate("MainWindow", "当前状态:未读取FA转换表"))
        self.CodeWidget.setTabText(self.CodeWidget.indexOf(self.tab), _translate("MainWindow", "Source Code"))
        self.CodeWidget.setTabText(self.CodeWidget.indexOf(self.FA_table), _translate("MainWindow", "FA_Table"))
        self.label_3.setText(_translate("MainWindow", "错误信息"))
        self.actionSyntax.setText(_translate("MainWindow", "Syntax"))
        self.actionRead_FA_File.setText(_translate("MainWindow", "Read FA File"))

    def show_getFA_Dialog1(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '.')
        if fname[0]:
            f = open(fname[0], 'r')
            with f:
                data = f.read()
                # self.textEdit.setText(data)
                self.plainTextEdit.setPlainText(data)

    def Analyze(self):
        codes = self.plainTextEdit.toPlainText()
        original, lexical, id_table = nfa.Lexical(codes)
        tmodel = QStandardItemModel(len(lexical), 2)
        tmodel.setHorizontalHeaderLabels(['原文', '词法'])
        for row in range(len(lexical)):
            if len(lexical[row]) == 3:
                item1 = QStandardItem(lexical[row][0])
                item1.setForeground(QtGui.QBrush(QtGui.QColor(255, 0, 0)))
                item2 = QStandardItem('ERROR!')
                item2.setForeground(QtGui.QBrush(QtGui.QColor(255, 0, 0)))
            elif isinstance(lexical[row][1], int):
                item1 = QStandardItem(original[row])
                item2 = QStandardItem('<' + lexical[row][0] + ',' + str(id_table[lexical[row][1]]) + '>')
            else:
                item1 = QStandardItem(original[row])
                item2 = QStandardItem('<' + lexical[row][0] + ',' + str(lexical[row][1]) + '>')
            tmodel.setItem(row, 0, item1)
            tmodel.setItem(row, 1, item2)
        self.tableView_2.setModel(tmodel)
        symboltabel = QStandardItemModel(len(id_table), 1)
        symboltabel.setHorizontalHeaderLabels(['序号', '符号'])
        for (key, value) in id_table.items():
            item1 = QStandardItem(str(key))
            item2 = QStandardItem(value)
            symboltabel.setItem(key, 0, item2)
        self.tableView.setModel(symboltabel)

    # 读取待分析代码
    def readCode(self):
        fname = QFileDialog.getOpenFileName(self, 'Open Source Code file', '.')
        if fname[0]:
            f = open(fname[0], 'r')
            with f:
                data = f.read()
                self.plainTextEdit.setPlainText(data)

    # 读取FA转换表
    def readFA(self):
        fname = QFileDialog.getOpenFileName(self, 'Open DFA file', '.dfa')
        if fname[0]:
            print(fname)
            nfa.read(fname[0])
            print('here2 ' + fname[0])
            FAT, symbol_index = nfa.str_table()
            symbols = []
            for (key, value) in symbol_index.items():
                symbols.append(key)
            tmodel = QStandardItemModel(len(FAT), len(symbols))
            # 设置水平方向四个头标签文本内容
            tmodel.setHorizontalHeaderLabels(symbols)
            for row in range(len(FAT)):
                for column in range(len(symbols)):
                    current_symbol = symbols[column]
                    if current_symbol in FAT[row]:
                        item = QStandardItem(str(FAT[row][current_symbol]))
                    else:
                        item = QStandardItem('_')
                    # 设置每个位置的文本值
                    tmodel.setItem(row, column, item)
            self.tableView_3.setModel(tmodel)
            _translate = QtCore.QCoreApplication.translate
            self.label_4.setText(_translate("MainWindow", "当前状态:已读取FA转换表"))
            # f = open(fname[0], 'r')
            # with f:
            #     data = f.read()
            #     self.textEdit.setText(data)
                # self.plainTextEdit.setPlainText(data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui = Ui_MainWindow(mainWindow)
    # ui.getLexAnalyzer(e_NFA())
    nfa = e_NFA()
    # ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())