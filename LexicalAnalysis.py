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
        self.fa_node = FA_Node()

    # 自己的补全
    def compile_regex(self, filename: str):
        pass

    # 通过遍历整棵语法树的方法来生成自动机
    def traverse_compile(self, tree: {}):
        # 通过前序遍历构建自动机
        initial_phrase = self.__recursive_traverse(tree)
        print('finished')


    # 根据treenode构造phrase
    def __recursive_traverse(self, tree_node: {}):
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
                return self.__recursive_traverse(value[0])
            # R - B | R
            elif len(sons) == 3 and sons[1].s == '|':
                current_phrase = Phrase(self.fa_node)
                p1 = self.__recursive_traverse(value[0])
                p2 = self.__recursive_traverse(value[2])
                current_phrase.branch(p1, p2)
                return current_phrase
            # B - A B
            elif len(sons) == 2 and sons[1].s != '*':
                current_phrase = Phrase(self.fa_node)
                pre = self.__recursive_traverse(value[0])
                post = self.__recursive_traverse(value[1])
                current_phrase.concatenate(pre, post)
                return current_phrase
            # A - A *
            elif len(sons) == 2 and sons[1].s == '*':
                current_phrase = Phrase(self.fa_node)
                star_phrase = self.__recursive_traverse(value[0])
                current_phrase.star(star_phrase)
                return current_phrase
            # A - ( R )
            elif len(sons) == 3 and sons[0].s == '(':
                return self.__recursive_traverse(value[1])
            # A - entity
            elif len(sons) == 1 and isinstance(sons[0], terminal):
                current_phrase = Phrase(self.fa_node)
                current_phrase.character('e')
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
    c = cfg_readfile('cfg_regex.txt')
    lr = LR_Parser(c)
    lr.parse('( entity ( entity | entity | entity ) entity entity * ) | entity')
    LR_tree = lr.tree
    enfa = e_NFA()
    enfa.traverse_compile(LR_tree)