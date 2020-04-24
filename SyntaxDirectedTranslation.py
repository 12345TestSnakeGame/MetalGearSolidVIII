from LexicalAnalysis import *
from SDT_definitions import *


# 进行语法制导翻译的翻译器
# lang读取带有语法动作的文法定义，将语法动作视为空字符，然后生成自动机
# SDT_Parser与普通Parser不同的是，它的分析栈除了状态栈和符号栈之外，还有一个属性栈
# 一边根据ACTION和GOTO表进行语法分析，一边执行语法动作
class SDT_Parser(Parser):
    def __init__(self, lang: cfg):
        Parser.__init__(self, lang)
        pass


# 用于生成中间代码的类
# SDT将符号定义，语法动作等数据传给CodePlatform,然后由CodePlatform维护与生成中间代码
class CodePlatform:
    def __init__(self):
        pass


if __name__ == '__main__':
    c = cfg_readfile('SDD/ControlFlow.txt')
    pda = Automata(c)
    print(pda)
