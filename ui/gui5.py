# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui5.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
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
        MainWindow.resize(1346, 953)
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
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.line_8 = QtWidgets.QFrame(self.gridLayoutWidget)
        self.line_8.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.gridLayout.addWidget(self.line_8, 1, 0, 1, 1)
        self.tableView_2 = QtWidgets.QTableView(self.gridLayoutWidget)
        self.tableView_2.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.tableView_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.tableView_2.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.tableView_2.setGridStyle(QtCore.Qt.SolidLine)
        self.tableView_2.setObjectName("tableView_2")
        self.gridLayout.addWidget(self.tableView_2, 3, 0, 1, 1)
        self.line_6 = QtWidgets.QFrame(self.gridLayoutWidget)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.line_6.setLineWidth(3)
        self.line_6.setMidLineWidth(3)
        self.line_6.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_6.setObjectName("line_6")
        self.gridLayout.addWidget(self.line_6, 3, 1, 1, 1)
        self.tableView = QtWidgets.QTableView(self.gridLayoutWidget)
        self.tableView.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.tableView.setObjectName("tableView")
        self.gridLayout.addWidget(self.tableView, 3, 2, 1, 1)
        self.line_9 = QtWidgets.QFrame(self.gridLayoutWidget)
        self.line_9.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9.setObjectName("line_9")
        self.gridLayout.addWidget(self.line_9, 1, 2, 1, 1)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 131, 771))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.line_4 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.verticalLayout.addWidget(self.line_4)
        self.pushButton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setObjectName("pushButton_2")
        # 词法分析按钮
        self.pushButton_2.clicked.connect(self.Analyze)
        self.verticalLayout.addWidget(self.pushButton_2)
        self.line = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setObjectName("pushButton")
        # 读取待分析代码按钮
        self.pushButton.clicked.connect(self.readCode)
        self.verticalLayout.addWidget(self.pushButton)
        self.line_2 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.pushButton_4 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_4.sizePolicy().hasHeightForWidth())
        self.pushButton_4.setSizePolicy(sizePolicy)
        self.pushButton_4.setObjectName("pushButton_4")
        # 读取FA转换表按钮
        self.pushButton_4.clicked.connect(self.readFA)
        self.verticalLayout.addWidget(self.pushButton_4)
        self.line_3 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout.addWidget(self.line_3)
        self.pushButton_3 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.readRegex)
        self.verticalLayout.addWidget(self.pushButton_3)
        self.line_5 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.verticalLayout.addWidget(self.line_5)
        self.CodeWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.CodeWidget.setGeometry(QtCore.QRect(150, 20, 481, 781))
        self.CodeWidget.setObjectName("CodeWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.tab)
        self.plainTextEdit.setGeometry(QtCore.QRect(0, 0, 471, 751))
        self.plainTextEdit.setFrameShape(QtWidgets.QFrame.Panel)
        self.plainTextEdit.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.CodeWidget.addTab(self.tab, "")
        self.FA_table = QtWidgets.QWidget()
        self.FA_table.setObjectName("FA_table")
        self.tableView_3 = QtWidgets.QTableView(self.FA_table)
        self.tableView_3.setGeometry(QtCore.QRect(0, 0, 471, 751))
        self.tableView_3.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.tableView_3.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.tableView_3.setObjectName("tableView_3")
        self.CodeWidget.addTab(self.FA_table, "")
        self.Regex_Tab = QtWidgets.QWidget()
        self.Regex_Tab.setObjectName("Regex_Tab")
        self.plainTextEdit_3 = QtWidgets.QPlainTextEdit(self.Regex_Tab)
        self.plainTextEdit_3.setGeometry(QtCore.QRect(0, 0, 471, 691))
        self.plainTextEdit_3.setObjectName("plainTextEdit_3")
        self.pushButton_5 = QtWidgets.QPushButton(self.Regex_Tab)
        self.pushButton_5.setGeometry(QtCore.QRect(140, 700, 171, 41))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(self.write_FA)
        self.CodeWidget.addTab(self.Regex_Tab, "")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(650, 620, 671, 181))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.line_7 = QtWidgets.QFrame(self.verticalLayoutWidget_2)
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.verticalLayout_2.addWidget(self.line_7)
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(self.verticalLayoutWidget_2)
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        self.verticalLayout_2.addWidget(self.plainTextEdit_2)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 820, 1311, 61))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_4 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setFrameShape(QtWidgets.QFrame.Panel)
        self.label_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label_4.setLineWidth(5)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1346, 26))
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
        self.pushButton.clicked.connect(self.pushButton.showMenu)
        self.pushButton_4.clicked.connect(self.pushButton_4.showMenu)
        self.pushButton_3.clicked.connect(self.pushButton_3.showMenu)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "C29编译器"))
        self.label_2.setText(_translate("MainWindow", "符号表"))
        self.label.setText(_translate("MainWindow", "词法分析结果"))
        self.pushButton_2.setText(_translate("MainWindow", "词法分析"))
        self.pushButton.setText(_translate("MainWindow", "读取待分析代码"))
        self.pushButton_4.setText(_translate("MainWindow", "读取FA转换表"))
        self.pushButton_3.setText(_translate("MainWindow", "读取词法正则"))
        self.CodeWidget.setTabText(self.CodeWidget.indexOf(self.tab), _translate("MainWindow", "待分析代码"))
        self.CodeWidget.setTabText(self.CodeWidget.indexOf(self.FA_table), _translate("MainWindow", "FA转换表"))
        self.pushButton_5.setText(_translate("MainWindow", "生成FA转换表"))
        self.CodeWidget.setTabText(self.CodeWidget.indexOf(self.Regex_Tab), _translate("MainWindow", "词法"))
        self.label_3.setText(_translate("MainWindow", "错误信息"))
        self.label_4.setText(_translate("MainWindow", "当前使用的词法："))
        self.actionSyntax.setText(_translate("MainWindow", "Syntax"))
        self.actionRead_FA_File.setText(_translate("MainWindow", "Read FA File"))

    def getLexAnalyzer(self, LA: e_NFA):
        self.Lexical_Analyzer = LA

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
        self.plainTextEdit_2.setPlainText('')
        for row in range(len(lexical)):
            if len(lexical[row]) == 3:
                item1 = QStandardItem(lexical[row][0])
                item1.setForeground(QtGui.QBrush(QtGui.QColor(255, 0, 0)))
                item2 = QStandardItem('ERROR!')
                item2.setForeground(QtGui.QBrush(QtGui.QColor(255, 0, 0)))
                pastinfp = self.plainTextEdit_2.toPlainText()
                cur = '发生错误！' + lexical[row][1] + '-行号：' + str(lexical[row][2]) + ', 错误符号:' + str(lexical[row][0]) + '\n'
                self.plainTextEdit_2.setPlainText(pastinfp + cur)
            elif isinstance(lexical[row][1], int):
                item1 = QStandardItem(original[row])
                item2 = QStandardItem('<' + lexical[row][0] + ',' + str(id_table[lexical[row][1]]) + '>')
            else:
                item1 = QStandardItem(original[row])
                if len(lexical[row][1]) == 0:
                    string = ''
                elif lexical[row][1][-1] == '\'':
                    string = '\'' + lexical[row][1]
                elif lexical[row][1][-1] == '\"':
                    string = '\"' + lexical[row][1]
                else:
                    string = str(lexical[row][1])
                item2 = QStandardItem('<' + lexical[row][0] + ',' + string + '>')
            tmodel.setItem(row, 0, item1)
            tmodel.setItem(row, 1, item2)
        self.tableView_2.setModel(tmodel)
        symboltabel = QStandardItemModel(len(id_table), 1)
        symboltabel.setHorizontalHeaderLabels(['符号'])
        for (key, value) in id_table.items():
            item1 = QStandardItem(str(key))
            item2 = QStandardItem(value)
            symboltabel.setItem(key, 0, item2)
        self.tableView.setModel(symboltabel)

    # 读取待分析代码
    def readCode(self):
        fname = QFileDialog.getOpenFileName(self, 'Open Source Code file', '.')
        if fname[0]:
            f = open(fname[0], 'r', encoding='utf-8')
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

    def readRegex(self):
        fname = QFileDialog.getOpenFileName(self, 'Open Regex file', '.')
        if fname[0]:
            f = open(fname[0], 'r', encoding='utf-8')
            self.plainTextEdit_3.setPlainText(f.read())
            f.close()

    def write_FA(self):
        fname = QFileDialog.getSaveFileName(self, 'Save generated FA table', '.dfa')
        if fname[0]:
            print(fname)
            data = self.plainTextEdit_3.toPlainText()
            lines = data.split('\n')
            try:
                nfa.compile(lines) # TODO
            except:
                QMessageBox.information(self, '错误', '正则文法中出现错误！', QMessageBox.Yes)
                return
            nfa.write(fname[0])
            nfa.read(fname[0])

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui = Ui_MainWindow(mainWindow)
    # ui.getLexAnalyzer(e_NFA())
    nfa = e_NFA()
    # ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())