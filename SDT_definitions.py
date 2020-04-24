from LexicalAnalysis import *


class Operation(empty_terminal):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: []):
        raise Exception('un-implemented!')


class SDT_rule(rule):
    def __init__(self, left: n_terminal, rights: [symbol, ]):
        rule.__init__(self, left, rights)


if __name__ == '__main__':
    pass