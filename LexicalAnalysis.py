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


class Phrase:
    def __init__(self, Nodes: FA_Node):
        self.fa_node = Nodes
        self.start = Nodes.generate()
        self.end = Nodes.generate()

    def connect(self, post_phrase):
        self.end.add_node(Edge('empty'), post_phrase.start)

    def concatenate(self, pre, post):
        self.start.add_node(Edge('empty'), pre.start)
        pre.end.add_node(Edge('empty'), post.start)
        post.end.add_node(Edge('empty'), self.end)
        # self.start = pre.start
        # self.end = post.end
        # pre.end.add_node(Edge('empty'), post.start)

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
        self.start.add_node(Edge(ch), self.end)

    def insert(self, phrase):
        # 不！能！直接把phrase原封不动嵌入进来。
        # 因为本质上是同型的自动机在不同的位置，于是起始与终止状态不同
        # self.start.add_node(Edge('empty'), phrase.start)
        # phrase.end.add_node(Edge('empty'), self.end)

        newphrase = Phrase(self.fa_node)
        self.copy(phrase, newphrase)
        self.start.add_node(Edge('empty'), newphrase.start)
        newphrase.end.add_node(Edge('empty'), self.end)

    def copy(self, original_phrase, new_phrase):
        # 还是三集合-广度优先搜索方法最好用
        explored = set()
        to_explore = set()
        exploring = set()
        new_start = new_phrase.start
        old2new = {original_phrase.start:new_start}
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


class DFA(FA):
    def __init__(self):
        super().__init__()

    # 自己的补全
    def compile_regex(self, filename: str):
        pass

    # 输入一段text，生成词法分析的输出结果
    def lexical_analyse(self, text):
        pass

    # 生成正则文法所产生的转换图
    def diagram(self):
        pass


class NFA(FA):
    def __init__(self):
        super().__init__()

    # 自己的补全
    def compile_regex(self, filename: str):
        pass

    # 输入一段text，生成词法分析的输出结果
    def lexical_analyse(self, text):
        pass

    # 生成正则文法所产生的转换图
    def diagram(self):
        pass

    def to_DFA(self):
        pass


class e_NFA(FA):
    def __init__(self):
        super().__init__()
        self.fa_node = FA_Node(0)
        # 默认的正则表达式内置符号。如果有冲突，需要在前面加一个斜杠
        self.__regex_built_in = {'(', ')', '|', '*'}
        self.__stop_symbol = {'\t', '\n', ' ', '$'}
        self.terminals = {}
        self.non_terminals = {}
        # 记录变量出现的顺序
        self.__variable = []
        self.__reg_ex = {}
        self.phrases = {}
        # 不可作为接受状态的变元
        self.__non_acc = set()
        # 从文件中读取正则表达式的构造规则(cfg)，得到LR分析器，用于分析每一条正则表达式的句法结构
        self.__lr = LR_Parser(cfg_readfile('cfg_regex.txt'))
        self.__table = {}
        self.table = {}
        self.end = {}

    # 从文件中读取正则文法，然后构造自动机与转换表
    def compile_regex(self, filename: str):
        time_start = time.time()
        # 正则文法的规则：
        # 第一行：所有的非终结符
        # 第二行：所有的终结符
        # 剩余行：所有的正则文法
        #   在后的正则文法会覆盖前面的正则文法，解决了关键字的问题（没有采用表的方法）
        #   右部中出现的非终结符必须在前面的行出现过
        #   由'#'开头的所有行都会忽略掉，作为注释
        #   由'^'开头的行，其符号只作为变元存在，而不能作为接收状态
        f = open(filename, 'r', encoding='utf-8')
        s = f.readlines()
        f.close()

        lines = []
        for l in s:
            if len(l) <= 1:
                continue
            elif l[0] == '#':
                continue
            if l[-1] == '\n':
                l = l[:-1]
            lines.append(l)

        # non terminals
        Nts = lines[0].split(',')
        for n in Nts:
            self.non_terminals[n] = n_terminal(n)
        # terminals
        Ts = lines[1].split(',')
        for t in Ts:
            self.terminals[t] = terminal(t)
        # regular expressions
        for line in lines[2:]:
            if line[0] == '^':
                line = line[1:]
                chars = line.split(' ')
                var = self.non_terminals[chars[0]]
                self.__non_acc.add(var)
            else:
                chars = line.split(' ')
                var = self.non_terminals[chars[0]]

            self.__variable.append(var)
            expression = []
            for elements in chars[2:]:
                if elements in self.__regex_built_in:
                    continue
                elif elements in self.non_terminals:
                    expression.append(self.non_terminals[elements])
                elif elements in self.terminals:
                    expression.append(self.terminals[elements])
                else:
                    raise Exception('e_NFA:正则表达式读取错误!')
            self.__reg_ex[var] = expression

        # 开始构建自动机
        eNFA = {}
        idx = 2
        for (key, value) in self.__reg_ex.items():
            analyze_str = lines[idx].split(' ')
            idx = idx + 1
            a = []
            for symb in analyze_str:
                if symb in self.__regex_built_in:
                    a.append(symb)
                else:
                    a.append('entity')
            string = ' '.join(a[2:])
            self.__lr.parse(string)
            # self.__lr.visualize_tree()
            tree = self.__lr.tree
            entities = value.copy()
            entities.reverse()

            phrase = self.__traverse_compile(tree, entities)
            self.phrases[key] = phrase
            # self.__visualize_phrase(phrase)
            # print(' ')

        # 子集构造法生成转换表
        # 实际上将正则表达式转换为自动机，通用的方法是直接转换为epsilon-NFA，然后直接子集构造法转换为DFA
        # 因此，另外两个FA的类其实就没有用了
        tab, endings = self.__subset_construct()
        # 写到文件里看看长啥样
        # f = open('result.txt', 'w', encoding='utf-8')
        # for (key, value) in tab.items():
        #     f.write(str(key) + ' -- ' + str(value))
        # f.close()
        # print(tab)
        time_end = time.time()
        print('finished, took ' + str(time_end - time_start) + ' s')

        # 重整转换表
        status_count = len(tab)
        new_table = {}
        end_status = {}
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
            if nt in self.__non_acc:
                continue
            cur_end = endings[nt]
            for (key, value) in new_table.items():
                original_set = set(status[key])
                if cur_end in original_set:
                    end_status[key] = nt
        print(new_table)
        print(end_status)
        self.__table = new_table
        for (key, value) in self.__table.items():
            self.table[key] = {}
            for (key1, value1) in value.items():
                self.table[key][key1.symbol] = value1
        self.end = end_status

    # 子集构造法
    def __subset_construct(self):
        start_node = self.fa_node.generate()
        end_nodes = {}
        # 用一个结点与所有开始状态连接，并记录所有结束状态
        for (key, value) in self.phrases.items():
            start_node.add_node(Edge('empty'), value.start)
            # end_nodes[value.end] = key
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
        end_status = set()
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
                current_phrase = Phrase(self.fa_node)
                p1 = self.__recursive_traverse(value[0], entities)
                p2 = self.__recursive_traverse(value[2], entities)
                current_phrase.branch(p1, p2)
                return current_phrase
            # B - A B
            elif len(sons) == 2 and sons[1].s != '*':
                current_phrase = Phrase(self.fa_node)
                pre = self.__recursive_traverse(value[0], entities)
                post = self.__recursive_traverse(value[1], entities)
                current_phrase.concatenate(pre, post)
                return current_phrase
            # A - A *
            elif len(sons) == 2 and sons[1].s == '*':
                current_phrase = Phrase(self.fa_node)
                star_phrase = self.__recursive_traverse(value[0], entities)
                current_phrase.star(star_phrase)
                return current_phrase
            # A - ( R )
            elif len(sons) == 3 and sons[0].s == '(':
                return self.__recursive_traverse(value[1], entities)
            # A - entity
            elif len(sons) == 1 and isinstance(sons[0], terminal):
                current_phrase = Phrase(self.fa_node)
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

    # 输入一个文本，生成词法分析的输出结果
    def lexical_analyse(self, input_filename: str, output_filename: str):
        f = open(input_filename, 'r', encoding='utf-8')
        content = f.read()
        f.close()
        content = list(content)
        content.reverse()
        content = ['$'] + content

        # 存放词法分析的结果
        lexical_result = []
        backup_status = 0
        current_status = 0
        backup_stack = []
        while len(content) != 0:
            ch = content.pop()

            # 先判断是否是停用词
            if ch in self.__stop_symbol:
                if current_status not in self.end:
                    raise Exception('LexicalAnalyzer:文法错误!')
                else:
                    lexical_result.append(self.end[current_status])
                    current_status = 0
            else:
                # 如果当前状态是一个终结状态，那么当前状态是一个潜在的成功识别符号
                if current_status in self.end:
                    # 如果有可行路径，走
                    if ch in self.table[current_status]:
                        # 当前路径是一个可行符号，先记录下来
                        backup_status = current_status
                        backup_stack.clear()
                        # 哨兵继续探索下一个状态
                        current_status = self.table[current_status][ch]
                        backup_stack.insert(0, ch)
                    # 无路可走了
                    else:
                        # 试着接收
                        lexical_result.append(self.end[current_status])
                        current_status = 0
                        backup_stack.clear()
                        backup_status = 0
                        # 符号再压回去
                        content.append(ch)
                # 如果当前状态不是终结状态，继续向前探索，备份好输入
                else:
                    # 如果无路可走了
                    if ch not in self.table[current_status]:
                        # 如果从初始状态到当前状态还没有碰到过可接受状态
                        if backup_status == 0:
                            raise Exception
                        # 如果碰到过的话，回滚
                        else:
                            lexical_result.append(self.end[backup_status])
                            content += backup_stack
                            current_status = 0
                            backup_stack = []
                            backup_status = 0
                    # 如果有路可走
                    else:
                        # 那就走呗
                        backup_stack.insert(0, ch)
                        current_status = self.table[current_status][ch]
        print(' '.join(list(map(str, lexical_result))))






if __name__ == '__main__':
    # c = cfg_readfile('cfg_regex.txt')
    # lr = LR_Parser(c)
    # lr.parse('( ( ( entity ( entity | entity | entity ) entity entity * ) | entity ) entity ) | entity entity *')
    # LR_tree = lr.tree
    enfa = e_NFA()
    enfa.compile_regex('testCases/regex/regex_C.txt')
    # enfa.visualize_DFA()
    enfa.lexical_analyse('testCases/lexical/lexical_2.txt', 'code_C_result.txt')
    pass

