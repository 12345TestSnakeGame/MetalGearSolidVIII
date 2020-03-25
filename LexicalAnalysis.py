from SyntaxAnalysis import *
import pickle
from graphviz import Digraph


# 产生node，并分配序号
# 可以生出一堆小node
class FA_Node:
    def __init__(self):
        self.count = 0
        self.nodes = {}

    def generate(self):
        new_node = _node(self.count)
        self.nodes[self.count] = new_node
        self.count += 1
        return new_node

    def __repr__(self):
        return '=FA_Node with ' + str(self.count + 1) + ' nodes='

    def __str__(self):
        return self.__repr__()

    def __hash__(self):
        return self.count


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
    def __init__(self, number: int):
        self.number = number
        self.next = {}

    def add_node(self, symbol: Edge, other_node):
        if symbol in self.next:
            self.next[symbol].append(other_node)
        else:
            self.next[symbol] = [other_node]

    def __repr__(self):
        return '-node_' + str(self.number) + '-'

    def __str(self):
        return self.__repr__()

    def __eq__(self, other):
        return other.number == self.number

    def __hash__(self):
        return self.number


class Phrase:
    def __init__(self, Nodes: FA_Node, pre_phrase):
        self.start = Nodes.generate()
        self.end = Nodes.generate()
        pre_phrase.end.add_node(Edge('empty'), self.start)

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

    # 自己的补全
    def compile_regex(self, filename: str):
        pass

    # 通过遍历整棵语法树的方法来生成自动机
    def __traverse_compile(self):
        pass

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
    pass