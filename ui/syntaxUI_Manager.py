import sys

from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QMainWindow

from ui.syntaxUI import *

from SyntaxAnalysis import *
from LexicalAnalysis import *


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


def setFunction(ui: Ui_MainWindow):
    runner = ui_Runner(ui)
    ui.pushButton_readSyntax.clicked.connect(ui_Runner.read_Rule)
    ui.pushButton_readCode.clicked.connect(ui_Runner.read_Code)
    ui.pushButton_analyze.clicked.connect(ui_Runner.analyze)
    ui.pushButton_generatePDF.clicked.connect(ui_Runner.genPDF)
    ui.pushButton_readWrong.clicked.connect(ui_Runner.read_wrong)



class ui_Runner:

    def __init__(self, ui: Ui_MainWindow):
        self.ui = ui

    def read_Rule(self):
        ui_Runner.enfa = e_NFA()
        ui_Runner.enfa.read('../FA/java_fa.dfa')
        ui_Runner.c = cfg_readfile('../syntax/java_mine_reCustomed.txt')
        f = open('../syntax/java_mine_reCustomed.txt', 'r', encoding='utf-8')
        text = f.read()
        f.close()
        ui.plainTextEdit_syntaxRule.setPlainText(text)

    def read_Code(self):
        o, r, i = ui_Runner.enfa.lexical4Syntax('../Syn_source/java_1.java', 'temp')
        ui_Runner.o, ui_Runner.r, ui_Runner.i = o, r, i
        f = open('../Syn_source/java_1.java', 'r', encoding='utf-8')
        text = f.read()
        f.close()
        ui.plainTextEdit_Code.setPlainText(text)

    def read_wrong(self):
        o, r, i = ui_Runner.enfa.lexical4Syntax('../Syn_source/java_3.java', 'temp')
        ui_Runner.o, ui_Runner.r, ui_Runner.i = o, r, i
        f = open('../Syn_source/java_3.java', 'r', encoding='utf-8')
        text = f.read()
        f.close()
        ui.plainTextEdit_Code.setPlainText(text)

    def analyze(self):
        ui_Runner.parse = LR_Parser(ui_Runner.c)
        ui_Runner.parse.parse3(ui_Runner.r)
        SELECT = ui_Runner.parse.CFG.SELECT
        SELECT_model = QStandardItemModel(len(SELECT), 50)
        SELECT_model.setHorizontalHeaderLabels(list(map(lambda x: str(x), list(range(1, 51)))))
        count = -1
        for (key, value) in SELECT.items():
            count += 1
            c = 0
            SELECT_model.setItem(count, c, QStandardItem(str(key)))
            for t in value:
                c += 1
                item = QStandardItem(t.s)
                SELECT_model.setItem(count, c, item)
        ui.tableView_SELECT.setModel(SELECT_model)

        FOLLOW = ui_Runner.parse.CFG.FOLLOW
        FOLLOW_model = QStandardItemModel(len(FOLLOW), 50)
        FOLLOW_model.setHorizontalHeaderLabels(list(map(lambda x: str(x), list(range(1, 51)))))
        count = -1
        for (key, value) in FOLLOW.items():
            count += 1
            c = 0
            FOLLOW_model.setItem(count, c, QStandardItem(str(key)))
            for t in value:
                c += 1
                item = QStandardItem(t.s)
                FOLLOW_model.setItem(count, c, item)
        ui.tableView_FOLLOW.setModel(FOLLOW_model)

        FIRST = ui_Runner.parse.CFG.FIRST
        FIRST_model = QStandardItemModel(len(FIRST), 50)
        FIRST_model.setHorizontalHeaderLabels(list(map(lambda x: str(x), list(range(1, 51)))))
        count = -1
        for (key, value) in FIRST.items():
            count += 1
            c = 0
            FIRST_model.setItem(count, c, QStandardItem(str(key)))
            for t in value:
                c += 1
                item = QStandardItem(t.s)
                FIRST_model.setItem(count, c, item)
        ui.tableView_FIRST.setModel(FIRST_model)

        table = ui_Runner.parse.PDA.table_LR1
        nt_idx, t_idx = {}, {}
        for (key, value) in table.nt.items():
            nt_idx[value] = key
        for (key, value) in table.t.items():
            t_idx[value] = key
        ntlist, tlist = [], []
        for idx in range(len(nt_idx)):
            ntlist.append(nt_idx[idx])
        for idx in range(len(t_idx)):
            tlist.append(t_idx[idx])
        ACTION = table.ACTION
        GOTO = table.GOTO
        ACTION_model = QStandardItemModel(len(ACTION), len(ACTION[0]))
        ACTION_model.setHorizontalHeaderLabels(list(map(lambda x: str(x), tlist)))
        GOTO_model = QStandardItemModel(len(GOTO), len(GOTO[0]))
        GOTO_model.setHorizontalHeaderLabels(list(map(lambda x: str(x), ntlist)))
        for i in range(len(ACTION)):
            for j in range(len(ACTION[0])):
                if len(ACTION[i][j]) == 0:
                    continue
                ACTION_model.setItem(i, j, QStandardItem(str(ACTION[i][j])))
        for i in range(len(GOTO)):
            for j in range(len(GOTO[0])):
                if len(GOTO[i][j]) == 0:
                    continue
                GOTO_model.setItem(i, j, QStandardItem(str(GOTO[i][j][0][1])))
        ui.tableView_GOTO.setModel(GOTO_model)
        ui.tableView_Action.setModel(ACTION_model)
        ui.plainTextEdit_SysOutput.setPlainText(str(ui_Runner.parse))
        errors = []
        for es in ui_Runner.parse.error:
            errors.append('Error at Line ' + str(es[-1]) + ' : with token <' + str(es[0]) + '-' + str(es[1]) + '>')
        ui.plainTextEdit_Error.setPlainText('\n'.join(errors))
        print('fin')

    def genPDF(self):
        ui_Runner.parse.visualize_tree()


app = QApplication(sys.argv)
mainWindow = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(mainWindow)
setFunction(ui)
mainWindow.show()
sys.exit(app.exec_())