



![程序结构](https://raw.githubusercontent.com/smartisantt/Python-100days/master/Day01-10/Day03/res/day03.jpg)

[脑图地址](http://naotu.baidu.com/file/0459fc6f503ca631ae6b9e3a80bcf35a?token=1853bee2f41c94da)(以下文档有脑图生成)

# 程序结构

## 顺序结构

## 分支结构

### if

### if    else

### if elif else

## 循环结构

### for 

#### 使用场景：确定次数

#### for  else

在这种结构中，当for循环正常执行后，程序会继续执行else语句中的内容，如果for循环因为某种行为没有正常执行完，如遇到break语句，则不会执行else语句中的内容。

### while

#### 使用场景：不确定次数

#### while else

在这种结构中，当while循环正常执行后，程序会继续执行else语句中的内容，如果while循环因为某种行为没有正常执行完，如遇到break语句，则不会执行else语句中的内容。

## break

### 提前结束循环语句

### 结束本层的循环

## continue

### 结束循环运行

### 只能结束本次循环的执行

### 不终止循环



### 练习：
##### 练习1：百分制成绩转等级制

```python
"""
百分制成绩转等级制成绩
90分以上 	 	--> A
80分~89分 	--> B
70分~79分	--> C
60分~69分	--> D
60分以下		--> E
Version: 0.1
Author: 陈伦巨
Date: 2019-03-11
"""

score = float(input('请输入成绩: '))
if score >= 90:
	grade = 'A'
elif score >= 80:
	grade = 'B'
elif score >= 70:
	grade = 'C'
elif score >= 60:
	grade = 'D'
else:
	grade = 'E'
print('对应的等级是:', grade)
```

##### 练习2：百元百鸡

```python
"""
百元百鸡问题：
已知：公鸡5元1只；母鸡3元一只；小鸡1元3只。
问想100元正好买100只鸡，应该如何买？
Version: 0.1
Author: 陈伦巨
Date: 2019-03-11
"""
for x in range(0, 21):
    for y in range(0, 34):
        z = 100 - x - y
        if 5*3 + 3*y + z/3 == 100:
            print("公鸡买%d只， 母鸡买%d只，小鸡买%d只。"%(x, y, z))
```

