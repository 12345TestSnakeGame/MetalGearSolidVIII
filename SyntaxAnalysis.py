from graphviz import Digraph

# 面对过程的first集函数
def first(first, n_terminals, terminals, rules):
    FIRST = {}
    for nt in n_terminals:
        FIRST[nt] = set()
    for t in terminals:
        FIRST[t] = set([t])

    empty_set = set()

    change = True
    while change:
        change = False
        for v in n_terminals:
            # 非终结符v的新first集合
            newv = set()
            # iv - v的一个产生式
            for iv in rules[(1, v)]:
                count = 0
                # 看产生式的第一个符号
                iiv = iv[count][1]
                for iiiv in FIRST[iiv]:
                    newv.add(iiiv)
                    if iiiv == 'empty':
                        empty_set.add(iiv)
                # 对于可能为空的符号，可以跳过
                while iiv in empty_set:
                    count += 1
                    if count == len(iv):
                        break
                    iiv = iv[count][1]
                    for iiiv in FIRST[iiv]:
                        newv.add(iiiv)
                        if iiiv == 'empty':
                            empty_set.add(iiv)
            # 检查是否有更新
            if len(FIRST[v]) < len(newv):
                change = True
                FIRST[v] = newv
    return FIRST


# 面对过程的follow集函数
def follow(start, n_terminals, terminals, rules, FIRST):
    FOLLOW = {}
    for nt in n_terminals:
        FOLLOW[nt] = set()

    # 一切的开始，开始符的FOLLOW集中添加一个end
    FOLLOW[start].add('$')

    change = True
    while change:
        change = False
        # 对每一个生成式
        for v in n_terminals:
            for iv in rules[(1, v)]:
                # 从尾部开始向前搜索
                if iv[-1][0] == 1:
                    next = v
                    cur = iv[-1][1]
                    for father_follow in FOLLOW[next]:
                        if father_follow not in FOLLOW[cur]:
                            change = True
                            FOLLOW[cur].add(father_follow)
                            # print('parsing ' + str(v) + '-' + str(iv))
                            # print('add ' + str(father_follow) + ' to ' + str(cur) + ' as 1')
                # 如果只有一个符号，到这里就结束了
                if len(iv) <= 1:
                    continue
                # 对剩下的符号依次处理
                for i in range(len(iv) - 2, -1, -1):

                    # 只需要计算非终结符
                    if iv[i][0] == 0:
                        continue
                    # 待处理的左符号
                    cur = iv[i][1]
                    no_empty = False
                    # 对于左符号右侧的串求FIRST
                    for k in range(i + 1, len(iv) + 1):
                        # 当上个符号不为空时，不需要继续计算下一个符号
                        if no_empty:
                            break
                        no_empty = True
                        # 如果循环到串尾
                        if k == len(iv):
                            next = v
                            for father_follow in FOLLOW[next]:
                                if father_follow not in FOLLOW[cur]:
                                    change = True
                                    FOLLOW[cur].add(father_follow)
                                    # print('parsing ' + str(v) + '-' + str(iv))
                                    # print('add ' + str(father_follow) + ' to ' + str(cur) + ' as 1')
                            break
                        next = iv[k][1]
                        for next_first in FIRST[next]:
                            # 可为空
                            if next_first == 'empty':
                                no_empty = False
                                continue
                            if next_first not in FOLLOW[cur]:
                                change = True
                                FOLLOW[cur].add(next_first)
                                # print('parsing ' + str(v) + '-' + str(iv))
                                # print('add ' + str(next_first) + ' to ' + str(cur) + ' as 2')

    return FOLLOW


# 面对过程的select集函数
def select(start, n_terminals, terminals, rules, FIRST, FOLLOW):
    # 使用二层dict存储SELECT集
    SELECT = {}
    for left in n_terminals:
        SELECT[(1, left)] = {}
        for right in rules[(1, left)]:
            tupled_right = tuple(right)
            SELECT[(1, left)][tupled_right] = set()

            # 对产生式右部进行分析
            no_empty = False
            for i in range(0, len(right) + 1):
                if no_empty:
                    break
                no_empty = True
                if i == len(right):
                    for v in FOLLOW[left]:
                        SELECT[(1, left)][tupled_right].add(v)
                    break
                cur = right[i][1]
                for v in FIRST[cur]:
                    if v == 'empty':
                        no_empty = False
                        continue
                    SELECT[(1, left)][tupled_right].add(v)

    return SELECT


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

    def __repr__(self):
        return self.left.s + ' -> ' + ' '.join(list(map(lambda x: str(x), self.right)))

    def __eq__(self, other):
        return other.left == self.left and other.right == self.right

    def __hash__(self):
        return hash(self.left) + sum(list(map(lambda x: hash(x), self.right)))


class item(rule):
    def __init__(self, position: int, left: n_terminal, rights: [symbol, ]):
        if len(rights) == 0:
            raise Exception
        if isinstance(rights[0], empty_terminal):
            self.empty = True
        else:
            self.empty = False
        if position == len(rights) or (len(rights) == 1 and rights[0].s == 'empty'):
            self.reduce = True
        else:
            self.reduce = False
        rule.__init__(self, left, rights)
        self.position = position
        self.__operation_cache = {}
        self.origin = (self.left, tuple(self.right), self.position)

    def __repr__(self):
        l_part = ' '.join(list(map(lambda x: str(x), self.right[0:self.position])))
        r_part = ' '.join(list(map(lambda x: str(x), self.right[self.position:])))
        return self.left.s + ' -> ' + l_part + ' · ' + r_part

    def __eq__(self, other):
        return other.left == self.left and other.right == self.right and self.position == other.position

    def __hash__(self):
        count = 0
        for v in self.right:
            count += hash(v)
        count *= (hash(self.left) + 1)
        count *= (self.position + 1)
        return count

    # 转换为产生式
    def to_rule(self):
        return rule(self.left, self.right)

    def merge(self, other):
        if not self.origin == other.origin:
            return None
        return self

    def successive_symbol(self):
        if len(self.right) == self.position:
            return None
        return self.right[self.position]

    def successive_item(self):
        if self.empty:
            return None
        if len(self.right) == self.position:
            return None
        return item(self.position + 1, self.left, self.right)

    # 对于一个输入符号，输出该产生式对该符号的操作 接受/不接受
    def get_operation(self, input: symbol):

        pass

    # 合法的规约符号
    # 当当前项目不是规约项目时，未定义行为
    def legal_reduce(self, input: symbol):
        # 普通item无任何限制
        return True


class item_lookahead(item):
    def __init__(self, position: int, left: n_terminal, rights: [symbol, ], lookahead: set):
        item.__init__(self, position, left, rights)
        self.lookahead = lookahead
        self.CFG_imported = False
        self.CFG = None

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
        return ss + ', ' + ''.join(list(map(str, list(self.lookahead))))

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
        if not self.origin == other.origin:
            return None

        return item_lookahead(self.position, self.left, self.right, self.lookahead.union(other.lookahead))

    def successive_item(self):
        if self.empty:
            return None
        if len(self.right) == self.position:
            return None
        return item_lookahead(self.position + 1, self.left, self.right, self.lookahead)

    def get_operation(self, input: symbol):
        pass

    def legal_reduce(self, input: symbol):

        return False


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
        self.FOLLOW ={}
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
            for c in self.FIRST[w[idx]]:
                if c.s == 'empty':
                    no_empty = False
                    continue
                s.add(c)
        return s

    # 计算每个符号的select集
    def __select(self):
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
                    if v.s == 'empty':
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
                            if not isinstance(temp, empty_terminal):
                                self.FOLLOW[cur.right[idx]].add(temp)
                                change = True
                    # 对于非最后一个符号是非终结符的情况，在其follow集中添加first（其后的子串）
                    elif idx < len(cur.right) - 1 and type(cur.right[idx]) == n_terminal:
                        # 对其后的子串进行遍历
                        no_empty = False
                        for k in range(idx + 1, len(cur.right) + 1):
                            if no_empty:
                                break
                            no_empty = True
                            # 当遍历到最后一符号，说明前面的所有符号都可以为空
                            if k == len(cur.right):
                                for temp in self.FOLLOW[cur.left]:
                                    if temp.s != 'empty' and temp not in self.FOLLOW[cur.right[idx]]:
                                        self.FOLLOW[cur.right[idx]].add(temp)
                                        change = True
                                break
                            for temp in self.FIRST[cur.right[k]]:
                                if temp.s == 'empty':
                                    no_empty = False
                                    continue
                                if temp not in self.FOLLOW[cur.right[idx]]:
                                    self.FOLLOW[cur.right[idx]].add(temp)
                                    change = True

    # 计算每个符号的first集
    def __first(self):
        # 首先，所有的终结符的first是自己本身
        for t in self.terminals:
            self.FIRST[t] = {[t]}
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
                        new_first_symbol.add(cur_first)
                        if cur_first.s == 'empty':
                            no_empty = False
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


class closure:
    def __init__(self, number: int, items: [item, ]):
        self.number = number
        self.items = items

    def __eq__(self, other):
        # return self.number == other.number and self.items == other.items
        return self.items == other.items

    def __repr__(self):
        return 'I' + str(self.number) + '\n' + '\n'.join(list(map(lambda x: str(x), self.items)))

    def __hash__(self):
        count = 0
        for i in self.items:
            count += i.__hash__()
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


class automata:
    def __init__(self, lang: cfg):
        self.CFG = lang
        self.to_dict = {}
        self.from_dict = {}
        self.closure_dict = {}
        self.__construct_automata()
        self.__construct_table()
        # TODO 造出一个完整的自动机的数据结构

    # 计算rules_对应的closure
    def cal_items(self, rules_: []):
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
                if r.origin not in rule_dict:
                    rule_dict[r.origin] = r
                else:
                    rule_dict[r.origin] = rule_dict[r.origin].merge(r)

            cur_rules = []
            for (key, value) in rule_dict.items():
                cur_rules.append(value)
            return cur_rules
        else:
            pass
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

    def GOTO(self, c: closure, sym: symbol):
        pass

    # 根据产生式计算自动机
    # 默认使用LR(1)
    def __construct_automata(self):
        # 对状态集的计数
        count = 0
        initial_rules = self.CFG.get_rule(self.CFG.start)
        # initial_items = list(map(lambda x: item(0, x.left, x.right), initial_rules))
        initial_items = list(map(lambda x: item_lookahead(0, x.left, x.right, {end_terminal('$')}), initial_rules))
        map(lambda x: x.import_CFG(self.CFG), initial_items)
        i_r_closure = closure(count, self.cal_items(initial_items))

        closure_pool = set()
        to_explore = [i_r_closure]
        exploring = []
        status_dict = {count: i_r_closure}
        reversed_status_dict = {i_r_closure:count}


        while len(to_explore) > 0:
            exploring = to_explore.copy()
            to_explore.clear()
            # 对每一个状态（按广度优先搜索顺序）
            for status in exploring:
                # 对状态中的每一个产生式，找到其后继产生式与对应的输入符号 （同样按顺序）
                last = status.number
                s_rule = {}
                for r in status.items:
                    s_item = r.successive_item()
                    s_symbol = r.successive_symbol()
                    if not s_item:
                        continue
                    if s_symbol in s_rule:
                        s_rule[s_symbol].append(s_item)
                    else:
                        s_rule[s_symbol] = [s_item]

                for (key, value) in s_rule.items():
                    temp_closure = closure(count + 1, self.cal_items(value))
                    # 如果是已经建立过的状态
                    if temp_closure in closure_pool or temp_closure in exploring or temp_closure in to_explore:
                        temp_number = reversed_status_dict[temp_closure]
                        if last in self.to_dict:
                            self.to_dict[last].append((key, temp_number))
                        else:
                            self.to_dict[last] = [(key, temp_number)]
                        continue
                    count = count + 1
                    to_explore.append(temp_closure)
                    if last in self.to_dict:
                        self.to_dict[last].append((key, count))
                    else:
                        self.to_dict[last] = [(key, count)]
                    status_dict[count] = temp_closure
                    reversed_status_dict[temp_closure] = count
            for v in exploring:
                closure_pool.add(v)
        self.closures = closure_pool

        self.closure_count = 0
        for c in closure_pool:
            self.closure_count += 1
            self.closure_dict[c.number] = c

    # 根据自动机生成分析表
    # 默认根据LR(1)生成
    def __construct_table(self):
        # *** item_lookahead only ***
        self.table = {'ACTION':{}, 'GO':{}}
        # 初始化
        for idx in range(0, self.closure_count + 1):
            self.table['GO'][idx] = {}
            self.table['ACTION'][idx] = {}
            for n in self.CFG.n_terminals:
                self.table['GO'][idx][n] = []
            for t in self.CFG.terminals + [end_terminal('$')]:
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


    def __repr__(self):
        c = list(self.closures)
        c.sort()
        tablestr = ''
        tablestr += '\nACTION\n\t'
        for n in self.CFG.terminals + [end_terminal('$')]:
            if isinstance(n, empty_terminal):
                continue
            tablestr += str(n) + '\t'
        tablestr += '\n'
        # 每一行
        for i in range(self.closure_count + 1):
            tablestr += '\n' + str(i) + '\t'
            for (key1, value1) in self.table['ACTION'][i].items():
                if len(value1) == 0:
                    tablestr += '[]\t'
                    continue
                # for k in value1:
                #     tablestr += k[0] + str(k[1]) + '\t'
                tablestr += ','.join(list(map(lambda x: x[0] + str(x[1]), value1)))
                tablestr += '\t'
        tablestr += '\nGO\n'
        for t in self.CFG.n_terminals:
            tablestr += str(t) + '\t'
        tablestr += '\n'
        # 每一行
        for i in range(self.closure_count):
            tablestr += '\n' + str(i) + '\t'
            for (key1, value1) in self.table['GO'][i].items():
                if len(value1) == 0:
                    tablestr += '[]\t'
                    continue
                for k in value1:
                    tablestr += k[0] + str(k[1]) + '\t'
                tablestr += '\t'
        return str(self.to_dict) + '\n' + '\n'.join(list(map(str, c))) + '\n' + tablestr

    def __eq__(self, other):
        return self.CFG == other.CFG

    def __hash__(self):
        return hash(self.CFG)


class LR_analyzer:
    def __init__(self, pda:automata):
        self.PDA = pda

    def analyze_str(self, input: str):
        symseq = self.__get_symbolSequence(input)
        reduce_record = list(map(lambda x:{x:None}, symseq))
        symseq.reverse()

        # 让栈提前于symbol而变化
        symbol_stack = []
        status_stack = [0]
        current_symbol = symseq.pop()

        index = 0
        finished = True
        while finished:
            # 当前的栈底状态
            current_status = status_stack[-1]
            if isinstance(current_symbol, n_terminal):
                operation = self.PDA.table['GO'][current_status][current_symbol]
                if len(operation) == 0:
                    raise Exception
                symbol_stack.append(current_symbol)
                status_stack.append(operation[0][1])
                current_symbol = symseq.pop()
            elif isinstance(current_symbol, terminal):
                operation = self.PDA.table['ACTION'][current_status][current_symbol]
                if len(operation) == 0:
                    raise Exception('转换表读取异常')
                # 归约
                if operation[0][0] == 'r':
                    number = operation[0][1]
                    if number == 0:
                        print('finished')
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


    def __get_symbolSequence(self, s: str):
        if len(s) == 0:
            return None
        elif s[-1] == '\n':
            s = s[:-1]
        symseq = []
        for c in s.split(' '):
            symseq.append(self.PDA.CFG.namelist[c])
        # symseq.insert(0, end_terminal('$'))
        symseq.append(end_terminal('$'))
        return symseq

    def visulize_tree(self):
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


# 从文件读取
def cfg_readfile(filename: str):
    f = open(filename, 'r', encoding='utf-8')
    lines = f.readlines()
    f.close()

    terminals = []
    n_terminals = []
    rules = []
    nameDict = {}

    firstLine = lines[0][:-1].split(',')
    secondLine = lines[1][:-1].split(',')
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
        rs = list(map(lambda x: nameDict[x], syms[2:]))
        rules.append(rule(l, rs))

    return cfg(start, n_terminals, terminals, rules)


def raw_read_CFG(filename: str):
    f = open(filename, 'r', encoding='utf-8')
    lines = f.readlines()

    # 非终结符
    firstLine = lines[0][:-1].split(',')
    start = firstLine[0]
    n_terminals = set(firstLine)
    terminals = set()
    rules = {}
    for n_terminal in n_terminals:
        rules[(1, n_terminal)] = []

    # 产生式
    chanshengshis = lines[1:]
    for rule in chanshengshis:
        if len(rule) == 0:
            continue
        if rule[-1] == '\n':
            rule = rule[:-1]
        line = rule.split(' ')
        left = line[0]
        right = line[2:]
        rules[(1, left)].append([])
        for symbol in right:
            if symbol in n_terminals:
                rules[(1, left)][-1].append((1, symbol))
            else:
                rules[(1, left)][-1].append((0, symbol))
                terminals.add(symbol)

    return start, n_terminals, terminals, rules


if __name__ == '__main__':
    # CFG的数据结构（从简）
    # 0 - terminal
    # 1 - non-terminal
    # start, n_terminals, terminals, rules = raw_read_CFG('testCases/first/cfg1.txt')
    # FIRST = first(start, n_terminals, terminals, rules)
    # FOLLOW = follow(start, n_terminals, terminals, rules, FIRST)
    # SELECT = select(start, n_terminals, terminals, rules, FIRST, FOLLOW)
    # print(SELECT)
    c = cfg_readfile('testCases/first/cfg_q7.8.txt')
    # print(c.FIRST)
    # print(c.FOLLOW)
    # print(c.SELECT)
    pda = automata(c)
    print(pda)
    # parse = LR_analyzer(pda)
    # parse.analyze_str('( entity ( entity | entity | entity ) entity entity * ) | entity')
    # parse.visulize_tree()
    pass