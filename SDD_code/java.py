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


class OP_0_1_setEnv(Operation):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('set offset working')
        platform.declare_env['offset'] = 0


# ==================================================Declare========================================
class OP_4_1_setoffset(Operation):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('set offset working')
        platform.declare_env['offset'] = 0


class OP_4_2_register(Operation):
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
        if len(platform.environment) == 0:
            platform.variables[id_lexme] = (T_type, T_width, platform.declare_env['offset'], None)
            platform.declare_env['offset'] = platform.declare_env['offset'] + T_width
        else:
            assert platform.environment[-1] == 'record'
            platform.environment_stack[-1][0][id_lexme] = (T_type, T_width, platform.environment_stack[-1][1]['offset'], None)
            platform.environment_stack[-1][1]['offset'] = platform.environment_stack[-1][1]['offset'] + T_width


class OP_4_3_registerValue(Operation):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('var register working')
        i = len(Symbol_stack) - 2 - 2
        # id_lexme = Attr_stack[-1]['lexme']

        temp_dict = reduce_record[i]
        k = None
        for (key, value) in temp_dict.items():
            k = key[1]

        id_lexme = platform.lex_varlist[k]
        T_type = Attr_stack[-4]['type']
        T_width = Attr_stack[-4]['width']
        T_value = Attr_stack[-1]['val']

        # TODO 需要整一个专门的函数
        platform.variables[id_lexme] = (T_type, T_width, platform.declare_env['offset'], T_value)
        platform.declare_env['offset'] = platform.declare_env['offset'] + T_width
        platform.gen_str(id_lexme + '=' + T_value)


class OP_4_4_getType(Operation):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('get type working')
        A_type = Attr_stack[-1]['type']
        A_width = Attr_stack[-1]['width']
        Attr_stack[-2]['type'] = A_type
        Attr_stack[-2]['width'] = A_width


class OP_4_5_intDef(Operation):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('int def working')

        platform.declare_env['w'] = 4
        platform.declare_env['t'] = basic_type('int', 4)


class OP_4_6_floatDef(Operation):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('float def working')

        platform.declare_env['w'] = 8
        platform.declare_env['t'] = basic_type('float', 8)


class OP_4_7_charDef(Operation):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('float def working')

        platform.declare_env['w'] = 8
        platform.declare_env['t'] = basic_type('char', 2)


class OP_4_8_arrayInit(Operation):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('array init working')

        Attr_stack[-1]['type'] = platform.declare_env['t']
        Attr_stack[-1]['width'] = platform.declare_env['w']


class OP_4_9_arrayAggregation(Operation):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('set offset working')

        A1_type = Attr_stack[-1]['type']
        idx = Attr_stack[-3]['val']
        array = array_type(idx, A1_type)

        Attr_stack[-4]['type'] = array
        Attr_stack[-4]['width'] = array.width


class OP_4_10_getConst(Operation):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('get const working')

        i = len(Symbol_stack) - 2
        # TODO

        temp_dict = reduce_record[i]
        k = None
        for (key, value) in temp_dict.items():
            k = key[1]

        Attr_stack[-1]['val'] = int(k)


# =======================================================Assignment==============================
class OP_5_1_plus(Operation):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('plus expression working')

        E_addr = platform.newtemp()
        platform.gen_str(E_addr + '=' + Attr_stack[-3]['addr'] + '+' + Attr_stack[-1]['addr'])
        Attr_stack[-3]['addr'] = E_addr


class OP_5_2_minus(Operation):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('minus expression working')

        E_addr = platform.newtemp()
        platform.gen_str(E_addr + '=' + Attr_stack[-3]['addr'] + '-' + Attr_stack[-1]['addr'])
        Attr_stack[-3]['addr'] = E_addr


class OP_5_3_valueTransit10(Operation):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('value transit from 1 to 0 expression working')

        # E_addr = platform.newtemp()
        # platform.gen_str(E_addr + '=' + Attr_stack[-1]['addr'])


class OP_5_4_mult(Operation):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('mult expression working')

        E_addr = platform.newtemp()
        platform.gen_str(E_addr + '=' + Attr_stack[-3]['addr'] + '*' + Attr_stack[-1]['addr'])
        Attr_stack[-3]['addr'] = E_addr


class OP_5_5_division(Operation):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('division expression working')

        E_addr = platform.newtemp()
        platform.gen_str(E_addr + '=' + Attr_stack[-3]['addr'] + '/' + Attr_stack[-1]['addr'])
        Attr_stack[-3]['addr'] = E_addr


class OP_5_6_valueTransit21(Operation):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('value transit from 2 to 1 expression working')

        # E_addr = platform.newtemp()
        # platform.gen_str(E_addr + '=' + Attr_stack[-1]['addr'])


class OP_5_7_valueTransit02(Operation):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('value transit from 0 to 2 expression working')

        # E_addr = platform.newtemp()
        # platform.gen_str(E_addr + '=' + Attr_stack[-2]['addr'])
        Attr_stack[-3]['addr'] = Attr_stack[-2]['addr']


class OP_5_8_iMinus(Operation):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('iminus expression working')

        E_addr = platform.newtemp()
        platform.gen_str(E_addr + '=' + '-' + Attr_stack[-1]['addr'])
        Attr_stack[-1]['addr'] = E_addr


class OP_5_8_iPos(Operation):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('ipos expression working')

        E_addr = platform.newtemp()
        platform.gen_str(E_addr + '=' + '+' + Attr_stack[-1]['addr'])
        Attr_stack[-1]['addr'] = E_addr


class OP_5_9_valueConst(Operation):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('getting value from const working')

        i = len(Symbol_stack) - 2
        # TODO

        temp_dict = reduce_record[i]
        k = None
        for (key, value) in temp_dict.items():
            k = key[1]

        Attr_stack[-1]['val'] = int(k)

        # E_addr = platform.newtemp()
        # platform.gen_str(E_addr + '=' + 'Const value')
        Attr_stack[-1]['addr'] = k


class OP_5_10_valueID(Operation):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('getting value from id working')

        E_addr = platform.newtemp()
        platform.gen_str(E_addr + '=' + 'ID value')
        Attr_stack[-1]['addr'] = E_addr


class OP_5_11_callConst(Operation):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('getting value from function calling working')

        E_addr = platform.newtemp()
        platform.gen_str(E_addr + '=' + 'call value')
        Attr_stack[-1]['addr'] = E_addr


class OP_5_13_valueExpression(Operation):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('getting value from function calling working')

        Attr_stack[-1]['val'] = Attr_stack[-1]['addr']


class OP_5_14_dottedVID(Operation):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('getting value from function calling working')

        raise Exception('unimplemented!')


class OP_5_15_ID2VID(Operation):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('getting value from function calling working')



class OP_5_16_id2ID(Operation):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('get id addr working')

        i = len(Symbol_stack) - 2 # TODO
        # id_lexme = Attr_stack[-1]['lexme']

        temp_dict = reduce_record[i]
        k = None
        for (key, value) in temp_dict.items():
            k = key[1]

        id_lexme = platform.lex_varlist[k]

        Attr_stack[-1]['formay'] = 'v'
        Attr_stack[-1]['addr'] = id_lexme


class OP_5_17_idArray(Operation):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('getting id Array addr working')

        i = len(Symbol_stack) - 5 # TODO
        # id_lexme = Attr_stack[-1]['lexme']

        temp_dict = reduce_record[i]
        k = None
        for (key, value) in temp_dict.items():
            k = key[1]

        id_lexme = platform.lex_varlist[k]

        Attr_stack[-4]['format'] = 'a'
        Attr_stack[-4]['array'] = platform.variables[id_lexme][0]
        Attr_stack[-4]['type'] = Attr_stack[-4]['array'].element
        Attr_stack[-4]['offset'] = platform.newtemp()
        platform.gen_str(Attr_stack[-4]['offset'] + '=' + str(Attr_stack[-4]['type'].width) + '*' + Attr_stack[-2]['addr'])


class OP_5_18_IDArray(Operation):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('getting ID Array addr working')

        # i = len(Symbol_stack) - 4 # TODO
        # # id_lexme = Attr_stack[-1]['lexme']
        #
        # temp_dict = reduce_record[i]
        # k = None
        # for (key, value) in temp_dict.items():
        #     k = key[1]
        #
        # id_lexme = platform.lex_varlist[k]

        Attr_stack[-4]['format'] = 'a'
        # Attr_stack[-4]['array'] = platform.variables[id_lexme][0]
        Attr_stack[-4]['type'] = Attr_stack[-4]['type'].element
        temp = platform.newtemp()
        platform.gen_str(temp + '=' + Attr_stack[-2]['addr'] + '*' + str(Attr_stack[-4]['type'].width))
        offset_temp = platform.newtemp()
        platform.gen_str(offset_temp + '=' + Attr_stack[-4]['offset'] + '+' + temp)


class OP_5_19_Assignment(Operation):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('getting ID Array addr working')

        platform.gen_str(Attr_stack[-3]['addr'] + '=' + Attr_stack[-1]['addr'])


class OP_5_20_iAdd(Operation):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('getting ID Array addr working')

        platform.gen_str(Attr_stack[-3]['addr'] + '=' + Attr_stack[-3]['addr'] + '+' + Attr_stack[-1]['addr'])


class OP_5_21_iMinus(Operation):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('getting ID Array addr working')

        platform.gen_str(Attr_stack[-3]['addr'] + '=' + Attr_stack[-3]['addr'] + '-' + Attr_stack[-1]['addr'])


class OP_5_22_inc(Operation):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('getting ID Array addr working')

        platform.gen_str(Attr_stack[-3]['addr'] + '=' + Attr_stack[-3]['addr'] + '+1')


class OP_5_23_dec(Operation):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('getting ID Array addr working')

        platform.gen_str(Attr_stack[-3]['addr'] + '=' + Attr_stack[-3]['addr'] + '-1')


# ==========================================================record============================================
class OP_3_1_registerRec(Operation):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('register record working')

        i = len(Symbol_stack) - 2 - 3
        # id_lexme = Attr_stack[-1]['lexme']

        temp_dict = reduce_record[i]
        k = None
        for (key, value) in temp_dict.items():
            k = key[1]

        id_lexme = platform.lex_varlist[k]

        # TODO
        platform.environment.pop()
        record_content = platform.environment_stack.pop()

        new_record = record_type(record_content[0])
        if len(platform.environment) == 0:
            platform.variables[id_lexme] = (new_record, new_record.width, platform.declare_env['offset'], None)
            platform.declare_env['offset'] = platform.declare_env['offset'] + new_record.width
        else:
            assert platform.environment[-1] == 'record'
            platform.environment_stack[-1][0][id_lexme] = (new_record, new_record.width,
                                                           platform.environment_stack[-1][1]['offset'], None)
            platform.environment_stack[-1][1]['offset'] = platform.environment_stack[-1][1]['offset'] + new_record.width

class OP_3_2_setRecordEnv(Operation):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('set record environment working')

        platform.environment.append('record')
        # 第一个是var，第二个是env
        platform.environment_stack.append([{}, {'offset': 0}])



def _terminal_with_empty(s: str):
    if s == 'empty':
        return empty_terminal('empty')
    else:
        return terminal(s)


def construct_root():
    # root SDT
    # R - Begin P
    #   Begin - empty {set env}
    # P - empty
    # P - P' P
    # P' - PROCESS
    # P' - RECORD
    # P' - DECLARE SEMI
    # P' - ASSIGNMENT SEMI
    # P' - CALL SEMI
    # P' - IF
    # P' - WHILE
    # P' - DO_WHILE
    # P' - FOR
    root_n_terminals = ['P\'', 'PROCESS', 'RECORD', 'DECLARE', 'ASSIGNMENT', 'CALL', 'IF', 'WHILE', 'DO_WHILE',
                        'FOR', 'P', 'R', 'Begin']
    root_terminals = ['SEMI', 'empty']

    # rule root_-1
    left = n_terminal('R')
    right = [n_terminal('Begin'), n_terminal('P')]
    rule_root__1 = rule(left, right)
    # rule root_-11
    left = n_terminal('Begin')
    right = [OP_0_1_setEnv()]
    rule_root__11 = rule(left, right)
    # rule root_0
    left = n_terminal('P')
    right = [empty_terminal('empty')]
    rule_root_0 = rule(left, right)
    # rule root_1
    left = n_terminal('P')
    right = [n_terminal('P\''), n_terminal('P')]
    rule_root_1 = rule(left, right)

    # rule root_3 TODO 移花接木
    left = n_terminal('DECLARE_NO_VALUE')
    right = [n_terminal('RECORD')]
    rule_root_3 = rule(left, right)

    # rule root_5
    left = n_terminal('P\'')
    right = [n_terminal('ASSIGNMENT'), terminal('SEMI')]
    rule_root_5 = rule(left, right)

    root_rules = [rule_root__1, rule_root__11, rule_root_0, rule_root_1, rule_root_3, rule_root_5]

    return root_n_terminals, root_terminals, root_rules


def construct_declare():
    # Declare SDT
    #
    # P' - DECLARE SEMI
    # DECLARE - DECLARE_NO_VALUE
    # DECLARE - DECLARE_VALUE
    #   Begin - empty {offset = 0}
    # DECLARE_NO_VALUE - TYPE id {register(id.lexme, TYPE.type, TYPE.width, None); offset += width}
    # DECLARE_VALUE - TYPE id assignment ASSIGN {register(id.lexme, type, width, value); offset += width}
    # TYPE - BASIC_TYPE Array {TYPE.type = Array.type; TYPE.width = Array.width}
    #   BASIC_TYPE - INT {w = 4; t = int}
    #   BASIC_TYPE - FLOAT {w = 8; t = float}
    #   BASIC_TYPE - CHAR {w = 2; t = char}
    # Array - empty {Array.type = t; Array.width = w}
    # Array - left_square_brace idx right_square_brace Array1 {A.type = array(idx, A1.type); A.width = A1.width * idx}
    # idx - CONST {idx.val = CONST.val TODO 可以加入一个错误处理}
    #
    #
    declare_n_terminals = ['DECLARE', 'Begin_Declare', 'DECLARE_NO_VALUE', 'DECLARE_VALUE', 'TYPE', 'BASIC_TYPE',
                           'Array', 'idx']
    declare_terminals = ['id', 'assignment', 'INT', 'FLOAT', 'CHAR', 'left_square_brace', 'right_square_brace', 'CONST']

    # rule Declare_0
    left = n_terminal('P\'')
    right = [n_terminal('DECLARE'), terminal('SEMI')]
    rule_declare_0 = rule(left, right)
    # rule Delcare_1
    left = n_terminal('DECLARE')
    right = [n_terminal('DECLARE_NO_VALUE')]
    rule_declare_1 = rule(left, right)
    # rule Delcare_2
    left = n_terminal('DECLARE')
    right = [n_terminal('DECLARE_VALUE')]
    rule_declare_2 = rule(left, right)
    # rule Declare_3
    left = n_terminal('Begin_Declare')
    right = [OP_4_1_setoffset()]
    rule_declare_3 = rule(left, right)
    # rule Declare_4
    left = n_terminal('DECLARE_NO_VALUE')
    right = [n_terminal('TYPE'), terminal('id'), OP_4_2_register()]
    rule_declare_4 = rule(left, right)
    # rule Declare_5
    left = n_terminal('DECLARE_VALUE')
    right = [n_terminal('TYPE'), terminal('id'), terminal('assignment'), n_terminal('ASSIGN'), OP_4_3_registerValue()]
    rule_declare_5 = rule(left, right)
    # rule Declare_6
    left = n_terminal('TYPE')
    right = [n_terminal('BASIC_TYPE'), n_terminal('Array'), OP_4_4_getType()]
    rule_declare_6 = rule(left, right)
    # rule Declare_7
    left = n_terminal('BASIC_TYPE')
    right = [terminal('INT'), OP_4_5_intDef()]
    rule_declare_7 = rule(left, right)
    # rule Declare_8
    left = n_terminal('BASIC_TYPE')
    right = [terminal('FLOAT'), OP_4_6_floatDef()]
    rule_declare_8 = rule(left, right)
    # rule Declare_9
    left = n_terminal('BASIC_TYPE')
    right = [terminal('CHAR'), OP_4_7_charDef()]
    rule_declare_9 = rule(left, right)
    # rule Declare_10
    left = n_terminal('Array')
    right = [OP_4_8_arrayInit()]
    rule_declare_10 = rule(left, right)
    # rule Declare_11
    left = n_terminal('Array')
    right = [terminal('left_square_brace'), n_terminal('idx'),
             terminal('right_square_brace'), n_terminal('Array'), OP_4_9_arrayAggregation()]
    rule_declare_11 = rule(left, right)
    # rule Declare_12
    left = n_terminal('idx')
    right = [terminal('CONST'), OP_4_10_getConst()]
    rule_declare_12 = rule(left, right)
    # # rule Declare_13
    # left = n_terminal('Array')
    # right = [terminal('left_square_brace'), n_terminal('idx'),
    #          terminal('right_square_brace'), n_terminal('Array'), OP_4_9_arrayAggregation()]
    # rule_declare_13 = rule(left, right)
    # # rule Declare_14
    # left = n_terminal('idx')
    # right = [terminal('CONST'), OP_4_10_getConst()]
    # rule_declare_14 = rule(left, right)

    declare_rules = [rule_declare_0, rule_declare_1, rule_declare_2, rule_declare_3, rule_declare_4,
                     rule_declare_5, rule_declare_6, rule_declare_7, rule_declare_8, rule_declare_9,
                     rule_declare_10, rule_declare_11, rule_declare_12]

    return declare_n_terminals, declare_terminals, declare_rules


def construct_assignment():
    # Assignment SDT
    #
    # EXPRESSION - EXPRESSION' plus EXPRESSION1 {E.addr = plat.newtemp(); plat.gen(E.addr = E'.addr + E1.addr)}
    # EXPRESSION - EXPRESSION minus EXPRESSION1
    # EXPRESSION - EXPRESSION1
    # EXPRESSION1 - EXPRESSION1 Star EXPRESSION2
    # EXPRESSION1 - EXPRESSION1 / EXPRESSION2
    # EXPRESSION1 - EXPRESSION2
    # EXPRESSION2 - SLP EXPRESSION SRP
    # EXPRESSION2 - minus EXPRESSION2
    # EXPRESSION2 - plus EXPRESSION2
    # EXPRESSION2 - CONST
    # EXPRESSION2 - V_ID
    # EXPRESSION2 - CALL
    #
    # ASSIGN - new id SLP PARAMS SRP
    # ASSIGN - EXPRESSION
    #
    # V_ID - V_ID dot ID
    # V_ID - ID
    # ID - id
    # ID - id [ ASSIGN ]
    # ID - ID [ ASSIGN ]
    #
    # ASSIGNMENT - V_ID assignment ASSIGN
    # ASSIGNMENT - V_ID IADD EXPRESSION
    # ASSIGNMENT - V_ID IMINUS EXPRESSION
    # ASSIGNMENT - V_ID INC
    # ASSIGNMENT - V_ID DEC
    assign_n_terminals = ['ASSIGN', 'EXPRESSION', 'EXPRESSION1', 'EXPRESSION2', 'V_ID', 'ID', 'CALL', 'PARAMS']
    assign_terminals = ['plus', 'minus', 'Star', '/', 'SLP', 'SRP', 'IADD', 'IMINUS', 'INC', 'DEC', 'dot']

    # rule assignment_0
    left = n_terminal('EXPRESSION')
    right = [n_terminal('EXPRESSION'), terminal('plus'), n_terminal('EXPRESSION1'), OP_5_1_plus()]
    rule_assignment_0 = rule(left, right)
    # rule assignment_1
    left = n_terminal('EXPRESSION')
    right = [n_terminal('EXPRESSION'), terminal('minus'), n_terminal('EXPRESSION1'), OP_5_2_minus()]
    rule_assignment_1 = rule(left, right)
    # rule assignment_2
    left = n_terminal('EXPRESSION')
    right = [n_terminal('EXPRESSION1'), OP_5_3_valueTransit10()]
    rule_assignment_2 = rule(left, right)
    # rule assignment_3
    left = n_terminal('EXPRESSION1')
    right = [n_terminal('EXPRESSION1'), terminal('Star'), n_terminal('EXPRESSION2'), OP_5_4_mult()]
    rule_assignment_3 = rule(left, right)
    # rule assignment_4
    left = n_terminal('EXPRESSION1')
    right = [n_terminal('EXPRESSION1'), terminal('/'), n_terminal('EXPRESSION2'), OP_5_5_division()]
    rule_assignment_4 = rule(left, right)
    # rule assignment_5
    left = n_terminal('EXPRESSION1')
    right = [n_terminal('EXPRESSION2'), OP_5_6_valueTransit21()]
    rule_assignment_5 = rule(left, right)
    # rule assignment_6
    left = n_terminal('EXPRESSION2')
    right = [terminal('SLP'), n_terminal('EXPRESSION'), terminal('SRP'), OP_5_7_valueTransit02()]
    rule_assignment_6 = rule(left, right)
    # rule assignment_7
    left = n_terminal('EXPRESSION2')
    right = [terminal('minus'), n_terminal('EXPRESSION2'), OP_5_8_iMinus()]
    rule_assignment_7 = rule(left, right)
    # rule assignment_8
    left = n_terminal('EXPRESSION1')
    right = [terminal('plus'), n_terminal('EXPRESSION2'), OP_5_8_iPos()]
    rule_assignment_8 = rule(left, right)
    # rule assignment_9
    left = n_terminal('EXPRESSION2')
    right = [terminal('CONST'), OP_5_9_valueConst()]
    rule_assignment_9 = rule(left, right)
    # rule assignment_10
    left = n_terminal('EXPRESSION2')
    right = [n_terminal('V_ID'), OP_5_10_valueID()]
    rule_assignment_10 = rule(left, right)
    # rule assignment_11
    left = n_terminal('EXPRESSION2')
    right = [n_terminal('CALL'), OP_5_11_callConst()]
    rule_assignment_11 = rule(left, right)

    # rule assignment_13
    left = n_terminal('ASSIGN')
    right = [n_terminal('EXPRESSION'), OP_5_13_valueExpression()]
    rule_assignment_13 = rule(left, right)

    # rule assignment_14
    left = n_terminal('V_ID')
    right = [n_terminal('V_ID'), terminal('dot'), n_terminal('ID'), OP_5_14_dottedVID()]
    rule_assignment_14 = rule(left, right)
    # rule assignment_15
    left = n_terminal('V_ID')
    right = [n_terminal('ID'), OP_5_15_ID2VID()]
    rule_assignment_15 = rule(left, right)
    # rule assignment_16
    left = n_terminal('ID')
    right = [terminal('id'), OP_5_16_id2ID()]
    rule_assignment_16 = rule(left, right)
    # rule assignment_17
    left = n_terminal('ID')
    right = [terminal('id'), terminal('left_square_brace'), n_terminal('ASSIGN'), terminal('right_square_brace'),
             OP_5_17_idArray()]
    rule_assignment_17 = rule(left, right)
    # rule assignment_18
    left = n_terminal('ID')
    right = [n_terminal('ID'), terminal('left_square_brace'), n_terminal('ASSIGN'), terminal('right_square_brace'),
             OP_5_18_IDArray()]
    rule_assignment_18 = rule(left, right)

    # rule assignment_19
    left = n_terminal('ASSIGNMENT')
    right = [n_terminal('V_ID'), terminal('assignment'), n_terminal('ASSIGN'), OP_5_19_Assignment()]
    rule_assignment_19 = rule(left, right)
    # rule assignment_20
    left = n_terminal('ASSIGNMENT')
    right = [n_terminal('V_ID'), terminal('IADD'), n_terminal('EXPRESSION'), OP_5_20_iAdd()]
    rule_assignment_20 = rule(left, right)
    # rule assignment_21
    left = n_terminal('ASSIGNMENT')
    right = [n_terminal('V_ID'), terminal('IMINUS'), n_terminal('EXPRESSION'), OP_5_21_iMinus()]
    rule_assignment_21 = rule(left, right)
    # rule assignment_22
    left = n_terminal('ASSIGNMENT')
    right = [n_terminal('V_ID'), terminal('INC'), OP_5_22_inc()]
    rule_assignment_22 = rule(left, right)
    # rule assignment_23
    left = n_terminal('ASSIGNMENT')
    right = [n_terminal('V_ID'), terminal('DEC'), OP_5_23_dec()]
    rule_assignment_23 = rule(left, right)


    assignment_rules = [rule_assignment_0, rule_assignment_1, rule_assignment_2, rule_assignment_3, rule_assignment_4,
                        rule_assignment_5, rule_assignment_6, rule_assignment_7, rule_assignment_8, rule_assignment_9,
                        rule_assignment_10, rule_assignment_11, rule_assignment_13, rule_assignment_14,
                        rule_assignment_15, rule_assignment_16, rule_assignment_17, rule_assignment_18,
                        rule_assignment_19, rule_assignment_20, rule_assignment_21, rule_assignment_22,
                        rule_assignment_23]

    return assign_n_terminals, assign_terminals, assignment_rules


def construct_record():
    # Record SDT
    # RECORD - record id LP DECLARES RP {register(id, record)}
    #   record - empty {env.append('record'); env_stack.append([])}
    # DECLARES - DECLARE SEMI DECLARES
    # DECLARES - empty

    record_n_terminals = ['RECORD', 'DECLARES', 'record\'']
    record_terminals = ['LP', 'RP', 'record']

    # rule record_0
    left = n_terminal('RECORD')
    right = [n_terminal('record\''), terminal('id'), terminal('LP'), n_terminal('DECLARES'), terminal('RP'),
             OP_3_1_registerRec()]
    rule_record_0 = rule(left, right)
    # rule record_1
    left = n_terminal('record\'')
    right = [terminal('record'), OP_3_2_setRecordEnv()]
    rule_record_1 = rule(left, right)
    # rule record_2
    left = n_terminal('DECLARES')
    right = [n_terminal('DECLARE'), terminal('SEMI'), n_terminal('DECLARES')]
    rule_record_2 = rule(left, right)
    # rule record_3
    left = n_terminal('DECLARES')
    right = [empty_terminal('empty')]
    rule_record_3 = rule(left, right)

    record_rules = [rule_record_0, rule_record_1, rule_record_2, rule_record_3]

    return record_n_terminals, record_terminals, record_rules


def construct_java_SDT():
    root_n_terminals, root_terminals, root_rules = construct_root()

    declare_n_terminals, declare_terminals, declare_rules = construct_declare()

    assign_n_terminals, assign_terminals, assignment_rules = construct_assignment()

    record_n_terminals, record_terminals, record_rules = construct_record()

    n_terminals = list(map(lambda x: n_terminal(x), root_n_terminals + declare_n_terminals + assign_n_terminals +
                           record_n_terminals))
    terminals = list(map(lambda x: _terminal_with_empty(x), root_terminals + declare_terminals + assign_terminals +
                         record_terminals))
    rules = root_rules + declare_rules + assignment_rules + record_rules

    return cfg(n_terminal('R'), list(set(n_terminals)), list(set(terminals)), rules)


if __name__ == '__main__':
    enfa = e_NFA()
    enfa.read('../FA/java_fa.dfa')
    o, r, i = enfa.lexical4Syntax('../SDD/java_1_test.txt', '../SDD/java_test1_lex.txt')
    print(o)
    print(r)
    print(i)
    CFG = construct_java_SDT()
    pda = Automata(CFG)
    print(pda)
    plat = CodePlatform()
    plat.lex_varlist = i
    parse = SDT_Parser(CFG, plat)
    parse.parse3(r)
    print(plat.variables)
    print(str(parse))
    print(plat.code)
