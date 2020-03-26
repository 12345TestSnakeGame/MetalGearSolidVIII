from SyntaxAnalysis import *
import pickle
from graphviz import Digraph


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
        self.start = Nodes.generate()
        self.end = Nodes.generate()

    def connect(self, post_phrase):
        self.end.add_node(Edge('empty'), post_phrase.start)

    def concatenate(self, pre, post):
        self.start.add_node(Edge('empty'), pre.start)
        pre.end.add_node(Edge('empty'), post.start)
        post.end.add_node(Edge('empty'), self.end)

    def star(self, phrase):
        self.start.add_node(Edge('empty'), self.end)
        self.end.add_node(Edge('empty'), self.start)
        self.start.add_node(Edge('empty'), phrase.start)
        phrase.start.add_node(Edge('empty'), phrase.end)

    def branch(self, p1, p2):
        self.start.add_node(Edge('empty'), p1.start)
        self.start.add_node(Edge('empty'), p2.start)
        p1.end.add_node(Edge('empty'), self.end)
        p2.end.add_node(Edge('empty'), self.end)

    def character(self, ch: str):
        self.start.add_node(Edge(ch), self.end)

    def insert(self, phrase):
        self.start.add_node(Edge('empty'), phrase.start)
        phrase.end.add_node(Edge('empty'), self.end)

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

    # 输入一段text，生成词法分析的输出结果
    def lexical_analyse(self, text):
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
        self.regex_built_in = {'(', ')', '|', '*'}
        self.terminals = {}
        self.non_terminals = {}
        self.reg_ex = {}
        self.phrases = {}
        # 从文件中读取正则表达式的构造规则(cfg)，得到LR分析器，用于分析每一条正则表达式的句法结构
        self.lr = LR_Parser(cfg_readfile('cfg_regex.txt'))

    # 从文件中读取正则文法，然后构造自动机与转换表
    def compile_regex(self, filename: str):
        # 正则文法的规则：
        # 第一行：所有的非终结符
        # 第二行：所有的终结符
        # 剩余行：所有的正则文法
        #   在后的正则文法会覆盖前面的正则文法，解决了关键字的问题（没有采用表的方法）
        #   右部中出现的非终结符必须在前面的行出现过
        #   由'#'开头的所有行都会忽略掉，作为注释
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
            chars = line.split(' ')
            var = self.non_terminals[chars[0]]
            expression = []
            for elements in chars[2:]:
                if elements in self.regex_built_in:
                    continue
                elif elements in self.non_terminals:
                    expression.append(self.non_terminals[elements])
                elif elements in self.terminals:
                    expression.append(self.terminals[elements])
                else:
                    raise Exception('e_NFA:正则表达式读取错误!')
            self.reg_ex[var] = expression

        # 开始构建自动机
        eNFA = {}
        idx = 2
        for (key, value) in self.reg_ex.items():
            analyze_str = lines[idx].split(' ')
            idx = idx + 1
            a = []
            for symb in analyze_str:
                if symb in self.regex_built_in:
                    a.append(symb)
                else:
                    a.append('entity')
            string = ' '.join(a[2:])
            self.lr.parse(string)
            tree = self.lr.tree
            entities = value.copy()
            entities.reverse()

            phrase = self.__traverse_compile(tree, entities)
            self.phrases[key] = phrase

        # 子集构造法生成转换表
        # 实际上将正则表达式转换为自动机，通用的方法是直接转换为epsilon-NFA，然后直接子集构造法转换为DFA
        # 因此，另外两个FA的类其实就没有用了
        self.__subset_construct()
        print('finished')

    def __subset_construct(self):
        start_node = self.fa_node.generate()
        end_nodes = {}
        # 用一个结点与所有开始状态连接，并记录所有结束状态
        for (key, value) in self.phrases.items():
            start_node.add_node(Edge('empty'), value.start)
            end_nodes[key] = value.end
        # 类似于广度优先搜索
        to_explore = set()
        explored = set()
        exploring = {set(self.__eclosure(start_node))}
        fa_table = {}
        end_status = set()
        while len(exploring) != 0:
            # 对每个状态子集
            for s in exploring:
                # 对状态子集中的每个状态
                # 所有状态的所有可达状态
                switch_table = {}
                for k in s:
                    for (key, value) in k.items():
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
                    if value not in explored and value not in exploring:
                        to_explore.add(value)
                    origin = [s]
                    origin.sort()
                    origin = tuple(origin)
                    if origin in fa_table:
                        fa_table[origin][key] = value
                    else:
                        fa_table[origin] = {key: value}
                explored.add(s)
            exploring = to_explore.copy()
            to_explore.clear()

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
        self.__visualize_phrase(initial_phrase)
        return initial_phrase

    def __visualize_phrase(self, p: Phrase):
        dot = Digraph(comment='finite automata')
        dot.node(p.start.__str__(), p.start.__str__())
        edge_set = set()
        self.__visualize_node(p.start, dot, edge_set)
        dot.view()

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

    # 输入一段text，生成词法分析的输出结果
    def lexical_analyse(self, text):
        pass

    # 生成正则文法所产生的转换图
    def diagram(self):
        pass

    def to_NFA(self):
        pass


if __name__ == '__main__':
    # c = cfg_readfile('cfg_regex.txt')
    # lr = LR_Parser(c)
    # lr.parse('( ( ( entity ( entity | entity | entity ) entity entity * ) | entity ) entity ) | entity entity *')
    # LR_tree = lr.tree
    enfa = e_NFA()
    enfa.compile_regex('regex_C.txt')
    pass
