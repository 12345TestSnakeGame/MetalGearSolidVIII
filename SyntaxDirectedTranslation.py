from LexicalAnalysis import *
from SDT_definitions import *
from SDD_code.type_expression_class import *


# 用于生成中间代码的类
# SDT将符号定义，语法动作等数据传给CodePlatform,然后由CodePlatform维护与生成中间代码
class CodePlatform:
    lex_varlist = []
    code = []
    variables = {}

    environment = []
    environment_stack = []

    declare_env = {}

    temp_variables = []
    temp_var_count = 0

    def newtemp(self):
        self.temp_var_count += 1
        v ='t' + str(self.temp_var_count)
        self.temp_variables.append(v)
        return v

    def gen_str(self, code_part: str):
        self.code.append(code_part)


# 进行语法制导翻译的翻译器
# lang读取带有语法动作的文法定义，将语法动作视为空字符，然后生成自动机
# SDT_Parser与普通Parser不同的是，它的分析栈除了状态栈和符号栈之外，还有一个属性栈
# 一边根据ACTION和GOTO表进行语法分析，一边执行语法动作
class SDT_Parser(Parser):
    def __init__(self, lang: cfg, platform: CodePlatform):
        Parser.__init__(self, lang)
        self.platfrom = platform
        self.PDA = Automata(lang)
        pass

    def parse_text(self, text: str):
        symbol_seq = self._get_symbolSequence(text)
        self.parse(symbol_seq)

    def parse(self, seq: []):
        pass

    def parse3(self, token_seq: []):
        lex_seq = list(map(lambda x: terminal(x[0]), token_seq))
        # reduce_record是用于构建树结构的表
        reduce_record = list(map(lambda x: {x: None}, token_seq))
        lex_seq.reverse()
        lex_seq.insert(0, end_terminal('$'))
        # 初始化的两个数据结构
        symbol_stack = [end_terminal('$')]
        status_stack = [0]
        # 属性栈需要特殊处理。如果有一条空产生式，那么提前+1，后面再减回去
        attr_stack = [{}]

        nTerminalList = self.CFG.n_terminals

        unfinished = True
        # 记录读取字符的位置
        token_position = 0
        # 记录错误的位置和新产生式
        errorList = []
        errorline = -1
        while unfinished:
            # 获得栈顶状态与输入符号
            current_status = status_stack[-1]
            current_symbol = lex_seq.pop()
            token_position += 1

            # 获取操作
            operation = self.PDA.table.get_action(current_status, current_symbol.s)
            if len(operation) == 0:
                input_length = len(lex_seq) + 1
                errorList.append(token_seq[-input_length])
                # print(symbol_stack)
                # print(status_stack)
                # raise Exception('LR分析表遇到未知状态')
                # 恐慌模式错误恢复
                found3 = False
                status_backup = []
                symbol_backup = []
                while len(status_stack) > 0:
                    topstatus = status_stack.pop()
                    topsymbol = symbol_stack.pop()
                    attr_stack.pop()
                    status_backup.append(topstatus)
                    symbol_backup.append(topsymbol)
                    # 判断status对应的GOTO表是否为空,并找出所有可用的状态和对应符号
                    fine_status = []
                    fine_symbol = []
                    found2 = False
                    for nt in nTerminalList:
                        goto = self.PDA.table.get_goto(topstatus, nt.s)
                        if len(goto) == 0:
                            continue
                        fine_status.append(goto[0][1])
                        fine_symbol.append(nt.s)

                    if len(fine_symbol) == 0:
                        continue
                    # 找到了goto表不为空，先还一个回去
                    symbol_stack.append(symbol_backup.pop())
                    status_stack.append(status_backup.pop())
                    attr_stack.append({})
                    # 对每一个都试一遍
                    for idx in range(len(fine_symbol)):
                        status = fine_status[idx]
                        symb = fine_symbol[idx]
                        found1 = False
                        input_backup = []
                        while len(lex_seq) > 0:
                            input_symbol = lex_seq.pop()
                            # 备份
                            input_backup.append(input_symbol)
                            if len(self.PDA.table.get_action(status, input_symbol.s)) == 0:
                                continue
                            ac = self.PDA.table.get_action(status, input_symbol.s)[0]
                            symbol_stack.append(symb)
                            status_stack.append(status)
                            attr_stack.append({})
                            found1 = True
                            break
                        if found1:
                            # 退回这个，刚刚拿着用的
                            lex_seq.append(input_backup[-1])
                            found2 = True
                            break
                        else:
                            # 退回
                            while len(input_backup) > 0:
                                lex_seq.append(input_backup.pop())
                            continue
                    if found2:
                        # TODO 这里应该不用什么了吧，状态栈符号栈输入栈都复原了
                        found3 = True
                        break
                    else:
                        status_backup.append(status_stack.pop())
                        symbol_backup.append(symbol_stack.pop())
                        attr_stack.pop()
                        continue
                if found3:
                    # 从头开始
                    # status_stack.append(status_backup[-1])
                    # symbol_stack.append(symbol_backup[-1])
                    # errorList.append(symbol_stack[-1])
                    continue
                else:
                    raise Exception('non')
                    # if len(status_backup) == 0:
                    #     print(token_seq[token_position])
                    #     raise Exception('无法恢复的错误！行号：' + str(token_seq[token_position][-1]))
                    # else:
                    #     while len(status_backup) > 0:
                    #         status_stack.append(status_backup.pop())
                    #         symbol_stack.append(symbol_backup.pop())

            # 需要移进
            if operation[0][0] == 's':
                next_status = operation[0][1]
                symbol_stack.append(current_symbol)
                status_stack.append(next_status)
                attr_stack.append({})
            elif operation[0][0] == 'r':
                # TODO SDT附带的程序在哪个位置执行？先试试开头
                # 完成parsing
                # 需要归约
                # 获取需要归约的产生式
                reduce_rule_number = int(operation[0][1])
                current_rule = self.PDA.CFG.rule_by_number(reduce_rule_number)
                all_empty = True
                for sy in current_rule.right:
                    if not isinstance(sy, empty_terminal):
                        all_empty = False
                if all_empty:
                    attr_stack.append({})
                if isinstance(current_rule.right[-1], Operation):
                    current_rule.right[-1].op(status_stack, symbol_stack, attr_stack, reduce_record, self.platfrom)
                rule_length = len(current_rule.right)
                # 忽略空字符的扩展在这里添加
                empty_count = 0
                for sy in current_rule.right:
                    if isinstance(sy, empty_terminal):
                        empty_count += 1
                # if current_rule.right[0].s == 'empty':
                #     rule_length = 0
                rule_length -= empty_count

                # attr_stack的元素不要被pop掉了
                if rule_length != 0:
                    attr_stack.append(None)
                for idx in range(rule_length):
                    status_stack.pop()
                    symbol_stack.pop()
                    attr_stack.pop()
                assert len(status_stack) > 0
                temp_status = status_stack[-1]
                next_status = self.PDA.table.get_goto(temp_status, current_rule.left.s)
                if operation[0][1] == 0 and isinstance(current_symbol, end_terminal):
                    father = current_rule.left.s
                    size = symbol_stack.__len__() + 1

                    if rule_length == 0:
                        reduce_record = reduce_record[:size - 2] + \
                                        [{father: empty_terminal('empty')}] \
                                        + reduce_record[size - 2:]
                    else:
                        s = size
                        reduce_record = reduce_record[:size - 2] + \
                                        [{father: reduce_record[size - 2: size - 2 + rule_length]}] \
                                        + reduce_record[size - 2 + rule_length:]
                    print('finished parse 2')
                    self.tree = reduce_record[0]
                    self.error = errorList
                    print(errorList)
                    return
                status_stack.append(next_status[0][1])
                symbol_stack.append(current_rule.left)
                if not all_empty:
                    attr_stack.append({})
                if rule_length != 0:
                    attr_stack.pop()
                lex_seq.append(current_symbol)
                token_position -= 1

                father = current_rule.left.s
                size = symbol_stack.__len__()

                if rule_length == 0:
                    reduce_record = reduce_record[:size - 2] + \
                                    [{father: empty_terminal('empty')}] \
                                    + reduce_record[size - 2:]
                else:
                    s = size
                    reduce_record = reduce_record[:size - 2] + \
                                    [{father: reduce_record[size - 2: size - 2 + rule_length]}] \
                                    + reduce_record[size -2 + rule_length:]
        raise Exception('你怎么到这里来了')

    def __print_node(self, depth: int, string: str, node: dict, lineCount: int):
        if node is None:
            return string
        for (key, value) in node.items():
            if isinstance(key, tuple):
                lineCount = key[-1]
                print(key)
                string += '\n' + depth * '\t' + str(key[0]) + ':' + str(key[1]) + ' (' + str(lineCount) + ')'
            else:
                string += '\n' + depth * '\t' + str(key) + ' (' + str(lineCount) + ')'
            if not isinstance(value, list):
                return string
            else:
                for v in value:
                    if isinstance(v, tuple):
                        lineCount = v[-1]
                    string = self.__print_node(depth + 1, string, v, lineCount)
        return string

    def __str__(self):
        return self.__print_node(0, '', self.tree, 1)


class Operation(empty_terminal):
    def __init__(self):
        empty_terminal.__init__(self, 'empty')

    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('OP work')


class SDT_rule(rule):
    def __init__(self, left: n_terminal, rights: [symbol, ]):
        rule.__init__(self, left, rights)


class OP1(Operation):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('OP1 work')


class OP2(Operation):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('OP2 work')


class OP3(Operation):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('OP3 work')


class OP4(Operation):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('OP4 work')


class OP5(Operation):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('OP5 work')


class OP6(Operation):
    def op(self, Status_stack: [], Symbol_stack: [], Attr_stack: [], reduce_record: [], platform: CodePlatform):
        print('OP6 work')


def _terminal_with_empty(s: str):
    if s == 'empty':
        return empty_terminal('empty')
    else:
        return terminal(s)

def controlFlow_SDT():
    # P' - MP'1 S OP2
    #   MP'1 - empty OP1
    # S - MS1 S' ; MS2 S
    #   MS1 - empty OP3
    #   MS2 - empty OP4
    # S - OP5
    terminall_strs = ['if', 'else', 'where', '(', ')', '{', '}', 'SEMI', 'B', 'empty', 'S\'']
    n_terminal_strs = ['P\'', 'S']
    lr_n_terminal_strs = ['MP\'1', 'MS1', 'MS2', 'MS3']

    terminals = list(map(lambda x: _terminal_with_empty(x), terminall_strs))
    n_terminals = list(map(lambda x: n_terminal(x), n_terminal_strs + lr_n_terminal_strs))

    # rule 0
    left0 = n_terminal('P\'')
    right0 = [n_terminal('MP\'1'), n_terminal('S'), OP2()]
    rule0 = rule(left0, right0)
    # rule 1
    left1 = n_terminal('MP\'1')
    right1 = [OP1()]
    rule1 = rule(left1, right1)
    # rule 2
    left2 = n_terminal('S')
    right2 = [n_terminal('MS1'), terminal('S\''), terminal('SEMI'), n_terminal('MS2'), n_terminal('S')]
    rule2 = rule(left2, right2)
    # rule 3
    left3 = n_terminal('MS1')
    right3 = [OP3()]
    rule3 = rule(left3, right3)
    # rule 4
    left4 = n_terminal('MS2')
    right4 = [OP4()]
    rule4 = rule(left4, right4)
    # rule 5
    left5 = n_terminal('S')
    right5 = [OP5()]
    rule5 = rule(left5, right5)
    # rule 6
    # left6 = n_terminal('MS3')
    # right6 = [OP6()]
    # rule6 = rule(left6, right6)

    return cfg(n_terminal('P\''), n_terminals, terminals, [rule0, rule1, rule2, rule3, rule4, rule5])


def testCase():
    enfa = e_NFA()
    enfa.compile_regex('regex/regex_SDT_test.txt')
    enfa.write('FA/sdf_test.fa')
    # enfa.read('FA/sdf_test.fa')
    o, r, i = enfa.lexical4Syntax('SDD/testcase.txt', 'SDD/testcase_lex.txt')
    print(o)
    print(r)
    print(i)
    CFG = controlFlow_SDT()
    pda = Automata(CFG)
    print(pda)
    parse = SDT_Parser(CFG, CodePlatform())
    parse.parse3(r)
    print(str(parse))

if __name__ == '__main__':
    testCase()
    # CFG = controlFlow_SDT()
    # print(CFG)
    # pda = Automata(CFG)
    # print(pda)
    # print('fin')