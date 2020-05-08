from graphviz import Digraph


# 符号
class symbol:
    def __init__(self, name: str):
        self.s = name

    def __str__(self):
        return self.s

    def __repr__(self):
        return self.s

    def __eq__(self, other):
        return other.s == self.s

    def __hash__(self):
        return hash(self.s)

    def __lt__(self, other):
        return self.s < other.s

    def __le__(self, other):
        return self.s <= other.s

    def __gt__(self, other):
        return self.s > other.s

    def __ge__(self, other):
        return self.s >= other.s


# 非终结符
class n_terminal(symbol):
    def __init__(self, name: str):
        symbol.__init__(self, name)
        self.type = 'N'


# 终结符
class terminal(symbol):
    def __init__(self, name: str):
        symbol.__init__(self, name)
        self.type = 'T'


# 空字符
class empty_terminal(terminal):
    def __init__(self, name: str):
        terminal.__init__(self, 'empty')
        self.type = 'T'


# 句尾符号
class end_terminal(terminal):
    def __init__(self, name: str):
        terminal.__init__(self, '$')
        self.type = 'T'


# 由左部和右部组成的一条产生式
# 左部为非终结符，右部为终结符与非终结符的序列
class rule:
    def __init__(self, left: n_terminal, rights: [symbol, ]):
        self.left = left
        self.right = rights
        self.count = self.right.__len__()
        self.__strHash()

    def __strHash(self):
        h = hash(self.left.s)
        for k in self.right:
            h += hash(k.s)
        self.ha = h

    def __repr__(self):
        return self.left.s + ' -> ' + ' '.join(list(map(lambda x: str(x), self.right)))

    def __eq__(self, other):
        return other.left == self.left and other.right == self.right

    def __hash__(self):
        return hash(self.left) + sum(list(map(lambda x: hash(x), self.right)))

    def __lt__(self, other):
        return self.ha < other.ha

    def __le__(self, other):
        return self.ha <= other.ha

    def __gt__(self, other):
        return self.ha > other.ha

    def __ge__(self, other):
        return self.ha >= other.ha


class item(rule):
    def __init__(self, position: int, left: n_terminal, rights: [symbol, ]):
        if len(rights) == 0:
            raise Exception
        # TODO 这里可能会是一个问题。只判断了是不是empty，且只适用于右部只有empty一个元素的情况。没有计算empty的位置和数量
        if isinstance(rights[0], empty_terminal):
            self.empty = True
        else:
            self.empty = False
        if position == len(rights) or (len(rights) == 1 and self.empty):
            self.reduce = True
            self.has_successive = False
        else:
            self.reduce = False
            self.has_successive = True
        rule.__init__(self, left, rights)
        self.position = position
        self.__operation_cache = {}
        self.core = (self.left, tuple(self.right), self.position)
        self.__strHash()

    def __strHash(self):
        h = hash(self.left.s)
        for k in self.right:
            h += hash(k.s)
        h += self.position
        self.ha = h

    def __repr__(self):
        l_part = ' '.join(list(map(lambda x: str(x), self.right[0:self.position])))
        r_part = ' '.join(list(map(lambda x: str(x), self.right[self.position:])))
        return self.left.s + ' -> ' + l_part + ' · ' + r_part

    def __eq__(self, other):
        return other.left == self.left and other.right == self.right and self.position == other.position

    def __hash__(self):
        count = 1
        for v in self.right:
            count += hash(v)
        count *= (hash(self.left) + 1)
        count *= (self.position + 1)
        return count

    # 转换为产生式
    def to_rule(self):
        return rule(self.left, self.right)

    def merge(self, other):
        if not self.core == other.origin:
            return None
        return self

    def successive_symbol(self):
        # TODO 这里没有对空产生式进行处理。是因为保证了空产生式不会运行到这一步吗
        if len(self.right) == self.position:
            return None
        else:
            all_empty = True
            first_nonempty_position = -1
            met = False
            for idx in range(self.position, len(self.right)):
                if not isinstance(self.right[idx], empty_terminal):
                    all_empty = False
                    if not met:
                        first_nonempty_position = idx
                        met = True
                    break
            if all_empty:
                return None
            else:
                return self.right[first_nonempty_position]
        # return self.right[self.position]

    def successive_item(self):
        # TODO bug出在这个位置
        # 已经匹配到了结尾
        if len(self.right) == self.position:
            return None
        else:
            p = self.position
            while p != len(self.right):
                if not isinstance(self.right[p], empty_terminal):
                    return item(p, self.left, self.right)
                p += 1
            if p == len(self.right):
                return item(p, self.left, self.right)

        raise Exception('程序不应该到达这里！')
        # return item(self.position + 1, self.left, self.right)


class item_lookahead(item):
    def __init__(self, position: int, left: n_terminal, rights: [symbol, ], lookahead: set):
        item.__init__(self, position, left, rights)
        self.lookahead = lookahead
        self.CFG_imported = False
        self.CFG = None

    def __strHash(self):
        h = hash(self.left.s)
        for k in self.right:
            h += hash(k.s)
        h += self.position
        for z in self.lookahead:
            h += hash(z)
        self.ha = h

    def __hash__(self):
        count = 0
        for v in self.right:
            count += hash(v)
        count *= (hash(self.left) + 1)
        count *= (self.position + 1)
        for k in self.lookahead:
            count += hash(k)
        return count

    def __eq__(self, other):
        return other.left == self.left and other.right == self.right and self.position == other.position and \
               self.lookahead == other.lookahead

    def __repr__(self):
        l_part = ' '.join(list(map(lambda x: str(x), self.right[0:self.position])))
        r_part = ' '.join(list(map(lambda x: str(x), self.right[self.position:])))
        ss =  self.left.s + ' -> ' + l_part + ' · ' + r_part
        return ss + ', ' + ' '.join(list(map(str, list(self.lookahead))))

    def __str__(self):
        l_part = ' '.join(list(map(lambda x: str(x), self.right[0:self.position])))
        r_part = ' '.join(list(map(lambda x: str(x), self.right[self.position:])))
        ss = self.left.s + ' -> ' + l_part + ' · ' + r_part
        return ss + ', ' + ''.join(list(map(str, list(self.lookahead))))


    # 计算first集合必须要cfg本体
    def import_CFG(self, CFG):
        self.CFG = CFG
        self.CFG_imported = True

    def next_lookahead(self):
        if self.position >= len(self.right):
            return None
        elif isinstance(self.right[self.position], terminal):
            return None
        else:
            s = self.CFG.select(self.right[self.position + 1:])
            if empty_terminal('empty') in s:
                s.remove(empty_terminal('empty'))
                s = s.union(self.lookahead)
            return s


    def merge(self, other):
        if not self.core == other.core:
            return None

        return item_lookahead(self.position, self.left, self.right, self.lookahead.union(other.lookahead))

    def successive_item(self):
        if len(self.right) == self.position:
            return None
        else:
            p = self.position + 1
            while p != len(self.right):
                if not isinstance(self.right[p], empty_terminal):
                    return item_lookahead(p, self.left, self.right, self.lookahead)
                p += 1
            # if p == len(self.right):
            #     return None
            return item_lookahead(p, self.left, self.right, self.lookahead)
        # return item_lookahead(self.position + 1, self.left, self.right, self.lookahead)


# 读取CFG文法，生成FIRST，FOLLOW和SELECT集
class cfg:
    def __init__(self, start: n_terminal, n_terminals: [], terminals: [], rules: []):
        # 初始符号，非终结符，终结符与产生式
        self.start = start
        self.n_terminals = n_terminals
        self.terminals = terminals
        self.rules = rules

        # 由产生式获取其序号
        self.rule_number = {}
        for idx in range(0, len(rules)):
            self.rule_number[rules[idx]] = idx

        # namelist可以根据字符串检索符号
        self.namelist = {}
        for s in n_terminals + terminals:
            self.namelist[s.s] = s
        if 'empty' not in self.namelist:
            self.namelist['empty'] = empty_terminal('empty')

        # 分别计算 first， follow与select集
        self.FIRST = {}
        self.FOLLOW = {}
        self.SELECT = {}
        self.__first()
        self.__follow()
        self.__select()

    # 获得以left为左部的所有生成式
    def get_rule(self, left_: n_terminal):
        rs = []
        for r in self.rules:
            if r.left == left_:
                rs.append(r)
        return rs

    # 获得以left为左部的产生式的初始项目
    def get_item(self, left_: n_terminal):
        rs = []
        for r in self.rules:
            if r.left == left_:
                rs.append(item(0, r.left, r.right))
        return rs

    # 获得对应下标的产生式
    def rule_by_number(self, number: int):
        return self.rules[number]

    # 获取产生式对应的下标
    def number_by_rule(self, r: rule):
        return self.rules.index(r)

    # 计算一个串的first集合。该串的所有符号都应该是cfg当中的符号
    def select(self, w: []):
        # 若串的长度为0，则select集合中只包含空串
        if len(w) == 0:
            return {empty_terminal('empty')}
        s = set()
        no_empty = False
        for idx in range(0, len(w) + 1):
            if no_empty:
                break
            no_empty = True
            # 能够走到结尾说明前面的串都可以为空
            if idx == len(w):
                s.add(empty_terminal('empty'))
                break
            for ccc in self.FIRST[w[idx]]:
                if ccc.s == 'empty':
                    no_empty = False
                    continue
                s.add(ccc)
        return s

    # 计算每个产生式的select集
    def __select(self):
        # 对每条产生式
        for r in self.rules:
            self.SELECT[r] = set()

            no_empty = False
            for i in range(0, len(r.right) + 1):
                if no_empty:
                    break
                no_empty = True
                if i == len(r.right):
                    for v in self.FOLLOW[r.left]:
                        self.SELECT[r].add(v)
                    break
                cur = r.right[i]
                for v in self.FIRST[cur]:
                    if isinstance(v, empty_terminal):
                        no_empty = False
                        continue
                    self.SELECT[r].add(v)

    # 计算每个符号的follow集
    def __follow(self):
        # follow集只对非终结符有
        for nt in self.n_terminals:
            self.FOLLOW[nt] = set()

        # 开始符的follow集添加一个end
        self.FOLLOW[self.start].add(end_terminal('$'))

        # 与__first相同，直到不发生变化时停止循环
        change = True
        while change:
            change = False
            # 对每一个生成式
            for cur in self.rules:
                # 从尾部向前搜索
                for idx in range(len(cur.right) - 1, -1, -1):
                    # 对于最后一个符号是非终结符的情况，在其follow集中添加左部的first集中的非空元素
                    if idx == len(cur.right) - 1 and isinstance(cur.right[idx], n_terminal):
                        for temp in self.FOLLOW[cur.left]:
                            if not isinstance(temp, empty_terminal) and temp not in self.FOLLOW[cur.right[idx]]:
                                self.FOLLOW[cur.right[idx]].add(temp)
                                change = True
                    # 对于非最后一个符号是非终结符的情况，在其follow集中添加first（其后的子串）
                    elif idx < len(cur.right) - 1 and isinstance(cur.right[idx], n_terminal):
                        # 对其后的子串进行遍历
                        no_empty = False
                        for k in range(idx + 1, len(cur.right) + 1):
                            if no_empty:
                                break
                            no_empty = True
                            # 当遍历到最后一符号，说明前面的所有符号都可以为空
                            if k == len(cur.right):
                                for temp in self.FOLLOW[cur.left]:
                                    if not isinstance(temp, empty_terminal) and temp not in self.FOLLOW[cur.right[idx]]:
                                        self.FOLLOW[cur.right[idx]].add(temp)
                                        change = True
                                break
                            for temp in self.FIRST[cur.right[k]]:
                                if isinstance(temp, empty_terminal):
                                    no_empty = False
                                    continue
                                if temp not in self.FOLLOW[cur.right[idx]]:
                                    self.FOLLOW[cur.right[idx]].add(temp)
                                    change = True

    # 计算每个符号的first集
    def __first(self):
        # 首先，所有的终结符的first是自己本身
        for t in self.terminals:
            self.FIRST[t] = set([t])
        # 初始化非终结符的first集合
        for nt in self.n_terminals:
            self.FIRST[nt] = set()

        # 能够推导出空串的非终结符
        empty_set = set()

        # 设置change，当所有symbol的first集不再变化时停止循环
        change = True
        while change:
            change = False
            # 对每一条产生式
            for cur in self.rules:
                # 产生式左部的新first集合
                new_first_symbol = set()
                no_empty = False
                for idx in range(0, len(cur.right) + 1):
                    if no_empty:
                        break
                    no_empty = True
                    # 循环到尾，说明前面的符号都可以为空串，那么first集合中包含空串
                    if idx == len(cur.right):
                        new_first_symbol.add(self.namelist['empty'])
                        break
                    # 对第idx个符号进行检查
                    # 循环到idx，说明idx前面的符号都可以为空，因此将idx符号first集中的所有元素加入
                    cur_sym = cur.right[idx]
                    for cur_first in self.FIRST[cur_sym]:
                        if isinstance(cur_first, empty_terminal):
                            no_empty = False
                        else:
                            new_first_symbol.add(cur_first)
                # 如果有新的符号可以添加
                if len(new_first_symbol - self.FIRST[cur.left]) > 0:
                    for sy in new_first_symbol:
                        self.FIRST[cur.left].add(sy)
                    change = True

    def __eq__(self, other):
        return self.start == other.start and self.n_terminals == other.n_terminals and \
               self.terminals == other.terminals and self.rules == other.rules

    def __hash__(self):
        return hash(self.start) + hash(self.terminals) + hash(self.n_terminals) + hash(self.rules)

    def __str__(self):
        s = ''
        s += '\n\nFIRST\n' + str(self.FIRST)
        s += '\n\nFOLLOW\n' + str(self.FOLLOW)
        s += '\n\nSELECT\n' + str(self.SELECT)
        return s

    def __repr__(self):
        return self.__str__()

class closure:
    def __init__(self, number: int, items: [item, ]):
        self.number = number
        self.items = items
        self.core = set(map(lambda x: x.core, items))

    def set_number(self, number: int):
        self.number = number

    # *** 只在item为item_lookahead的时候才可以调用 ***
    def closure_merge(self, other):
        s = list(self.core)
        s.sort()
        o = list(other.core)
        o.sort()
        if hash(tuple(s)) != hash(tuple(o)):
            raise Exception('两个closure的核心不相同')
        newitems = []
        for i in self.items:
            for j in other.items:
                if hash(i.core) == hash(j.core):
                    i.merge(j)
            newitems.append(i)
        return closure(self.number, newitems)

    def __eq__(self, other):
        # return self.number == other.number and self.items == other.items
        return self.items == other.items

    def __repr__(self):
        return 'I' + str(self.number) + '\n' + '\n'.join(list(map(lambda x: str(x), self.items)))

    def __hash__(self):
        count = 0
        for i in self.items:
            count -= i.__hash__()
        # 不同序号的closure有可能是同一个
        # count *= (self.number + 1)
        return count

    def __lt__(self, other):
        return self.number < other.number

    def __le__(self, other):
        return self.number <= other.number

    def __gt__(self, other):
        return self.number > other.number

    def __ge__(self, other):
        return self.number >= other.number


# 语法分析表
class ParsingTable:
    def __init__(self, table: {}, terminal_list: [], n_terminal_list: []):
        self.ACTION = []
        self.GOTO = []
        # 存放符号到列数的映射
        self.symbol_index = {}
        self.t = {}
        self.nt = {}
        for idx in range(len(terminal_list)):
            self.t[terminal_list[idx].s] = idx
        for idx in range(len(n_terminal_list)):
            self.nt[n_terminal_list[idx].s] = idx

        action_tab = table['ACTION']
        count = 0
        for (key, value) in action_tab.items():
            self.ACTION.append([])
            for (key1, value1) in value.items():
                self.ACTION[count].append(value1)
            count = count + 1
        goto_tab = table['GO']
        count = 0
        for (key, value) in goto_tab.items():
            self.GOTO.append([])
            for (key1, value1) in value.items():
                self.GOTO[count].append(value1)
            count += 1

    def get_action(self, status: int, tstr: str):
        idx = self.t[tstr]
        return self.ACTION[status][idx]

    def get_goto(self, status: int, n_tstr: str):
        idx = self.nt[n_tstr]
        return self.GOTO[status][idx]

    def __string(self):
        string = 'ACTION\n\t' + '\t'.join(self.t) + '\n'
        for i in range(len(self.ACTION)):
            string = string + str(i) + '\t'
            for k in self.ACTION[i]:
                if len(k) == 0:
                    string += '[]\t'
                else:
                    string += ','.join(list(map(lambda x: str(x[0]) + str(x[1]), k))) + '\t'
            string += '\n'
        string += '\nGOTO\n\t' + '\t'.join(self.nt) + '\n'
        for i in range(len(self.GOTO)):
            string = string + str(i) + '\t'
            for k in self.GOTO[i]:
                if len(k) == 0:
                    string += '[]\t'
                else:
                    string += ','.join(list(map(lambda x: str(x[0]) + str(x[1]), k))) + '\t'
            string += '\n'
        return string

    def __repr__(self):
        return self.__string()

    def __str__(self):
        return self.__string()


# 生成NFA自动机。专门用于自底向上的分析方法，包括LR(0),SLR,LR(1),LALR
class Automata:
    def __init__(self, lang: cfg, lr_mode = 'LR1'):
        self.CFG = lang

        # 计算LR(0)
        # self.__initial_closure = self.__initial_closure_LR0
        # self.__cal_items = self.__cal_items_LR0
        # c_pool, s_trans, i2c, il = self.__construct_automata()
        # self.__construct_table_LR0(c_pool, s_trans)

        # 计算SLR
        # self.__construct_table_SLR(c_pool, s_trans)

        # 计算LR(1)
        self.__initial_closure = self.__initial_closure_LR1
        self.__cal_items = self.__cal_items_LR1
        c_pool, s_trans, i2c, il = self.__construct_automata()
        self.__construct_table_LR1(c_pool, s_trans, i2c, il)

        # 计算LALR
        # self.__construct_table_LALR(c_pool, s_trans)
        # self.__construct_table()
        # self.closure_dict = {}

        self.table = self.table_LR1

        # TODO 造出一个完整的自动机的数据结构
        # LR0, SLR, LR1, LALR

    # 计算rules_对应的closure
    def __cal_items(self, rules_: []):
        if len(rules_) == 0:
            return []
        cur_rules = rules_.copy()
        # 我妥协了，还是得加个if判断
        if type(rules_[0]) == item_lookahead:
            change = True
            while change:
                change = False
                l = len(cur_rules)
                for idx in range(0, l):
                    # 先获得raw后继符号
                    s_symbol = cur_rules[idx].successive_symbol()
                    if not s_symbol:
                        continue
                    new_rule = self.CFG.get_rule(s_symbol)
                    for ii in range(len(cur_rules)):
                        cur_rules[ii].import_CFG(self.CFG)
                    look = cur_rules[idx].next_lookahead()
                    new_item = list(map(lambda x: item_lookahead(0, x.left, x.right, look), new_rule))
                    add_rule = list(filter(lambda x: x not in cur_rules, new_item))
                    cur_rules += add_rule
                if len(cur_rules) > l:
                    change = True
            # 去重，无展望符情况下无用
            rule_dict = {}
            for r in cur_rules:
                if r.core not in rule_dict:
                    rule_dict[r.core] = r
                else:
                    rule_dict[r.core] = rule_dict[r.core].merge(r)

            cur_rules = []
            for (key, value) in rule_dict.items():
                cur_rules.append(value)
            return cur_rules

        change = True
        while change:
            change = False
            l = len(cur_rules)
            for idx in range(0, l):
                s_symbol = cur_rules[idx].successive_symbol()
                if not s_symbol:
                    continue
                new_rule = self.CFG.get_rule(s_symbol)

                new_item = list(map(lambda x: item(0, x.left, x.right), new_rule))
                add_rule = list(filter(lambda x: x not in cur_rules, new_item))
                # cur_rules += list(map(lambda x: item(0, x.left, x.right), add_rule))
                cur_rules += add_rule
            if len(cur_rules) > l:
                change = True

        return cur_rules

    # 返回由rules_中的项目所生成的closure中的所有项目, rules_中是普通的item
    # 可用于LR(0)与SLR
    def __cal_items_LR0(self, rules_: []):
        if len(rules_) == 0:
            return []
        cur_rules = rules_.copy()

        change = True
        while change:
            change = False
            l = len(cur_rules)
            for idx in range(0, l):
                s_symbol = cur_rules[idx].successive_symbol()
                if not s_symbol:
                    continue
                new_rule = self.CFG.get_rule(s_symbol)

                new_item = list(map(lambda x: item(0, x.left, x.right), new_rule))
                add_rule = list(filter(lambda x: x not in cur_rules, new_item))
                # cur_rules += list(map(lambda x: item(0, x.left, x.right), add_rule))
                cur_rules += add_rule
            if len(cur_rules) > l:
                change = True

        return cur_rules

    # 返回由rules_中的项目所生成的closure中的所有项目, rules_中存放带展望符的item，即item_lookahead
    # 可用于LR(1)与LALR
    def __cal_items_LR1(self, rules_: []):
        if len(rules_) == 0:
            return []
        cur_rules = rules_.copy()
        # 我妥协了，还是得加个if判断
        if type(rules_[0]) == item_lookahead:
            change = True
            while change:
                change = False
                l = len(cur_rules)
                for idx in range(0, l):
                    # 先获得raw后继符号
                    s_symbol = cur_rules[idx].successive_symbol()
                    if not s_symbol:
                        continue
                    new_rule = self.CFG.get_rule(s_symbol)
                    for ii in range(len(cur_rules)):
                        cur_rules[ii].import_CFG(self.CFG)
                    look = cur_rules[idx].next_lookahead()
                    new_item = list(map(lambda x: item_lookahead(0, x.left, x.right, look), new_rule))
                    add_rule = list(filter(lambda x: x not in cur_rules, new_item))
                    cur_rules += add_rule
                if len(cur_rules) > l:
                    change = True
            # 去重，无展望符情况下无用
            rule_dict = {}
            for r in cur_rules:
                if r.core not in rule_dict:
                    rule_dict[r.core] = r
                else:
                    rule_dict[r.core] = rule_dict[r.core].merge(r)

            cur_rules = []
            for (key, value) in rule_dict.items():
                cur_rules.append(value)
            return cur_rules

    # 返回采用LR(0)的自动机的初始closure, 里面是item
    def __initial_closure_LR0(self):
        initial_rules = self.CFG.get_rule(self.CFG.start)
        initial_items = list(map(lambda x: item(0, x.left, x.right), initial_rules))
        map(lambda x: x.import_CFG(self.CFG), initial_items)
        return closure(0, self.__cal_items_LR0(initial_items))

    # 返回采用LR(1)的自动机的初始closure， 里面是item_lookahead
    def __initial_closure_LR1(self):
        initial_rules = self.CFG.get_rule(self.CFG.start)
        initial_items = list(map(lambda x: item_lookahead(0, x.left, x.right, {end_terminal('$')}), initial_rules))
        map(lambda x: x.import_CFG(self.CFG), initial_items)
        return closure(0, self.__cal_items_LR1(initial_items))

    # 根据产生式计算自动机
    # 默认使用LR(1)
    def __construct_automata(self):
        # 对状态集的计数
        count = 0
        # 存放closure之间的转换映射
        status_trans = {}
        # 首先获得初始状态
        # initial_rules = self.CFG.get_rule(self.CFG.start)
        # # initial_items = list(map(lambda x: item(0, x.left, x.right), initial_rules))
        # initial_items = list(map(lambda x: item_lookahead(0, x.left, x.right, {end_terminal('$')}), initial_rules))
        # map(lambda x: x.import_CFG(self.CFG), initial_items)
        # i_r_closure = closure(count, self.__cal_items(initial_items))
        i_r_closure = self.__initial_closure()

        # 存放已经遍历到的closure，无序
        closure_pool = set()
        # 存放在下一个循环将要遍历的状态，有序
        to_explore = [i_r_closure]
        # 当前循环下正在遍历的状态们，有序
        exploring = []

        # closures与序号
        # TODO 有很小的几率两个closure的hash值相同，但是用list感觉好麻烦。。。
        items = i_r_closure.items
        items.sort()
        # TODO 变成tuple之后，在右部包含包括空状态的多个状态的产生式的项目之间的等价性比较会不会出问题？
        status_dict = {count: tuple(items)}
        reversed_status_dict = {tuple(items): count}

        item2closure = {tuple(items): i_r_closure}
        itemList = [tuple(items)]

        numberSet = set()

        # 不断循环直到没有可遍历的状态了
        while len(to_explore) > 0:
            exploring = to_explore.copy()
            to_explore.clear()
            # 对每一个状态（按广度优先搜索顺序）
            # for status in exploring:
            while len(exploring) != 0:
                # 看顺序不对就换
                status = exploring[0]

                exploring = exploring[1:]
                numberSet.add(status.number)
                # 对状态中的每一个产生式，找到其可行的后继产生式与对应的输入符号 （同样按顺序）
                # origin_closure: 原状态的序号
                # s_rule: 状态之间的映射 TODO 同样，有很小的概率，key的hash值相同
                origin_closure = status.number
                s_rule = {}
                for r in status.items:
                    if not r.has_successive:
                        continue
                    s_item = r.successive_item()
                    s_symbol = r.successive_symbol()
                    # TODO 这里有错吗
                    if s_symbol in s_rule:
                        s_rule[s_symbol].append(s_item)
                    else:
                        s_rule[s_symbol] = [s_item]
                end_item = status.items
                end_item.sort()
                assert tuple(end_item) in itemList
                # TODO 如果s_rule为空呢
                # 对每个可行的移进
                for (key, value) in s_rule.items():
                    # 求出由该移进的项目生成的closure
                    temp_closure = closure(count + 1, self.__cal_items(value))
                    temp_items = temp_closure.items
                    temp_items.sort()
                    temp_tuple = tuple(temp_items)
                    # 如果是已经建立过的状态
                    # if temp_closure in closure_pool or temp_closure in exploring or temp_closure in to_explore:
                    if temp_tuple in itemList:
                        assert temp_tuple in item2closure
                        temp_number = reversed_status_dict[temp_tuple]
                        if origin_closure in status_trans:
                            # assert (key, temp_number) not in status_trans[origin_closure]
                            status_trans[origin_closure].append((key, temp_number))
                        else:
                            status_trans[origin_closure] = [(key, temp_number)]
                        continue
                    # 如果是为建立的状态
                    itemList.append(temp_tuple)
                    assert temp_tuple not in item2closure
                    item2closure[temp_tuple] = temp_closure
                    count = count + 1
                    to_explore.append(temp_closure) # TODO 这里应该不会重复吧。。。。
                    if origin_closure in status_trans:
                        status_trans[origin_closure].append((key, count))
                    else:
                        status_trans[origin_closure] = [(key, count)]
                    # assert count not in status_dict
                    assert temp_tuple not in reversed_status_dict
                    if temp_tuple in reversed_status_dict:
                        print(temp_tuple)
                        print(status_dict[reversed_status_dict[temp_tuple]])
                        raise Exception
                    status_dict[count] = temp_tuple
                    reversed_status_dict[temp_tuple] = count
                closure_pool.add(status)
            # for v in exploring:
            #     closure_pool.add(v)
        #
        # print('len ' + str(len(numberSet)))
        # print('max ' + str(max(numberSet)))
        return closure_pool, status_trans, item2closure, itemList

    # 为LALR设计。将closure_pool中核心相同的项集合并，返回合并后的项目集与转移映射
    def __merge_closures(self, closure_pool, status_trans: {}):
        closure_core = {}
        closure_d = {}
        equivalent_sets = {}
        for c in closure_pool:
            closure_d[c.number] = c
            l = list(c.core)
            l.sort()
            l_tuple = tuple(l)
            if l_tuple in equivalent_sets:
                equivalent_sets[l_tuple].append(c.number)
            else:
                equivalent_sets[l_tuple] = [c.number]

        new_pool = set()
        new_trans = {}
        olocount = len(equivalent_sets)
        # 建立从旧项目集到新项目集的对应关系
        old2ind = {}
        old2new = {}
        new_list = []
        for (key, value) in equivalent_sets.items():
            n = min(value)
            new_list.append(n)
            for v in value:
                old2ind[v] = n
        new_list.sort()
        for idx in range(len(new_list)):
            old2new[new_list[idx]] = idx

        for (key, value) in equivalent_sets.items():
            elem = value[0]
            indicate = old2new[old2ind[elem]]
            c = closure_d[elem]
            for cc in value[1:]:
                c = c.closure_merge(closure_d[cc])
            c.number = indicate
            new_pool.add(c)

        for (key, value) in status_trans.items():
            for o in value:
                src = old2new[old2ind[key]]
                tar = old2new[old2ind[o[1]]]
                symb = o[0]
                if src in new_trans:
                    new_trans[src].append((symb, tar))
                else:
                    new_trans[src] = [(symb, tar)]
        return new_pool, new_trans

    # 根据自动机生成分析表
    # 默认根据LR(1)生成
    def __construct_table(self):
        # *** item_lookahead only ***
        self.table = {'ACTION':{}, 'GO':{}}
        terminal_list = list(self.CFG.terminals) + [end_terminal('$')]
        n_terminal_list = list(self.CFG.n_terminals)
        # 初始化
        for idx in range(0, self.closure_count + 1):
            self.table['GO'][idx] = {}
            self.table['ACTION'][idx] = {}
            for n in n_terminal_list:
                self.table['GO'][idx][n] = []
            for t in terminal_list:
                if not isinstance(t, empty_terminal):
                    self.table['ACTION'][idx][t] = []
        # 填充移进
        for (key, value) in self.to_dict.items():
            for targets in value:
                if isinstance(targets[0], n_terminal):
                    self.table['GO'][key][targets[0]].append(('s', targets[1]))
                elif isinstance(targets[0], terminal):
                    self.table['ACTION'][key][targets[0]].append(('s', targets[1]))
        # 填充归约
        for (key, value) in self.closure_dict.items():
            for i in value.items:
                if i.reduce:
                    for follows in i.lookahead:
                        self.table['ACTION'][key][follows].append(('r', self.CFG.rule_number[i.to_rule()]))

    def __construct_table_LR0(self, closure_pool, status_trans: {}):
        closure_count = len(closure_pool)
        closure_dict = {}
        for k in closure_pool:
            closure_dict[k.number] = k
        table = {'ACTION': {}, 'GO': {}}
        terminal_list = list(self.CFG.terminals) + [end_terminal('$')]
        if empty_terminal('empty') in terminal_list:
            terminal_list.remove(empty_terminal('empty'))
        n_terminal_list = list(self.CFG.n_terminals)
        # 初始化
        for idx in range(0, closure_count + 1):
            table['GO'][idx] = {}
            table['ACTION'][idx] = {}
            for n in n_terminal_list:
                table['GO'][idx][n] = []
            for t in terminal_list:
                if not isinstance(t, empty_terminal):
                    table['ACTION'][idx][t] = []
        # 填充移进
        for (key, value) in status_trans.items():
            for targets in value:
                if isinstance(targets[0], n_terminal):
                    table['GO'][key][targets[0]].append(('s', targets[1]))
                elif isinstance(targets[0], terminal):
                    table['ACTION'][key][targets[0]].append(('s', targets[1]))
        # 填充归约
        for (key, value) in closure_dict.items():
            for i in value.items:
                if i.reduce:
                    for follows in terminal_list:
                        table['ACTION'][key][follows].append(('r', self.CFG.rule_number[i.to_rule()]))

        self.closures_LR0 = closure_dict
        self.trans_LR0 = status_trans
        self.table_LR0 = ParsingTable(table, terminal_list, n_terminal_list)

    def __construct_table_SLR(self, closure_pool, status_trans: {}):
        closure_count = len(closure_pool)
        closure_dict = {}
        for k in closure_pool:
            closure_dict[k.number] = k
        table = {'ACTION': {}, 'GO': {}}
        terminal_list = list(self.CFG.terminals) + [end_terminal('$')]
        if empty_terminal('empty') in terminal_list:
            terminal_list.remove(empty_terminal('empty'))
        n_terminal_list = list(self.CFG.n_terminals)
        # 初始化
        for idx in range(0, closure_count + 1):
            table['GO'][idx] = {}
            table['ACTION'][idx] = {}
            for n in n_terminal_list:
                table['GO'][idx][n] = []
            for t in terminal_list:
                if not isinstance(t, empty_terminal):
                    table['ACTION'][idx][t] = []
        # 填充移进
        for (key, value) in status_trans.items():
            for targets in value:
                if isinstance(targets[0], n_terminal):
                    table['GO'][key][targets[0]].append(('s', targets[1]))
                elif isinstance(targets[0], terminal):
                    table['ACTION'][key][targets[0]].append(('s', targets[1]))
        # 填充归约
        for (key, value) in closure_dict.items():
            for i in value.items:
                if i.reduce:
                    for follows in self.CFG.FOLLOW[i.left]:
                        table['ACTION'][key][follows].append(('r', self.CFG.rule_number[i.to_rule()]))

        self.closures_SLR = closure_dict
        self.trans_SLR = status_trans
        self.table_SLR = ParsingTable(table, terminal_list, n_terminal_list)

    def __construct_table_LR1(self, closure_pool, status_trans: {}, item2Closure: dict, itemList: []):
        closure_count = len(itemList)
        # assert len(itemList) != len(closure_pool)
        closure_dict = {}
        for k in itemList:
            closure_dict[item2Closure[k].number] = item2Closure[k]
        table = {'ACTION': {}, 'GO': {}}
        terminal_list = list(self.CFG.terminals) + [end_terminal('$')]
        if empty_terminal('empty') in terminal_list:
            terminal_list.remove(empty_terminal('empty'))
        n_terminal_list = list(self.CFG.n_terminals)
        # 初始化
        for idx in range(0, closure_count + 1):
            table['GO'][idx] = {}
            table['ACTION'][idx] = {}
            for n in n_terminal_list:
                table['GO'][idx][n] = []
            for t in terminal_list:
                if not isinstance(t, empty_terminal):
                    table['ACTION'][idx][t] = []
        # 填充移进
        for (key, value) in status_trans.items():
            for targets in value:
                if isinstance(targets[0], n_terminal):
                    table['GO'][key][targets[0]].append(('s', targets[1]))
                elif isinstance(targets[0], terminal):
                    table['ACTION'][key][targets[0]].append(('s', targets[1]))
        # 填充归约
        for (key, value) in closure_dict.items():
            for i in value.items:
                if i.reduce:
                    for follows in i.lookahead:
                        table['ACTION'][key][follows].append(('r', self.CFG.rule_number[i.to_rule()]))

        self.closures_LR1 = closure_dict
        self.trans_LR1 = status_trans
        self.table_LR1 = ParsingTable(table, terminal_list, n_terminal_list)

    def __construct_table_LALR(self, closure_pool, status_trans: {}):
        closure_pool, status_trans = self.__merge_closures(closure_pool, status_trans)
        closure_count = len(closure_pool)
        closure_dict = {}
        for k in closure_pool:
            closure_dict[k.number] = k
        table = {'ACTION': {}, 'GO': {}}
        terminal_list = list(self.CFG.terminals) + [end_terminal('$')]
        if empty_terminal('empty') in terminal_list:
            terminal_list.remove(empty_terminal('empty'))
        n_terminal_list = list(self.CFG.n_terminals)
        # 初始化
        for idx in range(0, closure_count + 1):
            table['GO'][idx] = {}
            table['ACTION'][idx] = {}
            for n in n_terminal_list:
                table['GO'][idx][n] = []
            for t in terminal_list:
                if not isinstance(t, empty_terminal):
                    table['ACTION'][idx][t] = []
        # 填充移进
        for (key, value) in status_trans.items():
            for targets in value:
                if isinstance(targets[0], n_terminal):
                    table['GO'][key][targets[0]].append(('s', targets[1]))
                elif isinstance(targets[0], terminal):
                    table['ACTION'][key][targets[0]].append(('s', targets[1]))
        # 填充归约
        for (key, value) in closure_dict.items():
            for i in value.items:
                if i.reduce:
                    for follows in i.lookahead:
                        table['ACTION'][key][follows].append(('r', self.CFG.rule_number[i.to_rule()]))

        self.closures_LALR = closure_dict
        self.trans_LALR = status_trans
        self.table_LALR = ParsingTable(table, terminal_list, n_terminal_list)

    def __string(self, name, closures, trans, table):
        string = name + '\n'
        for (key, value) in closures.items():
            string += str(value) + '\n'
        string += '\n'
        for (key, value) in trans.items():
            string += str(key) + ' - ' + str(value) + '\n'
        string += '\n' + str(table) + '\n\n'
        return string

    def __repr__(self):
        # return self.__string('LR0', self.closures_LR0, self.trans_LR0, self.table_LR0) \
        #          + self.__string('SLR', self.closures_SLR, self.trans_SLR, self.table_SLR) \
        #          + self.__string('LR1', self.closures_LR1, self.trans_LR1, self.table_LR1) \
        #          + self.__string('LALR', self.closures_LALR, self.trans_LALR, self.table_LALR)
        return self.__string('LR1', self.closures_LR1, self.trans_LR1, self.table_LR1)

    def __eq__(self, other):
        return self.CFG == other.CFG

    def __hash__(self):
        return hash(self.CFG)

    def __str__(self):
        return self.__repr__()


class Parser:
    def __init__(self, lang: cfg):
        self.CFG = lang

    def parse(self, text: str):
        pass

    # 按空格将字符串打成列表，然后再CFG的表中查询，把字符串替换成symbol对象。最后在结尾加一个end_terminal对象
    def _get_symbolSequence(self, s: str):
        if len(s) == 0:
            return None
        elif s[-1] == '\n':
            s = s[:-1]
        symseq = []
        for c in s.split(' '):
            symseq.append(self.CFG.namelist[c])
        symseq.append(end_terminal('$'))
        return symseq


class LR_Parser(Parser):
    def __init__(self, lang: cfg):
        super().__init__(lang)
        self.PDA = Automata(lang)

    # ACTION表与GOTO表的使用过程：
    #   +初始时刻，符号栈中元素为$，状态栈中为0
    #   每次取状态栈顶的状态，与待输入符号中的第一个
    def parse(self, text: str):
        # TODO 改成清晰的用栈结构实现的。为语义分析打下基础
        # TODO 栈结构清晰之后，才能实现恐慌模式错误恢复
        # 获得待处理的字符序列
        symseq = self._get_symbolSequence(text)
        reduce_record = list(map(lambda x: {x: None}, symseq))
        symseq.reverse()

        self.parse2(symseq.copy())

        # 让栈提前于symbol而变化
        symbol_stack = []
        status_stack = [0]
        current_symbol = symseq.pop()

        index = 0
        unfinished = True
        while unfinished:
            # 当前的栈底状态
            current_status = status_stack[-1]
            if isinstance(current_symbol, n_terminal):
                # operation = self.PDA.table['GO'][current_status][current_symbol]
                operation = self.PDA.table.get_goto(current_status, current_symbol.s)
                if len(operation) == 0:
                    raise Exception
                symbol_stack.append(current_symbol)
                status_stack.append(operation[0][1])
                current_symbol = symseq.pop()
            elif isinstance(current_symbol, terminal):
                # operation = self.PDA.table['ACTION'][current_status][current_symbol]
                operation = self.PDA.table.get_action(current_status, current_symbol.s)
                if len(operation) == 0:
                    raise Exception('转换表读取异常')
                # 归约
                if operation[0][0] == 'r':
                    number = operation[0][1]
                    if number == 0:
                        print('unfinished')
                        # reduce_record.remove(end_terminal('$'))
                        self.tree = reduce_record[0]
                        return
                    r = self.PDA.CFG.rule_by_number(number)
                    l = len(r.right)
                    if r.right[0].s == 'empty':
                        l = 0
                    # 把符号放回去
                    before_reduce = len(symbol_stack)
                    symseq.append(current_symbol)
                    current_symbol = r.left
                    for i in range(l):
                        status_stack.pop()
                        symbol_stack.pop()
                    after_reduce = len(symbol_stack)
                    # 归约的过程消除了一些符号
                    if after_reduce < before_reduce:
                        left_symbol = current_symbol
                        node = {left_symbol:reduce_record[after_reduce: before_reduce]}
                        reduce_record = reduce_record[:after_reduce] + [node] + reduce_record[before_reduce:]
                    # 归约过程没有消除符号，即生成串的产生式的归约
                    elif after_reduce == before_reduce:
                        left_symbol = current_symbol
                        reduce_record = reduce_record[:before_reduce] + [{left_symbol:empty_terminal('empty')}]\
                                        + reduce_record[before_reduce:]
                    else:
                        raise Exception('符号栈长度异常')
                # 移进
                elif operation[0][0] == 's':
                    symbol_stack.append(current_symbol)
                    status_stack.append(operation[0][1])
                    current_symbol = symseq.pop()

        raise Exception

    # 对sequence进行处理
    # seq:以$结尾的符号序列，反序
    def parse2(self, lex_seq: []):

        # 初始化的两个数据结构
        symbol_stack = [end_terminal('$')]
        status_stack = [0]

        unfinished = True
        while unfinished:
            # 获得栈顶状态与输入符号
            current_status = status_stack[-1]
            current_symbol = lex_seq.pop()

            # 获取操作
            operation = self.PDA.table.get_action(current_status, current_symbol.s)
            if len(operation) == 0:
                raise Exception('LR分析表遇到未知状态')

            # 需要移进
            if operation[0][0] == 's':
                next_status = operation[0][1]
                symbol_stack.append(current_symbol)
                status_stack.append(next_status)
            elif operation[0][0] == 'r':
                # 完成parsing
                if operation[0][1] == 0 and isinstance(current_symbol, end_terminal):
                    # TODO
                    print('finished parse 2')
                    return
                # 需要归约
                else:
                    # 获取需要归约的产生式
                    reduce_rule_number = int(operation[0][1])
                    current_rule = self.PDA.CFG.rule_by_number(reduce_rule_number)
                    rule_length = len(current_rule.right)
                    # TODO 忽略空字符的扩展在这里添加
                    if current_rule.right[0].s == 'empty':
                        rule_length = 0

                    for idx in range(rule_length):
                        status_stack.pop()
                        symbol_stack.pop()
                    assert len(status_stack) > 0
                    temp_status = status_stack[-1]
                    next_status = self.PDA.table.get_goto(temp_status, current_rule.left.s)
                    status_stack.append(next_status[0][1])
                    symbol_stack.append(current_rule.left)
                    lex_seq.append(current_symbol)

        raise Exception('你怎么到这里来了')

    # 接收token序列的parse
    def parse3(self, token_seq: []):
        lex_seq = list(map(lambda x: terminal(x[0]), token_seq))
        # reduce_record是用于构建树结构的表
        reduce_record = list(map(lambda x: {x: None}, token_seq))
        lex_seq.reverse()
        lex_seq.insert(0, end_terminal('$'))
        # 初始化的两个数据结构
        symbol_stack = [end_terminal('$')]
        status_stack = [0]

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
            elif operation[0][0] == 'r':
                # 完成parsing
                if operation[0][1] == 0 and isinstance(current_symbol, end_terminal):
                    # TODO
                    print('finished parse 2')
                    self.tree = reduce_record[0]
                    self.error = errorList
                    print(errorList)
                    return
                # 需要归约
                else:
                    # 获取需要归约的产生式
                    reduce_rule_number = int(operation[0][1])
                    current_rule = self.PDA.CFG.rule_by_number(reduce_rule_number)
                    rule_length = len(current_rule.right)
                    # TODO 忽略空字符的扩展在这里添加
                    if current_rule.right[0].s == 'empty':
                        rule_length = 0

                    for idx in range(rule_length):
                        status_stack.pop()
                        symbol_stack.pop()
                    assert len(status_stack) > 0
                    temp_status = status_stack[-1]
                    next_status = self.PDA.table.get_goto(temp_status, current_rule.left.s)
                    status_stack.append(next_status[0][1])
                    symbol_stack.append(current_rule.left)
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

    def visualize_tree(self):
        dot = Digraph(comment='parsing tree')

        # 父根节点
        father = self.tree
        # 初始层数为第0层
        level = 0
        # 第几个符号
        count = 0
        dot.node('R\'', 'R\'')
        self.__treenode(dot, 'R\'', father, 0)
        dot.view()
        # dot.render('test-output/test-table.gv', view=True)

    def __treenode(self, dot, fname, father, number):

        if not isinstance(father, dict):
            return
        count = 0
        for (key, value) in father.items():
            name = fname + '_' + str(number)
            dot.node(name, str(key))
            print(name)
            dot.edge(fname, name)
            if not isinstance(value, list):
                continue
            for nodes in value:
                count += 1
                self.__treenode(dot, name, nodes, count)

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

# 默认输入的语言是LL(k)的
class LL_Parser(Parser):
    def __init__(self, lang: cfg):
        super().__init__(lang)
        self.__generate_table()

    # 生成LL(1)文法的预测分析表
    def __generate_table(self):
        self.table = {}
        term = [self.CFG.terminals] + [end_terminal('$')]
        if empty_terminal('empty') in term:
            term.remove(empty_terminal('empty'))

        # 初始化
        for nt in self.CFG.n_terminals:
            self.table[nt] = {}
            for t in term:
                self.table[nt][t] = None

        # 填充产生式
        for it in self.CFG.rules:
            l = it.left
            for symb in self.CFG.SELECT[it]:
                self.table[l][symb] = it

    def parse(self, text: str):
        # 有两个栈，一个是输入符号栈，另一个是文法符号栈
        symbol_stack = self._get_symbolSequence(text)
        reduce_statck = [end_terminal('$'), self.CFG.start]

        r = reduce_statck[-1]
        pointer = symbol_stack[-1]
        while not isinstance(r, end_terminal):
            if r == pointer:
                symbol_stack.pop()
                pointer = symbol_stack[-1]
                reduce_statck.pop()
            elif isinstance(r, terminal):
                raise Exception('产生式与符号串匹配错误')
            elif not self.table[r][pointer]:
                raise Exception('预测分析表中遇到报错条目')
            else:
                reduce_statck.pop()
                match_rule = self.table[r][pointer]
                reversed_right = match_rule.right
                reversed_right.reverse()
                print(match_rule)
                reduce_statck += reversed_right
            r = reduce_statck[-1]

# TODO 带有操作的符号继承空串，可以直接复用现有的句法分析代码，实现SDT


# 从文件读取
def cfg_readfile(filename: str):
    f = open(filename, 'r', encoding='utf-8')
    lines = f.readlines()
    f.close()

    terminals = []
    n_terminals = []
    rules = []
    nameDict = {}

    firstLine = lines[0][:-1].split(' ')
    secondLine = lines[1][:-1].split(' ')
    start = n_terminal(firstLine[0])
    n_terminals.append(start)
    nameDict[start.s] = start

    for name in firstLine[1:]:
        sym = n_terminal(name)
        nameDict[name] = sym
        n_terminals.append(sym)

    for name in secondLine:
        sym = terminal(name)
        if name == 'empty':
            sym = empty_terminal(name)
        nameDict[name] = sym
        terminals.append(sym)

    rule_line = lines[2:]
    for line in rule_line:
        # 注释语句
        if line[0] == '#':
            continue
        if len(line) <= 1:
            continue
        if line[-1] == '\n':
            line = line[:-1]
        syms = line.split(' ')
        l = nameDict[syms[0]]
        print(line)
        rs = list(map(lambda x: nameDict[x], syms[2:]))
        rules.append(rule(l, rs))

    return cfg(start, n_terminals, terminals, rules)



if __name__ == '__main__':
    pass
    # CFG的数据结构（从简）
    # 0 - terminal
    # 1 - non-terminal
    # start, n_terminals, terminals, rules = raw_read_CFG('testCases/first/cfg1.txt')
    # FIRST = first(start, n_terminals, terminals, rules)
    # FOLLOW = follow(start, n_terminals, terminals, rules, FIRST)
    # SELECT = select(start, n_terminals, terminals, rules, FIRST, FOLLOW)
    # print(SELECT)
    c = cfg_readfile('syntax/cfg_syl.txt')
    # TODO 有bug，cfg_regex跑出来不是LALR的，却可以是SLR的。肯定哪里出错了
    # print(c.FIRST)
    # print(c.FOLLOW)
    # print(c.SELECT)
    pda = Automata(c)
    # f = open('syl_grammer_pda.txt', 'w', encoding='utf-8')
    # f.write(str(pda))
    # f.close()
    # f = open('syl_grammer_cfg.txt', 'w', encoding='utf-8')
    # f.write(str(c))
    # f.close()
    # print(pda)
    parse = LR_Parser(c)
    parse.parse('int [ CONST ] [ CONST ID ;')

