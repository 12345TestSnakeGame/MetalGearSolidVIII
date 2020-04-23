## 目录结构

- DFA_pic 存放词法分析器通过词法得到的DFA的可视化图
- FA 词法分析器得到的FA自动机
- Lex_source 词法分析的测试用例
- regex 为词法分析阶段编写的一些词法
- report 存放实验报告
- Syn_source 句法分析的测试用例
- syntax 为句法分析编写的句法
  - cfg_syl.txt 孙云龙写的句法，消除了LR(1)中的冲突，写成了我们的代码能够读取的格式
  - grammar5.txt 孙云龙的句法，用的是他自己的格式
  - java_mine.txt 我们自己的类java句法，有bug，算是一个初步设计
  - java_mine_reCustomed.txt 对java_mine的改进，用于展示的句法。对Syn-source中的测试用例已经没什么问题，展示阶段也ok，但仍可能存在bug。
- testCases 通用的一些测试用例，用到比较少
  - first 包含老师的习题中的许多文法，用于测试FIRST集
- ui 实现ui的部分代码
- cfg_regex.txt 正则表达式的词法。LexicalAnalysis.py必须要与该文件在同一目录下才能运行
- LexicalAnalysis.py 词法分析部分的代码
- SyntaxAnalysis.py 句法分析部分的代码
- SyntaxDirectedTranslation.py 语义分析部分的代码
- oldSyntax.py 最早的实现，实现了句法分析中的求Select集等几个基本功能，已经不再使用。

## 项目构成

### SyntaxAnalysis.py

这一部分是最初始的代码，Lexical的一部分代码需要用到这里的内容

symbol代表一个符号，n_terminal与terminal分别继承自symbol，前者代表非终结符，后者代表终结符。empty_terminal与end_terminal分别是空字符与句尾字符，专门把这两个写出来可以方便处理。

rule是文法规则，由左部和右部构成

item则是一个匹配中的rule，position代表当前所匹配到的位置

item_lookahead就是加上了展望符的item

closure是由多个item组成的闭包，类里面包含了一个能够合并几个闭包的函数。

cfg类。一个cfg实例可以读取一个符合一定格式的句法规则文件，然后自动生成SELECT，FOLLOW和FIRST集合

ParsingTable语法分析表类

Automata，读取一个cfg，然后生成自动机。然后根据自动机产生

## 3-19. 初步构思阶段

打算实验一和实验二一起写了，顺便打好实验三的地基

打算扩充一点，不用手动输入DFA,NFA转换表，我做成根据正则表达式直接生成NFA/DFA，这样以后很容易扩充。打算从C的文法开始，不过SQL的文法似乎也可以一起做出来。

打算先写核心的内容，这样GUI什么的换个模子就可以了。

先写的是从文件读取正则表达式，转换为NFA表。读取和输出的格式还待考虑，不过我打算先写成文本输入与输出，因为可能要用java来写GUI。然后句法分析的CFG文法也从文件读取，然后生成转换表，顺便加入判断LR，SLR，LR(1)之类的功能。

然后发现一个很有趣的事情：

> 正则表达式是CFG的，CFG表达式是正则的

这也意味着我想实现从正则表达式生成NFA，还得实现一个CFG句法分析器。实验一和实验二一起写真是选对了

## 3-23. 完成了CFG文法的识别与自动机的生成部分

写到一半的时候突然发现用面对对象来写要方便很多，于是就现学了python的面向对象的方法。

没有重载有点不太方便，不过python的语法糖实在是很好用

正则文法的CFG公式研究了一会儿，后来发现我走进了一个误区：

我发现把 $\epsilon$ 加入到公式里的时候，得到的转换表总是有重复项。花了一天我才意识到，这个 $\epsilon$ 实际上就是正则表达式里面的一个符号，一个entity，而不是cfg中的空串！

搞清楚这个之后，正则表达式就比较好写了。

```regex
R',R,C,B,A
(,),empty,entity,|,*
R' - R
R - B | R
R - B
B - A B
B - A
A - ( C )
A - A *
A - entity
C - R
```

## 3-24 拉了一个team，

这个仓库用team代替origin，别传错了
