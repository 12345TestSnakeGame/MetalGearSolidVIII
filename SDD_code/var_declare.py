from SyntaxDirectedTranslation import *
from LexicalAnalysis import *
from SyntaxAnalysis import *

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


class OP_1_setoffset(Operation):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('set offset working')
        platform.declare_env['offset'] = 0


class OP_2_register(Operation):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('var register working')
        i = len(Symbol_stack) - 2
        # id_lexme = Attr_stack[-1]['lexme']

        temp_dict = reduce_record[i]
        k = None
        for (key, value) in temp_dict.items():
            k = key[1]

        id_lexme = platform.lex_varlist[k]
        T_type = Attr_stack[-2]['type']
        T_width = Attr_stack[-2]['width']

        # TODO 需要整一个专门的函数
        platform.variables[id_lexme] = (T_type, T_width)
        platform.declare_env['offset'] = platform.declare_env['offset'] + T_width


class OP_3_getType(Operation):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('get type working')
        A_type = Attr_stack[-1]['type']
        A_width = Attr_stack[-1]['width']
        Attr_stack[-2]['type'] = A_type
        Attr_stack[-2]['width'] = A_width


class OP_4_intDef(Operation):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('int def working')

        platform.declare_env['w'] = 4
        platform.declare_env['t'] = basic_type('int', 4)


class OP_5_floatDef(Operation):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('float def working')

        platform.declare_env['w'] = 8
        platform.declare_env['t'] = basic_type('float', 8)


class OP_6_arrayInit(Operation):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('array init working')

        Attr_stack[-1]['type'] = platform.declare_env['t']
        Attr_stack[-1]['width'] = platform.declare_env['w']


class OP_7_arrayAggregation(Operation):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('set offset working')

        A1_type = Attr_stack[-1]['type']
        idx = Attr_stack[-3]['val']
        array = array_type(idx, A1_type)

        Attr_stack[-4]['type'] = array
        Attr_stack[-4]['width'] = array.width


class OP_8_getConst(Operation):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('get const working')

        i = len(Symbol_stack) - 2
        # TODO

        temp_dict = reduce_record[i]
        k = None
        for (key, value) in temp_dict.items():
            k = key[1]

        Attr_stack[-1]['val'] = int(k)

def _terminal_with_empty(s: str):
    if s == 'empty':
        return empty_terminal('empty')
    else:
        return terminal(s)


def construct_SDT():
    # S' - D'
    # D' - Begin D
    #   Begin - empty {offset = 0}
    #   D - P ; D
    #   D - empty
    # P - T id {register(id.lexme, T.type, T.width); offset += T.width}
    # T - B A {T.type = A.type; T.width = A.width}
    #   B - INT {w = 4; t = int}
    #   B - FLOAT {w = 8; t = float}
    # A - empty {A.type = t; A.width = w}
    # A - [ idx ] A1 {A.type = array(CONST, A1.type); A.width = A1.width * CONST}
    # idx - CONST {idx.val = CONST.val}

    terminal_strs = ['INT', 'FLOAT', 'empty', 'id', 'left_square_brace', 'right_square_brace', 'CONST', 'SEMI']
    n_terminal_strs = ['S\'', 'D\'', 'Begin', 'P', 'D', 'B', 'A', 'idx', 'T']

    terminals = list(map(lambda x: _terminal_with_empty(x), terminal_strs))
    n_terminals = list(map(lambda x: n_terminal(x), n_terminal_strs))

    # rule 0
    left = n_terminal('S\'')
    right = [n_terminal('D\'')]
    rule0 = rule(left, right)
    # rule 1
    left = n_terminal('D\'')
    right = [n_terminal('Begin'), n_terminal('D')]
    rule1 = rule(left, right)
    # rule 2
    left = n_terminal('Begin')
    right = [OP_1_setoffset()]
    rule2 = rule(left, right)
    # rule 3
    left = n_terminal('D')
    right = [n_terminal('P'), terminal('SEMI'), n_terminal('D')]
    rule3 = rule(left, right)
    # rule 4
    left = n_terminal('D')
    right = [empty_terminal('empty')]
    rule4 = rule(left, right)
    # rule 5
    left = n_terminal('P')
    right = [n_terminal('T'), terminal('id'), OP_2_register()]
    rule5 = rule(left, right)
    # rule 6
    left = n_terminal('T')
    right = [n_terminal('B'), n_terminal('A'), OP_3_getType()]
    rule6 = rule(left, right)
    # rule 7
    left = n_terminal('B')
    right = [terminal('INT'), OP_4_intDef()]
    rule7 = rule(left, right)
    # rule 8
    left = n_terminal('B')
    right = [terminal('FLOAT'), OP_5_floatDef()]
    rule8 = rule(left, right)
    # rule 9
    left = n_terminal('A')
    right = [OP_6_arrayInit()]
    rule9 = rule(left, right)
    # rule 10
    left = n_terminal('A')
    right = [terminal('left_square_brace'), n_terminal('idx'),
             terminal('right_square_brace'), n_terminal('A'), OP_7_arrayAggregation()]
    rule10 = rule(left, right)
    # rule 11
    left = n_terminal('idx')
    right = [terminal('CONST'), OP_8_getConst()]
    rule11 = rule(left, right)

    return cfg(n_terminal('S\''), n_terminals, terminals, [rule0, rule1, rule2, rule3, rule4, rule5, rule6, rule7,
                                                           rule8, rule9, rule10, rule11])


if __name__ == '__main__':
    enfa = e_NFA()
    enfa.read('../FA/declare_fa.dfa')
    o, r, i = enfa.lexical4Syntax('../SDD/declare_test.txt', '../SDD/declare_test_lex.txt')
    print(o)
    print(r)
    print(i)
    CFG = construct_SDT()
    pda = Automata(CFG)
    print(pda)
    plat = CodePlatform()
    plat.lex_varlist = i
    parse = SDT_Parser(CFG, plat)
    parse.parse3(r)
    print(plat.variables)
    print(str(parse))