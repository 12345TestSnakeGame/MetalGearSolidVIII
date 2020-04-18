import time
from SyntaxAnalysis import *
import pickle


# from graphviz import Digraph


# 产生node，并分配序号
# 可以生出一堆小node
class FA_Node:
    def __init__(self, number: int):
        self.number = number
        self.count = 0
        self.nodes = {}

    def generate(self):
        new_node = _node(self.number, self.count)
        self.nodes[self.count] = new_node
        self.count += 1
        return new_node

    def __repr__(self):
        return '=FA_Node with ' + str(self.count + 1) + ' nodes='

    def __str__(self):
        return self.__repr__()

    def __hash__(self):
        return self.count + self.number


# 只允许单字符，以及empty
class Edge:
    def __init__(self, symbol: str):
        if len(symbol) != 1 and symbol != 'empty':
            raise Exception('Edge:非法字符!')
        else:
            self.symbol = symbol

    def __hash__(self):
        return hash(self.symbol)

    def __repr__(self):
        return '--' + self.symbol + '->'

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        return self.symbol == other.symbol


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


# phrase是构建一个自动机的基本单元
#   start是这个自动机模块的起始点，end是结束点
# 以phrase为基本单位进行连接，|，*等操作
# TODO 添加对+,?的支持
class Phrase:
    def __init__(self, Nodes: FA_Node, replace: {}):
        # 一些替换字符串
        self.__replace = replace
        self.fa_node = Nodes
        self.start = Nodes.generate()
        self.end = Nodes.generate()

    def connect(self, post_phrase):
        self.end.add_node(Edge('empty'), post_phrase.start)

    def concatenate(self, pre, post):
        self.start.add_node(Edge('empty'), pre.start)
        pre.end.add_node(Edge('empty'), post.start)
        post.end.add_node(Edge('empty'), self.end)

    def star(self, phrase):
        # self.start = phrase.start
        # self.end = phrase.end
        self.start.add_node(Edge('empty'), self.end)
        self.end.add_node(Edge('empty'), self.start)
        self.start.add_node(Edge('empty'), phrase.start)
        phrase.end.add_node(Edge('empty'), self.end)

    def branch(self, p1, p2):
        self.start.add_node(Edge('empty'), p1.start)
        self.start.add_node(Edge('empty'), p2.start)
        p1.end.add_node(Edge('empty'), self.end)
        p2.end.add_node(Edge('empty'), self.end)

    def character(self, ch: str):
        # assert len(ch) == 1 # 别这么缺德啊
        if ch in self.__replace:
            ch = self.__replace[ch]
        self.start.add_node(Edge(ch), self.end)

    def insert(self, phrase):
        # 不！能！直接把phrase原封不动嵌入进来。
        # 因为本质上是同型的自动机在不同的位置，于是起始与终止状态不同
        # self.start.add_node(Edge('empty'), phrase.start)
        # phrase.end.add_node(Edge('empty'), self.end)

        newphrase = Phrase(self.fa_node, self.__replace)
        self.copy(phrase, newphrase)
        self.start.add_node(Edge('empty'), newphrase.start)
        newphrase.end.add_node(Edge('empty'), self.end)

    def copy(self, original_phrase, new_phrase):
        # 还是三集合-广度优先搜索方法最好用
        explored = set()
        to_explore = set()
        exploring = set()
        new_start = new_phrase.start
        old2new = {original_phrase.start: new_start}
        to_explore.add(original_phrase.start)
        while len(to_explore) != 0:
            for n in to_explore:
                newn = old2new[n]
                for (key, value) in n.next.items():
                    for v in value:
                        # 如果已经访问过了
                        if v in old2new:
                            newn.add_node(key, old2new[v])
                        else:
                            newnode = self.fa_node.generate()
                            old2new[v] = newnode
                            newn.add_node(key, newnode)
                            exploring.add(v)
            explored = explored.union(to_explore)
            to_explore = exploring.copy()
            exploring.clear()
        new_phrase.end = old2new[original_phrase.end]

    def __repr__(self):
        return '==' + str(self.start) + '-' + str(self.end) + '=='

    def __str__(self):
        return self.__repr__()


# 基本的finite automata
# 正则文法的句法分析的表由SyntaxAnalysis产生，通过pickle文件读入
# pickle文件的文件名作为默认参数
class FA:
    def __init__(self):
        pass

    # 根据文件名读取正则文法并compile:
    #   · 使用正则句法的转换表进行句法分析
    #   · 消除冗余
    #   · 生成词法分析的转换表
    def compile_regex(self, filename: str):
        pass

    # 生成正则文法所产生的转换图
    def diagram(self):
        pass


class splited_terminal(n_terminal):
    def __init__(self, name: str, type: int):
        super().__init__(name)
        self.type = type


class e_NFA(FA):
    def __init__(self):
        super().__init__()
        self.fa_node = FA_Node(0)
        # 默认的正则表达式内置符号。如果有冲突，需要在前面加一个斜杠
        self.__regex_built_in = {'(', ')', '|', '*'}
        # 当扫描字符序列时，遇到这些字符即停止扫描
        self.__stop_symbol = {'\t', '\n', ' ', '$'}
        # 对于内置符号和停用词，在某些情况下是会用到的，而那些情况则用字符串代替
        self.__reuse_match = {'left_parenthes': '(',
                              'right_parenthes': ')',
                              'or': '|',
                              'star': '*',
                              'backline': '\n',
                              'tab': '\t',
                              'space': ' ',
                              'comma': ','}
        # 存储所有的终结符与非终结符--以字符串访问symbol对象
        self.terminals = {}
        self.non_terminals = {}
        # 记录变量出现的顺序。在我的句法分析的实现中，所有除了正则表达式内置符号之外的符号都被置换为entity
        # 因此需要将原符号的顺序记录下来，同时生成置换后的字符串
        self.__variable = []
        self.__reg_ex = {}
        # 存储每个变元所对应的自动机的模块
        self.phrases = {}
        # 从文件中读取正则表达式的构造规则(cfg)，得到LR分析器，用于分析每一条正则表达式的句法结构
        self.__lr = LR_Parser(cfg_readfile('cfg_regex.txt'))
        # 内部DFA转换表，key值是symbol
        self.__table = {}
        # 供外部访问的DFA转换表，key值被改为str
        self.table = {}
        # 终止结点
        self.end = {}
        self.backup_end = {}

        # 每个正则文法的FA表
        self.FAs = {}

        self.__end_category = {}
        # const         -   @   获得常量值
        # str           -   ;   获得字符串值
        # annotation    -   :   直接忽略
        # symbol        -   普通符号,普通关键字
        # id            -   &   变量，在注册表中标记
        # ignore        -   ^   中间变量，不会作为终结状态
        # 其中annotation与str需要到特殊终结符中去找
        # 这些特殊ending的状态需要特殊处理
        # 起始符号默认激活，终止符号默认不激活。当检测到起始符号之后，开始等待终止符号

        # 对于注释与字符串这种涉及到自动机状态的符号，需要另外开辟一个数据结构来处理
        # 而且有的符号的起始与终止词不同，有的相同，需要加以区分
        # 元组第一个元素
        #   符号的名字，也就是显示在词法分析结果的字符串
        # 元组的第二个元素
        #   0 - 字符串类，即起始于终止符号相同
        #   1 - 注释类的起始符号
        #   2 - 注释类的终止符号
        # 元组的第三个元素
        #   0 - 接受
        #   1 - 丢弃
        self.__special_endings = {}
        self.__special_pair = {}
        self.__adjustable_endings = {'non_acc': set(), 'annotation': set(), 'str': set()}

    def compile(self, s):
        time_start = time.time()
        # 正则文法的规则：
        # 第一行：所有的非终结符
        # 第二行：所有的终结符
        # 剩余行：所有的正则文法
        #   在后的正则文法会覆盖前面的正则文法，解决了关键字的问题（没有采用表的方法）
        #   右部中出现的非终结符必须在前面的行出现过
        #   由'#'开头的所有行都会忽略掉，作为注释
        #   由'^'开头的行，其符号只作为变元存在，而不能作为接收状态
        #   如果与正则表达式的符号冲突，如括号，|，在前面加个反斜杠\

        # 预处理，去除行尾回车和注释行
        lines = []
        for lll in s:
            if len(lll) <= 1:
                continue
            elif lll[0] == '#':
                continue
            if lll[-1] == '\n':
                lll = lll[:-1]
            lines.append(lll)

        # non terminals
        Nts = lines[0].split(',')
        for n in Nts:
            self.non_terminals[n] = n_terminal(n)
        # terminals
        Ts = lines[1].split(',')
        for t in Ts:
            if t in self.__reuse_match:
                t = self.__reuse_match[t]
            self.terminals[t] = terminal(t)
        # regular expressions
        # for line in lines[2:]:
        #     # 非接收状态
        #     if line[0] == '^':
        #         line = line[1:]
        #         chars = line.split(' ')
        #         var = self.non_terminals[chars[0]]
        #         self.__non_acc.add(var)
        #     # 注释块
        #     elif line[0] == ':':
        #         line = line[1:]
        #         chars = line.split(' ')
        #         envir_name = chars[0]
        #         split_index = chars.index('and')
        #         # 起始和结束符号
        #         e_start = chars[2:split_index]
        #         e_end = chars[split_index + 1:]
        #     # 字符串块
        #     elif line[0] == ';':
        #         line = line[1:]
        #     # 普通符号
        #     else:
        #         chars = line.split(' ')
        #         var = self.non_terminals[chars[0]]
        #
        #     # 记录该正则表达式中符号出现的顺序
        #     self.__variable.append(var)
        #     expression = []
        #     for elements in chars[2:]:
        #         if elements in self.__regex_built_in:
        #             continue
        #         elif elements in self.non_terminals:
        #             expression.append(self.non_terminals[elements])
        #         elif elements in self.terminals:
        #             expression.append(self.terminals[elements])
        #         elif elements in self.__reuse_match:
        #             expression.append(self.terminals[self.__reuse_match[elements]])
        #         else:
        #             raise Exception('e_NFA:正则表达式读取错误!-' + str(elements))
        #     self.__reg_ex[var] = expression

        originline = []

        for line in lines[2:]:
            # 标识符号种类的字符
            type_word = line[0]
            cur_type = ''
            if type_word == '^':
                cur_type = 'ignore'
                line = line[1:]
                chars = line.split(' ')
                var = self.non_terminals[chars[0]]
                self.__end_category[var] = cur_type
                self.__adjustable_endings['non_acc'].add(var)
                expression = []
                for elements in chars[2:]:
                    if elements in self.__regex_built_in:
                        continue
                    elif elements in self.non_terminals:
                        expression.append(self.non_terminals[elements])
                    elif elements in self.terminals:
                        expression.append(self.terminals[elements])
                    elif elements in self.__reuse_match:
                        expression.append(self.terminals[self.__reuse_match[elements]])
                    else:
                        raise Exception('e_NFA:正则表达式读取错误!-' + str(elements))
                self.__reg_ex[var] = expression
                self.__variable.append(var)
                originline.append(line)
            elif type_word == '@':
                cur_type = 'const'
                line = line[1:]
                chars = line.split(' ')
                var = self.non_terminals[chars[0]]
                self.__end_category[var] = cur_type
                expression = []
                for elements in chars[2:]:
                    if elements in self.__regex_built_in:
                        continue
                    elif elements in self.non_terminals:
                        expression.append(self.non_terminals[elements])
                    elif elements in self.terminals:
                        expression.append(self.terminals[elements])
                    elif elements in self.__reuse_match:
                        expression.append(self.terminals[self.__reuse_match[elements]])
                    else:
                        raise Exception('e_NFA:正则表达式读取错误!-' + str(elements))
                self.__reg_ex[var] = expression
                self.__variable.append(var)
                originline.append(line)
            elif type_word == ';':
                cur_type = 'str'
                line = line[1:]
                chars = line.split(' ')
                var_name = chars[0]
                chars = chars[1:]
                split_idx = chars.index('and')
                delimiter_regex = chars[1:split_idx]
                delimiter_name = var_name + '-0'
                self.non_terminals[delimiter_name] = n_terminal(delimiter_name)
                self.__end_category[self.non_terminals[delimiter_name]] = cur_type

                self.__special_endings[delimiter_name] = (self.non_terminals[var_name], 0, 0)
                self.__special_pair[self.non_terminals[delimiter_name]] = self.non_terminals[delimiter_name]
                expression = []
                for elements in delimiter_regex:
                    if elements in self.__regex_built_in:
                        continue
                    elif elements in self.non_terminals:
                        expression.append(self.non_terminals[elements])
                    elif elements in self.terminals:
                        expression.append(self.terminals[elements])
                    elif elements in self.__reuse_match:
                        expression.append(self.terminals[self.__reuse_match[elements]])
                    else:
                        raise Exception('e_NFA:正则表达式读取错误!-' + str(elements))
                self.__reg_ex[self.non_terminals[delimiter_name]] = expression
                self.__variable.append(self.non_terminals[delimiter_name])
                originline.append(' '.join(['a', 'a'] + delimiter_regex))
            elif type_word == ':':
                # TODO 这里默认两个不相等了。我实在不想改了
                cur_type = 'annotation'
                line = line[1:]
                chars = line.split(' ')
                var_name = chars[0]
                chars = chars[1:]
                split_idx = chars.index('and')
                start_regex = chars[1:split_idx]
                end_regex = chars[split_idx + 1:]
                start_name = var_name + '-1'
                end_name = var_name + '-2'
                self.non_terminals[start_name] = n_terminal(start_name)
                self.non_terminals[end_name] = n_terminal(end_name)
                self.__end_category[self.non_terminals[start_name]] = cur_type
                self.__end_category[self.non_terminals[end_name]] = cur_type
                self.__special_pair[self.non_terminals[start_name]] = self.non_terminals[end_name]

                self.__special_endings[start_name] = (self.non_terminals[var_name], 1, 1)
                self.__special_endings[end_name] = (self.non_terminals[var_name], 2, 1)

                count = 0
                names = [start_name, end_name]
                for regex in [start_regex, end_regex]:
                    var = self.non_terminals[names[count]]
                    count += 1
                    expression = []
                    for elements in regex:
                        if elements in self.__regex_built_in:
                            continue
                        elif elements in self.non_terminals:
                            expression.append(self.non_terminals[elements])
                        elif elements in self.terminals:
                            expression.append(self.terminals[elements])
                        elif elements in self.__reuse_match:
                            expression.append(self.terminals[self.__reuse_match[elements]])
                        else:
                            raise Exception('e_NFA:正则表达式读取错误!-' + str(elements))
                    self.__reg_ex[var] = expression
                    self.__variable.append(var)
                    originline.append(' '.join(['a', 'a'] + regex))
            elif type_word == '&':
                cur_type = 'id'
                line = line[1:]
                chars = line.split(' ')
                var = self.non_terminals[chars[0]]
                self.__end_category[var] = cur_type
                expression = []
                for elements in chars[2:]:
                    if elements in self.__regex_built_in:
                        continue
                    elif elements in self.non_terminals:
                        expression.append(self.non_terminals[elements])
                    elif elements in self.terminals:
                        expression.append(self.terminals[elements])
                    elif elements in self.__reuse_match:
                        expression.append(self.terminals[self.__reuse_match[elements]])
                    else:
                        raise Exception('e_NFA:正则表达式读取错误!-' + str(elements))
                self.__reg_ex[var] = expression
                self.__variable.append(var)
                originline.append(line)
            else:
                cur_type = 'symbol'
                chars = line.split(' ')
                var = self.non_terminals[chars[0]]
                self.__end_category[var] = cur_type
                expression = []
                for elements in chars[2:]:
                    if elements in self.__regex_built_in:
                        continue
                    elif elements in self.non_terminals:
                        expression.append(self.non_terminals[elements])
                    elif elements in self.terminals:
                        expression.append(self.terminals[elements])
                    elif elements in self.__reuse_match:
                        expression.append(self.terminals[self.__reuse_match[elements]])
                    else:
                        raise Exception('e_NFA:正则表达式读取错误!-' + str(elements))
                self.__reg_ex[var] = expression
                self.__variable.append(var)
                originline.append(line)


        # 开始构建自动机
        # 第2行开始才是正则表达式
        idx = 0
        for (key, value) in self.__reg_ex.items():
            analyze_str = originline[idx].split(' ')
            idx = idx + 1
            a = []
            # 置换entity
            for symb in analyze_str:
                if symb in self.__regex_built_in:
                    a.append(symb)
                else:
                    a.append('entity')
            string = ' '.join(a[2:])
            print(string)
            # LR分析
            self.__lr.parse(string)
            # self.__lr.visualize_tree()
            tree = self.__lr.tree
            entities = value.copy()
            entities.reverse()

            # 对句法树进行先序遍历，用phrase组装自动机
            print(entities)
            phrase = self.__traverse_compile(tree, entities)
            self.phrases[key] = phrase
            # self.__visualize_phrase(phrase)
            # print(' ')

        # 子集构造法生成转换表，将所有自动机合起来
        # 实际上将正则表达式转换为自动机，通用的方法是直接转换为epsilon-NFA，然后直接子集构造法转换为DFA
        # 因此，另外两个FA的类其实就没有用了---已经删掉了
        tab, endings = self.__subset_construct()
        temp_FA = {}
        for (key, value) in self.phrases.items():
            temptab, tempendings = self.__single_subset_construct(key)
            temp_FA[key] = [temptab, tempendings]
        # 写到文件里看看长啥样
        # f = open('result.txt', 'w', encoding='utf-8')
        # for (key, value) in tab.items():
        #     f.write(str(key) + ' -- ' + str(value))
        # f.close()
        # print(tab)
        time_end = time.time()
        print('finished, took ' + str(time_end - time_start) + ' s')

        # 重整转换表
        new_table = {}
        end_status = {}
        backup_end_status = {}
        # 存放旧状态（复杂的子集）与新状态（计数）之间的对应关系
        status = {}
        reverse_status = {}
        count = 0
        for (key, value) in tab.items():
            new_table[count] = {}
            status[count] = key
            reverse_status[key] = count
            count = count + 1
        for (key, value) in tab.items():
            for (key1, value1) in value.items():
                temp = list(value1)
                temp.sort()
                temptemp = tuple(temp)
                new_table[reverse_status[key]][key1] = reverse_status[temptemp]
        for nt in self.__variable:
            # 有的变元不能成为接收状态
            if self.__end_category[nt] in {'ignore'}:
                continue
            if nt.s in self.__special_endings:
                if self.__special_endings[nt.s][1] == 2:
                    cur_end = endings[nt]
                    for (key, value) in new_table.items():
                        original_set = set(status[key])
                        if cur_end in original_set:
                            backup_end_status[key] = nt
                    continue
            cur_end = endings[nt]
            for (key, value) in new_table.items():
                original_set = set(status[key])
                if cur_end in original_set:
                    end_status[key] = nt
        for (key, value) in temp_FA.items():
            # 重整转换表
            _new_table = {}
            _end_status = {}
            _backup_end_status = {}
            # 存放旧状态（复杂的子集）与新状态（计数）之间的对应关系
            _status = {}
            _reverse_status = {}
            _count = 0
            for (key1, value1) in value[0].items():
                _new_table[_count] = {}
                _status[_count] = key1
                _reverse_status[key1] = _count
                _count = _count + 1
            for (key1, value1) in value[0].items():
                for (key2, value2) in value1.items():
                    temp = list(value2)
                    temp.sort()
                    temptemp = tuple(temp)
                    _new_table[_reverse_status[key1]][key2] = _reverse_status[temptemp]
            cur_end = value[1]
            for (key1, value1) in _new_table.items():
                original_set = set(_status[key1])
                if cur_end in original_set:
                    _end_status[key1] = key
            self.FAs[key] = [_new_table, _end_status]
        self.__table = new_table
        for (key, value) in self.__table.items():
            self.table[key] = {}
            for (key1, value1) in value.items():
                self.table[key][key1.symbol] = value1
        self.end = end_status
        self.backup_end = backup_end_status

    # 从文件中读取正则文法，然后构造自动机与转换表
    def compile_regex(self, filename: str):
        # 正则文法的规则：
        # 第一行：所有的非终结符
        # 第二行：所有的终结符
        # 剩余行：所有的正则文法
        #   在后的正则文法会覆盖前面的正则文法，解决了关键字的问题（没有采用表的方法）
        #   右部中出现的非终结符必须在前面的行出现过
        #   由'#'开头的所有行都会忽略掉，作为注释
        #   由'^'开头的行，其符号只作为变元存在，而不能作为接收状态
        #   如果与正则表达式的符号冲突，如括号，|，在前面加个反斜杠\
        # TODO 需要更新了
        f = open(filename, 'r', encoding='utf-8')
        s = f.readlines()
        f.close()
        self.compile(s)

    # 子集构造法
    def __subset_construct(self):
        # 用一个结点与所有开始状态连接，并记录所有结束状态
        start_node = self.fa_node.generate()
        end_nodes = {}
        for (key, value) in self.phrases.items():
            start_node.add_node(Edge('empty'), value.start)
            end_nodes[key] = value.end

        # 绘图观察
        # temp_phrase = Phrase(self.fa_node)
        # temp_phrase.start = start_node
        # self.__visualize_phrase(temp_phrase)

        # 类似于广度优先搜索
        to_explore = set()
        explored = set()
        exploring = set()
        st = tuple(list(self.__eclosure(start_node)))
        exploring.add(st)
        fa_table = {}
        while len(exploring) != 0:
            # 对每个状态子集
            for s in exploring:
                s = list(s[:])
                # 对状态子集中的每个状态
                # 所有状态的所有可达状态
                switch_table = {}
                for k in s:
                    for (key, value) in k.next.items():
                        # 跳过所有空转移。closure保证了不会有子集之间的空转移
                        if key.symbol == 'empty':
                            continue
                        if key in switch_table:
                            switch_table[key] = switch_table[key].union(set(value))
                        else:
                            switch_table[key] = set(value)

                # closure补全
                for (key, value) in switch_table.items():
                    closure_subset = set()
                    for incomplete_set in value:
                        closure_subset = closure_subset.union(self.__eclosure(incomplete_set))
                    switch_table[key] = closure_subset

                # 将新触及的状态子集填写进转换表
                for (key, value) in switch_table.items():
                    # 未探索过的状态加入探索集合
                    set_value = list(value)
                    set_value.sort()
                    set_value = tuple(set_value)
                    if set_value not in explored and value not in exploring:
                        to_explore.add(set_value)
                    origin = [s]
                    origin.sort()
                    o = tuple(*origin)
                    if o in fa_table:
                        fa_table[o][key] = value
                    else:
                        fa_table[o] = {key: value}
                # 如果switch_table里面什么都没有，说明已经到了结尾状态
                if len(switch_table) == 0:
                    origin = [s]
                    origin.sort()
                    o = tuple(*origin)
                    fa_table[o] = {}
                s.sort()
                s = tuple(s)
                explored.add(s)
            exploring = to_explore.copy()
            to_explore.clear()
        return fa_table, end_nodes

    def __single_subset_construct(self, s: symbol):
        # 用一个结点与所有开始状态连接，并记录所有结束状态
        start_node = self.phrases[s].start
        end_nodes = self.phrases[s].end
        # for (key, value) in self.phrases.items():
        #     start_node.add_node(Edge('empty'), value.start)
        #     end_nodes[key] = value.end

        # 绘图观察
        # temp_phrase = Phrase(self.fa_node)
        # temp_phrase.start = start_node
        # self.__visualize_phrase(temp_phrase)

        # 类似于广度优先搜索
        to_explore = set()
        explored = set()
        exploring = set()
        st = tuple(list(self.__eclosure(start_node)))
        exploring.add(st)
        fa_table = {}
        while len(exploring) != 0:
            # 对每个状态子集
            for s in exploring:
                s = list(s[:])
                # 对状态子集中的每个状态
                # 所有状态的所有可达状态
                switch_table = {}
                for k in s:
                    for (key, value) in k.next.items():
                        # 跳过所有空转移。closure保证了不会有子集之间的空转移
                        if key.symbol == 'empty':
                            continue
                        if key in switch_table:
                            switch_table[key] = switch_table[key].union(set(value))
                        else:
                            switch_table[key] = set(value)

                # closure补全
                for (key, value) in switch_table.items():
                    closure_subset = set()
                    for incomplete_set in value:
                        closure_subset = closure_subset.union(self.__eclosure(incomplete_set))
                    switch_table[key] = closure_subset

                # 将新触及的状态子集填写进转换表
                for (key, value) in switch_table.items():
                    # 未探索过的状态加入探索集合
                    set_value = list(value)
                    set_value.sort()
                    set_value = tuple(set_value)
                    if set_value not in explored and value not in exploring:
                        to_explore.add(set_value)
                    origin = [s]
                    origin.sort()
                    o = tuple(*origin)
                    if o in fa_table:
                        fa_table[o][key] = value
                    else:
                        fa_table[o] = {key: value}
                # 如果switch_table里面什么都没有，说明已经到了结尾状态
                if len(switch_table) == 0:
                    origin = [s]
                    origin.sort()
                    o = tuple(*origin)
                    fa_table[o] = {}
                s.sort()
                s = tuple(s)
                explored.add(s)
            exploring = to_explore.copy()
            to_explore.clear()
        return fa_table, end_nodes

    # 计算node对应的closure闭包
    def __eclosure(self, _node):
        empty_edge = Edge('empty')
        # 广度优先搜索
        explored = {_node}
        exploring = {_node}
        to_explore = set()
        while len(exploring) != 0:
            for n in exploring:
                if empty_edge in n.next:
                    for k in n.next[empty_edge]:
                        if k not in explored and k not in exploring:
                            to_explore.add(k)
            for k in exploring:
                explored.add(k)
            exploring = to_explore.copy()
            to_explore.clear()
        return explored

    # 通过遍历整棵语法树的方法来生成自动机
    def __traverse_compile(self, tree: {}, entities: []):
        # 通过前序遍历构建自动机
        initial_phrase = self.__recursive_traverse(tree, entities)
        # self.__visualize_phrase(initial_phrase)
        return initial_phrase

    # 绘制一个phrase的自动机图
    def __visualize_phrase(self, p: Phrase):
        dot = Digraph(comment='finite automata')
        dot.node(p.start.__str__(), p.start.__str__())
        edge_set = set()
        self.__visualize_node(p.start, dot, edge_set)
        dot.view()

    # __visualize_phrase的子函数
    def __visualize_node(self, n: _node, dot, edge_s):
        father_name = n.__str__()
        for (key, value) in n.next.items():
            edge = key
            for post in value:
                new_edge = (father_name, post.__str__(), edge.__str__())
                if new_edge in edge_s:
                    continue
                else:
                    dot.edge(father_name, post.__str__(), edge.__str__())
                    edge_s.add(new_edge)

                self.__visualize_node(post, dot, edge_s)

    # 可视化产生的DFA
    def visualize_DFA(self):
        d = Digraph(comment='DFA')
        for (key, value) in self.__table.items():
            if key in self.end:
                d.node(str(key), str(key) + '-' + str(self.end[key]), color='red')
            else:
                d.node(str(key), str(key))
        for (key, value) in self.__table.items():
            for (key1, value1) in value.items():
                d.edge(str(key), str(value1), str(key1))
        d.view()
        # d.render('test-output/DFA_.gv', view=True)

    def visualize_single(self, tables, ends):
        d = Digraph(comment='DFA')
        for (key, value) in tables.items():
            if key in ends:
                d.node(str(key), str(key) + '-' + str(ends[key]), color='red')
            else:
                d.node(str(key), str(key))
        for (key, value) in tables.items():
            for (key1, value1) in value.items():
                d.edge(str(key), str(value1), str(key1))
        d.view()

    # 根据treenode构造phrase
    def __recursive_traverse(self, tree_node: {}, entities: []):
        for (key, value) in tree_node.items():
            # 在这里根据value考虑下一步
            # 与产生式直接相关
            sons = []
            for d in value:
                for (key1, value1) in d.items():
                    sons.append(key1)
            # R' - R
            # B - A
            # R - B
            if len(sons) == 1 and isinstance(sons[0], n_terminal):
                return self.__recursive_traverse(value[0], entities)
            # R - B | R
            elif len(sons) == 3 and sons[1].s == '|':
                current_phrase = Phrase(self.fa_node, self.__reuse_match)
                p1 = self.__recursive_traverse(value[0], entities)
                p2 = self.__recursive_traverse(value[2], entities)
                current_phrase.branch(p1, p2)
                return current_phrase
            # B - A B
            elif len(sons) == 2 and sons[1].s != '*':
                current_phrase = Phrase(self.fa_node, self.__reuse_match)
                pre = self.__recursive_traverse(value[0], entities)
                post = self.__recursive_traverse(value[1], entities)
                current_phrase.concatenate(pre, post)
                return current_phrase
            # A - A *
            elif len(sons) == 2 and sons[1].s == '*':
                current_phrase = Phrase(self.fa_node, self.__reuse_match)
                star_phrase = self.__recursive_traverse(value[0], entities)
                current_phrase.star(star_phrase)
                return current_phrase
            # A - ( R )
            elif len(sons) == 3 and sons[0].s == '(':
                return self.__recursive_traverse(value[1], entities)
            # A - entity
            elif len(sons) == 1 and isinstance(sons[0], terminal):
                current_phrase = Phrase(self.fa_node, self.__reuse_match)
                real_entity = entities.pop()
                if isinstance(real_entity, n_terminal):
                    current_phrase.insert(self.phrases[real_entity])
                elif isinstance(real_entity, terminal):
                    if real_entity.s == 'empty':
                        current_phrase.character('empty')
                    else:
                        assert len(real_entity.s) == 1
                        current_phrase.character(real_entity.s)
                return current_phrase
            else:
                raise Exception('e_NFA:遍历树过程中未知产生式!')

    # TODO 通过设计SDT来在parsing时生成自动机
    def __SDT_compile(self):
        pass

    def str_table(self):
        symbol_index = {}
        count = 0
        for (key, value) in self.terminals.items():
            symbol_index[key] = count
            count += 1
        return self.table, symbol_index

    def write(self, filename: str):

        terminals_ = self.terminals
        non_terminals_ = self.non_terminals
        phrases = self.phrases
        tabels = self.table
        ends = self.end
        backup_ends = self.backup_end
        end_category_ = self.__end_category
        special_endings_ = self.__special_endings
        adjustable_endings_ = self.__adjustable_endings
        pairs = self.__special_pair
        internal_table = self.__table
        FAS = self.FAs

        result = [terminals_, non_terminals_, phrases, tabels, ends, backup_ends, end_category_,
                  special_endings_, adjustable_endings_, pairs, internal_table, FAS]


        f = open(filename, 'wb')
        pickle.dump(result, f)
        f.close()

    def read(self, filename: str):
        f = open(filename, 'rb')
        infos = pickle.load(f)
        f.close()

        self.terminals = infos[0]
        self.non_terminals = infos[1]
        self.phrases = infos[2]
        self.table = infos[3]
        self.end = infos[4]
        self.backup_end = infos[5]
        self.__end_category = infos[6]
        self.__special_endings = infos[7]
        self.__adjustable_endings = infos[8]
        self.__special_pair = infos[9]
        self.__table = infos[10]
        self.FAs = infos[11]

    def Lexical(self, codes: []):
        content = list(codes)
        content.reverse()
        content = ['$'] + content

        # 存放词法分析的结果
        lexical_result = []
        registered_id = {}
        backup_status = 0
        current_status = 0
        # backup，就是存储不一定属于合法词的字符序列。content是一定是合法词的字符序列
        backup_stack = []
        content_stack = []

        # 原输入
        original_input = []

        # 丢弃掉的错误输入
        error_stack = []
        in_error = False

        # 行号计数
        line_count = 1

        extra_stack = []
        extra_statuses = []

        # 定义三种处理的状态
        #   1 正常读取状态，将读到的字符放入自动机
        #   2 注释状态，丢弃所有字符直到出注释块
        #   3 字符串状态，保存所有字符知道出字符串状态

        in_env = False
        preserve_input = False
        expect_status = -1
        errorline = 0
        reline = True

        while len(content) != 0:
            ch = content.pop()
            if ch == '\n':
                line_count = line_count + 1
            if in_env:
                if in_error and current_status in self.end:
                    in_error = False
                    reline = True
                    lexical_result.append((''.join(error_stack), '词法错误！', errorline))
                    original_input.append(' ')
                    error_stack.clear()
                # 万恶的转义字符
                if ch == '\\':
                    extra_stack.append(content.pop())
                    continue
                extra_stack.append(ch)
                if 0 not in extra_statuses:
                    extra_statuses.append(0)
                newstatus = []
                for idx in range(len(extra_statuses)):
                    if ch in self.table[extra_statuses[idx]]:
                        newstatus.append(self.table[extra_statuses[idx]][ch])
                        temp_status = newstatus[-1]
                        if temp_status in self.backup_end:
                            cur = self.backup_end[temp_status]
                        elif temp_status in self.end:
                            cur = self.end[temp_status]
                        else:
                            continue
                        if cur == expect_status:
                            current_status = 0
                            backup_stack = []
                            backup_status = 0
                            content_stack = []
                            in_env = False
                            if preserve_input:
                                lexical_result.append(('str', ''.join(extra_stack)))
                                if extra_stack[-1] == '\"':
                                    original_input.append('\"' + ''.join(extra_stack))
                                else:
                                    original_input.append('\'' + ''.join(extra_stack))
                                extra_stack.clear()
                            else:
                                extra_stack.clear()
                            break
                extra_statuses = newstatus
                continue

            # 如果当前处于错误恢复状态，同时又找到了终止状态
            if in_error and current_status in self.end:
                in_error = False
                reline = True
                lexical_result.append((''.join(error_stack), '词法错误！', errorline))
                original_input.append(' ')
                error_stack.clear()

            try:
                # 先判断是否是停用词。至少如果是停用词的话，要么接收要么报错
                if ch in self.__stop_symbol:
                    # 是停用词代表不会进入自动机，看自动机当前状态
                    # 如果自动机在初始状态
                    if current_status == 0:
                        # 直接跳过
                        continue
                    elif current_status in self.end:
                        # 如果当前状态是终结状态
                        symb = self.end[current_status]
                        copy_stack = backup_stack
                        copy_stack.reverse()
                        content_stack += copy_stack
                        cur_type = self.__end_category[symb]
                        if cur_type == 'const':
                            lexical_result.append((symb.s, ''.join(content_stack)))
                            original_input.append(''.join(content_stack))
                        elif cur_type == 'id':
                            string = ''.join(content_stack)
                            if string in registered_id:
                                lexical_result.append(('id', registered_id[string]))
                                original_input.append(''.join(content_stack))
                            else:
                                new_idx = len(registered_id)
                                registered_id[string] = new_idx
                                lexical_result.append(('id', new_idx))
                                original_input.append(''.join(content_stack))
                        else:
                            lexical_result.append((symb.s, ''))
                            original_input.append(''.join(content_stack))
                        current_status = 0
                        backup_stack.clear()
                        content_stack.clear()
                        backup_status = 0
                    elif backup_status != 0:
                        symb = self.end[backup_status]

                        # 把content_stack的内容压回去
                        # 先把刚刚读出来的符号压回去
                        content.append(ch)
                        if ch == '\n':
                            line_count -= 1
                        # 然后把存放在backup_stack中的字符压回去，要反序
                        content += backup_stack
                        iii = backup_stack.count('\n')
                        line_count -= iii

                        # 存放在content_stack中的内容成为接收的字符串。
                        content_stack = content_stack
                        cur_type = self.__end_category[symb]

                        if cur_type == 'const':
                            lexical_result.append((symb.s, ''.join(content_stack)))
                            original_input.append(''.join(content_stack))
                        elif cur_type == 'id':
                            string = ''.join(content_stack)
                            if string in registered_id:
                                lexical_result.append(('id', registered_id[string]))
                                original_input.append(''.join(content_stack))
                            else:
                                new_idx = len(registered_id)
                                registered_id[string] = new_idx
                                lexical_result.append(('id', new_idx))
                                original_input.append(''.join(content_stack))
                        else:
                            lexical_result.append((symb.s, ''))
                            original_input.append(''.join(content_stack))
                        current_status = 0
                        backup_stack = []
                        content_stack = []
                        backup_status = 0
                    else:
                        # 读取到了停用词，当前状态既不是初始状态也不是终结状态，而是读取某个文法到一半的状态。
                        raise Exception('LexicalAnalyzer:文法错误!\n' + ch + '  '.join(list(map(str, lexical_result))) +
                                        '当前状态：' + str(current_status) + ' content_stack:' + ''.join(content_stack)
                                        + ' backup_stack:' + ''.join(backup_stack))
                else:
                    # 如果当前状态是一个终结状态，那么当前状态是一个潜在的成功识别符号
                    if current_status in self.end:
                        # 如果有可行路径，根据最长匹配原则，需要继续探索，同时记录下当前位置
                        if ch in self.table[current_status]:
                            # 当前路径是一个可行符号，先记录下来z
                            backup_status = current_status
                            # 把未确认内容保存，注意要倒序
                            copy_stack = backup_stack
                            copy_stack.reverse()
                            content_stack += copy_stack
                            backup_stack.clear()
                            # 哨兵继续探索下一个状态
                            current_status = self.table[current_status][ch]
                            backup_stack.insert(0, ch)
                        # 无路可走了
                        else:
                            # 试着接收
                            symb = self.end[current_status]
                            copy_stack = backup_stack
                            copy_stack.reverse()
                            content_stack += copy_stack
                            cur_type = self.__end_category[symb]
                            if cur_type == 'const':
                                lexical_result.append((symb.s, ''.join(content_stack)))
                                original_input.append(''.join(content_stack))
                            elif cur_type == 'id':
                                string = ''.join(content_stack)
                                if string in registered_id:
                                    lexical_result.append(('id', registered_id[string]))
                                    original_input.append(''.join(content_stack))
                                else:
                                    new_idx = len(registered_id)
                                    registered_id[string] = new_idx
                                    lexical_result.append(('id', new_idx))
                                    original_input.append(''.join(content_stack))
                            else:
                                lexical_result.append((symb.s, ''))
                                original_input.append(''.join(content_stack))
                            current_status = 0
                            backup_stack.clear()
                            content_stack.clear()
                            backup_status = 0
                            # 符号再压回去
                            content.append(ch)
                            if ch == '\n':
                                line_count -= 1
                    # 如果当前状态不是终结状态，继续向前探索，备份好输入
                    else:
                        # 如果无路可走了
                        if ch not in self.table[current_status]:
                            # 如果从初始状态到当前状态还没有碰到过可接受状态
                            if backup_status == 0:
                                # TODO 读取的是合法字符，但当前状态不是终止状态，当前符号也不是可接受符号，且来的路上也没有碰到过可接受状态
                                raise Exception('当前状态：' + str(current_status) + ' 已读取符号:' + ''.join(content_stack) + ' backup_stack:' + ''.join(backup_stack))
                            # 如果碰到过的话，回滚
                            else:
                                symb = self.end[backup_status]

                                # 把content_stack的内容压回去
                                # 先把刚刚读出来的符号压回去
                                content.append(ch)
                                if ch == '\n':
                                    line_count -= 1
                                # 然后把存放在backup_stack中的字符压回去，要反序
                                content += backup_stack
                                iii = backup_stack.count('\n')
                                line_count -= iii

                                # 存放在content_stack中的内容成为接收的字符串。
                                cur_type = self.__end_category[symb]

                                if cur_type == 'const':
                                    lexical_result.append((symb.s, ''.join(content_stack)))
                                    original_input.append(''.join(content_stack))
                                elif cur_type == 'id':
                                    string = ''.join(content_stack)
                                    if string in registered_id:
                                        lexical_result.append(('id', registered_id[string]))
                                        original_input.append(''.join(content_stack))
                                    else:
                                        new_idx = len(registered_id)
                                        registered_id[string] = new_idx
                                        lexical_result.append(('id', new_idx))
                                        original_input.append(''.join(content_stack))
                                else:
                                    lexical_result.append((symb.s, ''))
                                    original_input.append(''.join(content_stack))
                                current_status = 0
                                backup_stack = []
                                content_stack = []
                                backup_status = 0
                        # 如果有路可走
                        else:
                            # 那就走呗
                            backup_stack.insert(0, ch)
                            current_status = self.table[current_status][ch]
            except Exception as e:
                # 每次出现异常，就说明存储在backup_stack中的序列无法作为合法的词，所以一定会忽略一个
                in_error = True
                if reline:
                    errorline = line_count
                if len(backup_stack) == 0:
                    ignore_ch = ch
                else:
                    ignore_ch = backup_stack.pop()
                    assert len(content_stack) == 0
                    content.append(ch)
                    while len(backup_stack) != 0:
                        content.append(backup_stack.pop())
                    current_status = 0
                    backup_status = 0
                error_stack.append(ignore_ch)
            finally:
                pass

            if current_status not in self.end:
                pass
            elif self.end[current_status] in self.__special_pair:
                in_env = True
                properties = self.__special_endings[self.end[current_status].s]
                if properties[2] == 0:
                    preserve_input = True
                else:
                    preserve_input = False
                if properties[1] == 1:
                    expect_status = self.__special_pair[self.end[current_status]]
                elif properties[1] == 0:
                    expect_status = self.end[current_status]
                else:
                    raise Exception('注释区块错误-' + '当前状态：' + str(current_status) + ' 已读取符号:'
                                    + ''.join(content_stack) + ' backup_stack:' + ''.join(backup_stack))
                continue

        # 如果还在注释/字符串环境中
        if in_env:
            if preserve_input:
                lexical_result.append(('', '字符串环境错误！', 0))
                original_input.append(' ')
            else:
                lexical_result.append(('', '注释环境错误！', 0))
                original_input.append(' ')
        elif len(backup_stack) != 0:
            backup_stack.reverse()
            lexical_result.append((''.join(backup_stack), '词法错误！', errorline))
            original_input.append(' ')

        print(lexical_result)
        print(registered_id)
        id_index = {}
        for (key, value) in registered_id.items():
            id_index[value] = key
        return original_input, lexical_result, id_index

    def Lexical4Syntax(self, codes: []):
        content = list(codes)
        content.reverse()
        content = ['$'] + content

        # 存放词法分析的结果
        lexical_result = []
        registered_id = {}
        backup_status = 0
        current_status = 0
        # backup，就是存储不一定属于合法词的字符序列。content是一定是合法词的字符序列
        backup_stack = []
        content_stack = []

        # 原输入
        original_input = []

        # 丢弃掉的错误输入
        error_stack = []
        in_error = False

        # 行号计数
        line_count = 1

        extra_stack = []
        extra_statuses = []

        # 定义三种处理的状态
        #   1 正常读取状态，将读到的字符放入自动机
        #   2 注释状态，丢弃所有字符直到出注释块
        #   3 字符串状态，保存所有字符知道出字符串状态

        in_env = False
        preserve_input = False
        expect_status = -1
        errorline = 0
        reline = True

        while len(content) != 0:
            ch = content.pop()
            if ch == '\n':
                line_count = line_count + 1
            if in_env:
                if in_error and current_status in self.end:
                    in_error = False
                    reline = True
                    lexical_result.append((''.join(error_stack), '词法错误！', errorline))
                    original_input.append(' ')
                    error_stack.clear()
                # 万恶的转义字符
                if ch == '\\':
                    extra_stack.append(content.pop())
                    continue
                extra_stack.append(ch)
                if 0 not in extra_statuses:
                    extra_statuses.append(0)
                newstatus = []
                for idx in range(len(extra_statuses)):
                    if ch in self.table[extra_statuses[idx]]:
                        newstatus.append(self.table[extra_statuses[idx]][ch])
                        temp_status = newstatus[-1]
                        if temp_status in self.backup_end:
                            cur = self.backup_end[temp_status]
                        elif temp_status in self.end:
                            cur = self.end[temp_status]
                        else:
                            continue
                        if cur == expect_status:
                            current_status = 0
                            backup_stack = []
                            backup_status = 0
                            content_stack = []
                            in_env = False
                            if preserve_input:
                                lexical_result.append(('CONST', ''.join(extra_stack)))
                                if extra_stack[-1] == '\"':
                                    original_input.append('\"' + ''.join(extra_stack))
                                else:
                                    original_input.append('\'' + ''.join(extra_stack))
                                extra_stack.clear()
                            else:
                                extra_stack.clear()
                            break
                extra_statuses = newstatus
                continue

            # 如果当前处于错误恢复状态，同时又找到了终止状态
            if in_error and current_status in self.end:
                in_error = False
                reline = True
                lexical_result.append((''.join(error_stack), '词法错误！', errorline))
                original_input.append(' ')
                error_stack.clear()

            try:
                # 先判断是否是停用词。至少如果是停用词的话，要么接收要么报错
                if ch in self.__stop_symbol:
                    # 是停用词代表不会进入自动机，看自动机当前状态
                    # 如果自动机在初始状态
                    if current_status == 0:
                        # 直接跳过
                        continue
                    elif current_status in self.end:
                        # 如果当前状态是终结状态
                        symb = self.end[current_status]
                        copy_stack = backup_stack
                        copy_stack.reverse()
                        content_stack += copy_stack
                        cur_type = self.__end_category[symb]
                        if cur_type == 'const':
                            lexical_result.append((symb.s, ''.join(content_stack), line_count))
                            original_input.append(''.join(content_stack))
                        elif cur_type == 'id':
                            string = ''.join(content_stack)
                            if string in registered_id:
                                lexical_result.append(('id', registered_id[string], line_count))
                                original_input.append(''.join(content_stack))
                            else:
                                new_idx = len(registered_id)
                                registered_id[string] = new_idx
                                lexical_result.append(('id', new_idx, line_count))
                                original_input.append(''.join(content_stack))
                        else:
                            lexical_result.append((symb.s, '', line_count))
                            original_input.append(''.join(content_stack))
                        current_status = 0
                        backup_stack.clear()
                        content_stack.clear()
                        backup_status = 0
                    elif backup_status != 0:
                        symb = self.end[backup_status]

                        # 把content_stack的内容压回去
                        # 先把刚刚读出来的符号压回去
                        content.append(ch)
                        if ch == '\n':
                            line_count -= 1
                        # 然后把存放在backup_stack中的字符压回去，要反序
                        content += backup_stack
                        iii = backup_stack.count('\n')
                        line_count -= iii

                        # 存放在content_stack中的内容成为接收的字符串。
                        content_stack = content_stack
                        cur_type = self.__end_category[symb]

                        if cur_type == 'const':
                            lexical_result.append((symb.s, ''.join(content_stack), line_count))
                            original_input.append(''.join(content_stack))
                        elif cur_type == 'id':
                            string = ''.join(content_stack)
                            if string in registered_id:
                                lexical_result.append(('id', registered_id[string], line_count))
                                original_input.append(''.join(content_stack))
                            else:
                                new_idx = len(registered_id)
                                registered_id[string] = new_idx
                                lexical_result.append(('id', new_idx, line_count))
                                original_input.append(''.join(content_stack))
                        else:
                            lexical_result.append((symb.s, '', line_count))
                            original_input.append(''.join(content_stack))
                        current_status = 0
                        backup_stack = []
                        content_stack = []
                        backup_status = 0
                    else:
                        # 读取到了停用词，当前状态既不是初始状态也不是终结状态，而是读取某个文法到一半的状态。
                        raise Exception('LexicalAnalyzer:文法错误!\n' + ch + '  '.join(list(map(str, lexical_result))) +
                                        '当前状态：' + str(current_status) + ' content_stack:' + ''.join(content_stack)
                                        + ' backup_stack:' + ''.join(backup_stack))
                else:
                    # 如果当前状态是一个终结状态，那么当前状态是一个潜在的成功识别符号
                    if current_status in self.end:
                        # 如果有可行路径，根据最长匹配原则，需要继续探索，同时记录下当前位置
                        if ch in self.table[current_status]:
                            # 当前路径是一个可行符号，先记录下来z
                            backup_status = current_status
                            # 把未确认内容保存，注意要倒序
                            copy_stack = backup_stack
                            copy_stack.reverse()
                            content_stack += copy_stack
                            backup_stack.clear()
                            # 哨兵继续探索下一个状态
                            current_status = self.table[current_status][ch]
                            backup_stack.insert(0, ch)
                        # 无路可走了
                        else:
                            # 试着接收
                            symb = self.end[current_status]
                            copy_stack = backup_stack
                            copy_stack.reverse()
                            content_stack += copy_stack
                            cur_type = self.__end_category[symb]
                            if cur_type == 'const':
                                lexical_result.append((symb.s, ''.join(content_stack), line_count))
                                original_input.append(''.join(content_stack))
                            elif cur_type == 'id':
                                string = ''.join(content_stack)
                                if string in registered_id:
                                    lexical_result.append(('id', registered_id[string], line_count))
                                    original_input.append(''.join(content_stack))
                                else:
                                    new_idx = len(registered_id)
                                    registered_id[string] = new_idx
                                    lexical_result.append(('id', new_idx, line_count))
                                    original_input.append(''.join(content_stack))
                            else:
                                lexical_result.append((symb.s, '', line_count))
                                original_input.append(''.join(content_stack))
                            current_status = 0
                            backup_stack.clear()
                            content_stack.clear()
                            backup_status = 0
                            # 符号再压回去
                            content.append(ch)
                            if ch == '\n':
                                line_count -= 1
                    # 如果当前状态不是终结状态，继续向前探索，备份好输入
                    else:
                        # 如果无路可走了
                        if ch not in self.table[current_status]:
                            # 如果从初始状态到当前状态还没有碰到过可接受状态
                            if backup_status == 0:
                                # TODO 读取的是合法字符，但当前状态不是终止状态，当前符号也不是可接受符号，且来的路上也没有碰到过可接受状态
                                raise Exception('当前状态：' + str(current_status) + ' 已读取符号:' + ''.join(content_stack) + ' backup_stack:' + ''.join(backup_stack))
                            # 如果碰到过的话，回滚
                            else:
                                symb = self.end[backup_status]

                                # 把content_stack的内容压回去
                                # 先把刚刚读出来的符号压回去
                                content.append(ch)
                                if ch == '\n':
                                    line_count -= 1
                                # 然后把存放在backup_stack中的字符压回去，要反序
                                content += backup_stack
                                iii = backup_stack.count('\n')
                                line_count -= iii

                                # 存放在content_stack中的内容成为接收的字符串。
                                cur_type = self.__end_category[symb]

                                if cur_type == 'const':
                                    lexical_result.append((symb.s, ''.join(content_stack), line_count))
                                    original_input.append(''.join(content_stack))
                                elif cur_type == 'id':
                                    string = ''.join(content_stack)
                                    if string in registered_id:
                                        lexical_result.append(('id', registered_id[string], line_count))
                                        original_input.append(''.join(content_stack))
                                    else:
                                        new_idx = len(registered_id)
                                        registered_id[string] = new_idx
                                        lexical_result.append(('id', new_idx, line_count))
                                        original_input.append(''.join(content_stack))
                                else:
                                    lexical_result.append((symb.s, '', line_count))
                                    original_input.append(''.join(content_stack))
                                current_status = 0
                                backup_stack = []
                                content_stack = []
                                backup_status = 0
                        # 如果有路可走
                        else:
                            # 那就走呗
                            backup_stack.insert(0, ch)
                            current_status = self.table[current_status][ch]
            except Exception as e:
                # 每次出现异常，就说明存储在backup_stack中的序列无法作为合法的词，所以一定会忽略一个
                in_error = True
                if reline:
                    errorline = line_count
                if len(backup_stack) == 0:
                    ignore_ch = ch
                else:
                    ignore_ch = backup_stack.pop()
                    assert len(content_stack) == 0
                    content.append(ch)
                    while len(backup_stack) != 0:
                        content.append(backup_stack.pop())
                    current_status = 0
                    backup_status = 0
                error_stack.append(ignore_ch)
            finally:
                pass

            if current_status not in self.end:
                pass
            elif self.end[current_status] in self.__special_pair:
                in_env = True
                properties = self.__special_endings[self.end[current_status].s]
                if properties[2] == 0:
                    preserve_input = True
                else:
                    preserve_input = False
                if properties[1] == 1:
                    expect_status = self.__special_pair[self.end[current_status]]
                elif properties[1] == 0:
                    expect_status = self.end[current_status]
                else:
                    raise Exception('注释区块错误-' + '当前状态：' + str(current_status) + ' 已读取符号:'
                                    + ''.join(content_stack) + ' backup_stack:' + ''.join(backup_stack))
                continue

        # 如果还在注释/字符串环境中
        if in_env:
            if preserve_input:
                lexical_result.append(('', '字符串环境错误！', 0))
                original_input.append(' ')
            else:
                lexical_result.append(('', '注释环境错误！', 0))
                original_input.append(' ')
        elif len(backup_stack) != 0:
            backup_stack.reverse()
            lexical_result.append((''.join(backup_stack), '词法错误！', errorline))
            original_input.append(' ')

        print(lexical_result)
        print(registered_id)
        id_index = {}
        for (key, value) in registered_id.items():
            id_index[value] = key
        return original_input, lexical_result, id_index

    # 输入一个文本，生成词法分析的输出结果
    def lexical_analyse(self, input_filename: str, output_filename: str):
        f = open(input_filename, 'r', encoding='utf-8')
        content = f.read()
        f.close()
        self.Lexical(content)

    def lexical4Syntax(self, input_filename: str, output_filename: str):
        f = open(input_filename, 'r', encoding='utf-8')
        content = f.read()
        f.close()
        o, r, i = self.Lexical4Syntax(content)
        f = open(output_filename, 'w', encoding='utf-8')
        f.write('\n'.join(list(map(lambda x: str(x), r))))
        f.close()
        return o, r, i

    # TODO DFA中消除无效状态

def test():
    enfa = e_NFA()
    enfa.read('FA/java_fa.dfa')
    o, r, i = enfa.lexical4Syntax('Syn_source/java_1.java', 'code_java_result.txt')
    c = cfg_readfile('syntax/java_mine_reCustomed.txt')
    # pda = Automata(c)
    parse = LR_Parser(c)
    parse.parse3(r)


if __name__ == '__main__':
    test()
    # enfa = e_NFA()
    # enfa.compile_regex('regex/regex_java.txt')
    # enfa.write('FA/java_fa.dfa')
    # enfa.read('FA/java_fa.dfa')
    # enfa.read('C:/Users/MSI-PC/De sktop/Compilers_Lab/FA/java_fa.dfa')
    # enfa.lexical_analyse('Syn_source/java_1.java', 'code_java_result.txt')
    # enfa.lexical4Syntax('Syn_source/java_1.java', 'code_java_result.txt')
    pass
