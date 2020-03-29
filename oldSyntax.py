

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

