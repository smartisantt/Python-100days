"""

输入一个小写字母转换成大写字母；
反之，输入一个大写字母转换成小写的
Version: 0.1
Author: 陈伦巨
Date: 2019-03-13

"""

letter = input("请输入一个字母：")
print(chr(ord(letter)^32))

"""
备注：
ord()函数主要用来返回对应字符的ascii码，
chr()主要用来表示ascii码对应的字符他的输入时数字，
可以用十进制，也可以用十六进制。
字符'a'-'z'与'A'-'Z'所对应的大小写ASCII相差32位，
通过位运算异或即可实现转换。


"""