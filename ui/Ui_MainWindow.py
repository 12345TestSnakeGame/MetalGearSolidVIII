# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QFileDialog, QApplication, QPushButton, QWidget, \
    QGridLayout
from PyQt5.QtGui import QIcon


class MainUi(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setFixedSize(960, 700)
        self.main_widget = QWidget()  # 创建窗口主部件
        self.main_layout = QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局

        self.up_widget = QWidget()  # 创建上侧部件
        self.up_widget.setObjectName('up_widget')
        self.up_layout = QGridLayout()  # 创建左侧部件的网格布局
        self.up_widget.setLayout(self.up_layout)  # 设置左侧部件布局为网格布局

        self.down_widget = QWidget()  # 创建下侧部件
        self.down_widget.setObjectName('down_widget')
        self.down_layout = QGridLayout()  # 创建右侧部件的网格布局
        self.down_widget.setLayout(self.down_layout)  # 设置右侧部件布局为网格布局

        self.main_layout.addWidget(self.up_widget, 0, 0, 1, 12)
        self.main_layout.addWidget(self.down_widget, 1, 0, 10, 12)
        self.setCentralWidget(self.main_widget)  # 设置窗口主部件

        self.button1 = QPushButton(QIcon(''), '打开文件')  # 创建按钮
        self.main_layout.addWidget(self.button1, 0, 0,1,1.5)

        self.button2 = QPushButton(QIcon(''), '词法规则')  # 创建按钮
        self.main_layout.addWidget(self.button2, 0, 1.5, 1,1.5)

        self.button3 = QPushButton(QIcon(''), '词法分析')  # 创建按钮
        self.main_layout.addWidget(self.button3, 0, 3, 1,1.5)

        self.button4 = QPushButton(QIcon(''), '语法规则')  # 创建按钮
        self.main_layout.addWidget(self.button4, 0, 4.5, 1, 1.5)

        self.button5 = QPushButton(QIcon(''), '语法分析')  # 创建按钮
        self.main_layout.addWidget(self.button5, 0, 6, 1, 1.5)

        self.button6 = QPushButton(QIcon(''), '语义规则')  # 创建按钮
        self.main_layout.addWidget(self.button6, 0, 7.5, 1, 1.5)

        self.button7 = QPushButton(QIcon(''), '语义分析')  # 创建按钮
        self.main_layout.addWidget(self.button7, 0, 9, 1, 1.5)

        self.button8 = QPushButton(QIcon(''), '清空界面')  # 创建按钮
        self.main_layout.addWidget(self.button8, 0, 10.5, 1, 1.5)

        self.textEdit = QTextEdit()  # 创建文本框用于显示
        self.down_layout.addWidget(self.textEdit, 0, 0, 4, 8)
        self.button1.clicked.connect(self.showDialog1)

    # 定义打开文件夹目录的函数
    def showDialog1(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '.')
        if fname[0]:
            f = open(fname[0], 'r')
            with f:
                data = f.read()
                self.textEdit.setText(data)


def main():
    app = QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
