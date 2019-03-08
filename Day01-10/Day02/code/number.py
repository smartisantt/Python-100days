"""

输入一个三位整数，从低位到高位反向输出
例如：输入123， 打印321

Version: 0.1
Author: 陈伦巨
Date: 2019-03-07

"""

num = int(input("请输入一个3位整数："))
hundred = num//100
decade = num%100//10
unit = num%10
new_num = unit*100 + decade*10 + hundred
print("The new number is %d" % new_num)
