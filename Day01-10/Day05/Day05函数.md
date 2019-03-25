> Author: 陈伦巨
>
> Data: 2019-03-25
>
> Email: 545560793@qq.com
>
> github: https://github.com/smartisantt

## 一、函数

##### 1、什么是函数

函数就是对实现某一特定功能的代码段的封装。

##### 2、函数的分类

- 系统函数：系统已经给我们定义好的函数，程序员直接调用函数使用函数的功能。
- 自定义函数：需要程序员自己去定义的函数。

##### 3、函数的定义

###### a、语法

```python
def 函数名(参数列表):
    函数体
```

###### b、说明

def - Python中声明函数的关键字

函数名 - 标识符，不能是关键字；PEP8命名规范，见名知意。

() - 固定格式

参数列表 - 参数1，参数2，参数3……；这里的参数叫形参。

​		 功能是将函数外面的数据传递到函数里面

: - 固定格式

函数体 - 实现功能的代码段。一个完整的函数体包含：函数说明文档、实现函数功能的代码段、函数的返回值。

###### c、初学着声明函数的步骤

1. 确定函数的功能
2. 根据功能给函数命名
3. 确定形参（看实现函数的功能需不需要外面传值近来）
4. 实现函数功能
5. 确定函数返回值



**注意：函数的在声明的时候不会执行函数体。只有在调用的时候才会执行。**

```python
def my_sum(num1, num2):
    """
    求两个数的和。
    :param num1:
    :param num2:
    :return:
    """
    print(num1 + num2)
```

##### 4、函数的调用

就是使用函数。

###### a、语法

函数名(实参列表)

###### b、说明

函数名 - 这个函数名对应的函数必须是已经声明过的函数

() - 固定写法

实参列表 - 实参是用来给新参赋值（用实参给形参赋值的过程就是传参）

​		   实参和新参要一一对应。

###### c、调用过程

1. 回到函数声明的位置
2. 用实参给形参赋值（传参）
3. 执行函数体
4. 执行完函数体就确定并返回返回值
5. 再回到函数调用位置，接着执行后面其他代码



练习：N的阶乘

```python
def factorial (num1):
    """
    打印N的阶乘
    :param num1:
    :return:
    """
    result = 1
    while num1:
        result *= num1
        num1 -= 1
    print(result)
```



## 二、参数

##### 1、位置参数和关键字参数

根据实参的传递方式对参数进行的分类

###### a、位置参数：

实参的位置和形参保持一致，按形参声明的先后顺序一一赋值。

###### b、关键字参数：

调用函数的时候以 形参=实参的方式来传参，这个时候实参的顺序无所谓



```python
def func1(a, b, c):
    print(a, b, c)
# 通过位置参数给新参赋值
func1(10, 20, 30)  

def func2(a, b, c):
    print(a, b, c)
# 通过关键字参数给新参赋值
func2(c = 10, a = 20, b =30)  
# 通过位置参数和关键字参数结合传参(注意关键字参数必须在位置参数的后面)
func2(10, 20, c =30)  
```

##### 2、参数默认值

声明函数的时候，可以给参数赋默认值。

如果一个形参有默认值了，那么调用函数的时候这个参数就可以不用传参。

有默认值的形参要放在没有默认值的后面。

调用函数要保证每个参数都有值！

```python
def fun2(a, b c=0):
	print(a, b, c)
fun2(1, 2, 3)
fun2(1, 2)
fun2(b = 2, a = 1)
```

##### 3、参数类型说明

类型说明只有提示功能，没有约束功能。

a、给参数设置默认值，默认值的类型就是参数的类型。

b在形参后面加:类型命，来说明参数类型。这个方式调用的时候必须传参。

c、函数声明的时候在() 后面加 ->类型名，来说明函数返回值的类型。

```python
def list_item(list1: list, index = 0):
    print(list1[index])
```

**类型说明的好处：**

1. 传参时候，对实参的类型进行说明。
2. 实现函数功能的时候有类型相关的语法提示

```python
def list_item(list1: list, index = 0) ->int:
    return list1[index]
```

##### 4、不定长参数

函数的参数不确定。

写一个函数，计算多个函数的和

方法一:声明函数的时候，在参数名前加*，可以用来同时获取多个实参的值。实质是将带\*的参数变成元祖，将多个实参的值作为元祖的元素。

注意：如果函数中既有不定长参数又有普通参数，那么不定长参数必须放在普通参数的后边。

```python
def my_sum(*nums):
    print(nums)
    print(type(nums))

my_sum(1, 2, 3, 4, 5, 6)
```

```python
def my_sum(*nums):
    print(sum(nums))
```

方法二：在参数名前加两个*

传参时需使用关键字传参，会将参数变成一个字典来获取关键字参数的值，其他关键字作为key,实参作为value

```python
def my_sum(**nums):
    print(nums)
    print(type(nums))

my_sum(a = 1)
# {'a': 1}
# <class 'dict'>
```


注意：

如果函数中既有不定长参数又有普通参数，那么不定长参数必须放在普通参数后边。

两个\*的参数要放在一个\*的后面

```python
def fun1(*args, **kwargs):
    print(args, kwargs)
    
fun1(10, 3, 4)
fun1(a= 10, b = 3, c = 2)
fun1(90, 23, z = 3, y = 3)
"""
(10, 3, 4) {}
() {'a': 10, 'b': 3, 'c': 2}
(90, 23) {'z': 3, 'y': 3}
"""
```


## 三、返回值

##### 1、什么是返回值

a、返回值就是函数调用表达式的值，就是return关键字后面的表达式的值。返回值就是将函数里面的数据传递到函数外面。

b、Python中每个函数都有返回值，默认是None，如果遇到return ，return 后面是什么返回值就是什么。

函数调用表达式 - 调用函数的语句

return - 关键字，只能写在函数体中。

return功能：

1. 确定函数的返回值
2. 结束函数，执行时遇到return，函数直接结束，并且将return后面的值作为函数的返回值。

```python
def func1():
    print('***')
    
result = func1()
print(resut)  # None
```

##### 2、多个返回值

return 值1, 值2, 值3...      相当于返回一个元祖

```python
def fun3():
    return 1, 2, 3

fun3()
print(type(fun3()))
```

##### 3、怎么确定函数是否需要返回值

函数执行完成后是否产生新的数据，如果产生新的数据就将这个数据用return返回。

## 四、练习

##### 1.计算5的阶乘 5!的结果是

```python
fact_number = 5
result = 1
while fact_number:
    result *= fact_number
    fact_number -= 1
print(result)
```

##### 2.求1+2!+3!+...+20!的和 

1.程序分析：此程序只是把累加变成了累乘。

```python
for number in range(1, 21):
    fact_result = 1
    while number:
        fact_result *= number
        number -= 1
    result += fact_result
print(result)
```

##### 3.计算 1+1/2!+1/3!+1/4!+...1/20!=?

```python
result = 0
for number in range(1, 21):
    fact_result = 1
    while number:
        fact_result *= number
        number -= 1
    result += 1/fact_result
print(result)
```



##### 4.循环输入大于0的数字进行累加，直到输入的数字为0，就结束循环，并最后输出累加的结果。

```python
numbers = []
number = int(input('请输入大于0的数字：'))
while number != 0:
    numbers.append(number)
    number = int(input('请输入大于0的数字：'))
print('输入累加的结果',sum(numbers))
```