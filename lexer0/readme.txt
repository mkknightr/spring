程序内容介绍：
1. CLexer.g4 
它是根据antlr词法定义规范编写的词法规则文件

2. CLexer.interp CLexer.tokens CLexer.py
他们是antlr4生成的词法分析器文件 

3. test/
test目录下是C语言代码文件，包括冒泡排序和回文检测

4. lexerDrive.py 
此文件是测试运行的脚本文件，它会调用antlr4生成的词法分析器工具，
对test目录下的C语言源代码文件进行词法分析，然后将词法分析得到的结果
打印出来 

可以直接在命令行中运行lexerDrive.py: 
python lexerDrive.py 

默认分析./test/bubbleSort.c 文件， 可以在命令行中指定参数: 
python lexerDrive.py ./test/palindrom.c  // 分析回文检测文件

