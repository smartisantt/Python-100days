> Author: 陈伦巨
>
> Data: 2019-08-09
>
> Email: 545560793@qq.com
>
> github: https://github.com/smartisantt



## SQL注入

![](https://github.com/smartisantt/Python-100days/blob/master/%E6%95%B0%E6%8D%AE%E5%BA%93/res/exploits_of_a_mom.png?raw=true)



上面的图片来自：<https://bobby-tables.com/>，下面的对话就是关于SQL注入。

**School**: Hi, this is your son's school. We're having some computer trouble.

**Mom**: Oh, dear -- Did he break something?

**School**: In a way. Did you really name your son `Robert'); DROP TABLE Students;--`?

**Mom**: Oh. Yes. Little Bobby Tables we call him.

**School**: Well, we've lost this year's student records. I hope you're happy.

**Mom**: And I hope you've learned to sanitize your database inputs.



```python
import pymysql

db = pymysql.connect(
    host = '127.0.0.1',
    user = 'root',
    password = 'hbb123',
    port = 3306,
    db = 'mydb'
)

cur = db.cursor()

# name = input("Input:")
# print(name)

# # 使用 execute() 方法执行 SQL，如果表存在则删除
# cur.execute("DROP TABLE IF EXISTS EMPLOYEE")
#
# # 使用预处理语句创建表
# sql = """CREATE TABLE EMPLOYEE (
#          ID INT PRIMARY KEY auto_increment,
#          FIRST_NAME  CHAR(20) NOT NULL,
#          LAST_NAME  CHAR(20),
#          AGE INT,
#          SEX CHAR(1),
#          INCOME FLOAT )"""

# SQL 查询语句
name = input("Input:")
sql = "SELECT * FROM EMPLOYEE \
       WHERE first_name = '%s'" % (name)

cur.execute(sql)
res = cur.fetchall()
print(res)

cur.close()
db.close()
```



#### 1、情景一

当正常输入的时候：

```
Input:Mac
((3, 'Mac', 'Mohan', 20, 'M', 2000.0),)
```



非法输入的时候：

```
Input:' or 1=1 or '
((3, 'Mac', 'Mohan', 20, 'M', 2000.0), (4, 'aaa', 'Mohan', 20, 'M', 2000.0), (5, 'bbb', 'Mohan', 20, 'M', 2000.0), (6, 'cc', 'Mohan', 20, 'M', 2000.0))
```

最终执行的sql命令为：

```sql
SELECT * FROM EMPLOYEE \
       WHERE first_name = '' or 1=1 or '';
```

此时条件1=1始终为真，则查询了所有信息，实现了sql注入。





#### 2、情景二

先将查询代码改成如下条件(因为数据库中没有age=30的数据，所以查询结果始终为空)：

```python
name = input("Input:")
sql = "SELECT * FROM EMPLOYEE \
       WHERE first_name = '%s' and age=%d" % (name, 30)
```



正常输入：

```
Input:Mac
()
```



非法输入的时候：

```
Input:Mac' -- aaa
((3, 'Mac', 'Mohan', 20, 'M', 2000.0),)
或者
Input:Mac' # aaa
((3, 'Mac', 'Mohan', 20, 'M', 2000.0),)
```

 最终执行的sql命令为：(-- aaa  和 # aaa是mysql中的注释，后面的代码不参与到sql语句中)

```mysql
SELECT * FROM EMPLOYEE \
       WHERE first_name = 'Mac'; -- aaa  
```



### 预防 SQL 注入 – pymysql 参数化语句



#### 1、情景一

现在将代码改成如下：

```python
name = input("Input:")
sql = "SELECT * FROM EMPLOYEE \
        WHERE first_name = %s"

cur.execute(sql, (name, ))
```



测试：

```
Input:Mac
((3, 'Mac', 'Mohan', 20, 'M', 2000.0),)

Input:' or 1=1 or '
()
```



#### 2、情景二

```python
name = input("Input:")

sql = "SELECT * FROM EMPLOYEE \
        WHERE first_name = %s and age=30"
```



测试：

```python
Input:Mac
()

Input:Mac' -- aaa
()
```



### 总结：

不要使用拼接字符串的格式，容易被SQL注入：

```python
cmd = "update people set name='%s' where id='%s'" % (name, id)
curs.execute(cmd)
```

建议使用：

```python
cmd = "update people set name=%s where id=%s"
curs.execute(cmd, (name, id))
```

如果查询参数只有一个变量的时候：

```python
cmd = "SELECT * FROM PEOPLE WHERE name = %s"
curs.execute(cmd, (name,))
```







## XSS攻击

XSS（Cross Site Scripting）攻击通常指的是通过利用网页开发时留下的漏洞，通过巧妙的方法注入恶意指令代码到网页，使用户加载并执行攻击者恶意制造的网页程序。

HTML是一种超文本标记语言，通过将一些字符特殊地对待来区别文本和标记，例如，小于符号（<）被看作是HTML标签的开始，\<title>与\</title>之间的字符是页面的标题等等。当动态页面中插入的内容含有这些特殊字符（如<）时，用户浏览器会将其误认为是插入了HTML标签，当这些HTML标签引入了一段JavaScript脚本时，这些脚本程序就将会在用户浏览器中执行。所以，当这些特殊字符不能被动态页面检查或检查出现失误时，就将会产生XSS漏洞。



使用python bleach让html干净

`pip install bleach`



```python
import bleach

print(bleach.clean('<h1>My title</h1>'))
# &lt;h1&gt;My title&lt;/h1&gt;
```

