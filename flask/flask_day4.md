> Author: 陈伦巨
>
> Data: 2019-04-07
>
> Email: 545560793@qq.com
>
> github: https://github.com/smartisantt

## 一、ORM

对象关系映射ORM(Object Relational Mapping)是一种为了解决面向对象与关系数据库存在的互不匹配的现象的技术。简单的说ORM要完成对象要映射到数据库中的表。这个操作就避免使用SQL语句来操作数据库。那是怎么映射的呢？

**Mapping Logic**

| Object                  | Relation DB            |
| ----------------------- | ---------------------- |
| 类（class）             | 数据库的表（table）    |
| 对象（object）          | 记录（record，行数据） |
| 对象的属性（attribute） | 字段（field）          |



不使用ORM操作数据的写法如下：

```python
import MySQLdb

# 打开数据库连接
db = MySQLdb.connect("localhost", "testuser", "test123", "TESTDB", charset='utf8' )

# 使用cursor()方法获取操作游标 
cursor = db.cursor()

sql = "select id, first_name, last_name, phone, birth_date, sex from persons where id = 10"
res = cursor.execute(sql)
name = res[0]["FIRST_NAME"]
db.commit()
# 关闭数据库连接
db.close()
```



改成ORM的写法如下：

```python
p = Person.get(10);
name = p.first_name;
```

ORM的优点：

- 基于ORM的月舞代码比较简单，代码量少，容易理解
- 不必编写SQL语句

- ORM是天然的Model，最终是代码更清晰

ORM的缺点：

- ORM库不是轻量级工具，需要花很多精力学习和设置。
- 对于复杂的查询，ORM要么是无法表达，要么是性能不如原生的SQL





## 二、配置数据库

安装第三方库

 `pip install pymysql==0.9.3`

`pip install flask-sqlalchemy==2.3.2`

[flask-sqlalchemy文档](http://flask-sqlalchemy.pocoo.org/2.3/config/)



 创建模型

```python
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_script import Manager

# 生成数据库访问对象db
db = SQLAlchemy()

app = Flask(__name__)
# 配置数据库
# 格式：dialect+driver://username:password@host:port/database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/flask9'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化app
db.init_app(app)

class Student(db.Model):
    # 定义id主键，自增字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 定义不能为空，且唯一的姓名字段
    s_name = db.Column(db.String(10), unique=True, nullable=False)
    # 定义整型，默认为20的年龄字段
    age = db.Column(db.Integer, default=20)
    
    
 if __name__ == '__main__':
    manage.run()
```



数据库连接格式：`'mysql+pymysql://root:123456@127.0.0.1:3306/flask9'`



## 三、迁移

##### 1、迁移模型：

访问create_db路由的时候，会调用create_db的方法，执行create_db的方法，就会识别模型映射成数据库中的某张表。

```python
@blue.route('/create_db/')
def create_db():
    # 迁移模型
    db.create_all() #把模型映射成数据库中的表
    return '创建表成功'
```



创建表：`db.create_all()`

第一次迁移模型的时候才有用，如果更改Object中的字段（增加字段，删除字段，更改约束等）再执行create_db是无效的。

删除表：`db.drop_all()`



##### 2、插入数据

将数据插入数据库有三步：

1. 创建Python对象
2. 将其添加到会话中
3. 提交会话（这里的会话不是Flask会话，而是Flask-SQLAlchemy会话。本质上是数据库事务的增强版本。

```python
@blue.route('/add_stu/')
def add_stu():
    # 新增学生数据
    stu = Student()
    stu.s_name = '小花'
    stu.age = 20
    # 准备SQL语句
    db.session.add(stu)
    # 执行SQL语句
    db.session.commit()
    return '添加数据成功'
```



批量添加数据：

```python
@blue.route('/add_stus/')
def add_stus():
    # 批量添加内容
    for i in range(10):
        stu = Student()
        stu.s_name = '小李' + str(i)
        stu.age = int(i)
        db.session.add(stu)
    # 最后一次提交所有的数据
    db.session.commit()
    return '批量插入数据成功'
```

上面的方法循环一次就使用add方法，现在我们改成一次添加10个对象。

批量添加：`db.session.add_all(对象列表)`

```python
@blue.route('/add_stus/')
def add_stus():
    # 批量添加内容
    stu_list=[]
    for i in range(10):
        stu = Student()
        stu.s_name = '小李' + str(i)
        stu.age = int(i)
        stu_list.append(stu)
        # db.session.add(stu)
    # add_all的参数是对象的列表
    db.session.add_all(stu_list)
    # 最后一次提交所有的数据
    db.session.commit()
    return '批量插入数据成功'
```





##### 3、查询

**filter_by查询：**

```python
stu = Student.query.filter_by(s_name='小红2').first()
# 用first查询filter_by结果第一个对象，相当于下面的语句。
# stu = Student.query.filter_by(s_name='小红2').all()[0]
```



**filter查询:**

```python
stu = Student.query.filter(Student.s_name == '小红2').first()
```

filter查询不到信息不会报错，返回None。



常见错误信息如下：

```python
TypeError: filter() got an unexpected keyword argument 's_name'
```

解决方案：请检查你是否把filter和filter_by的用法混淆了。



**get查询：**

get只能查询填主键所在行的信息，主键为id。查询不到数据返回None。

```python
stu = Student.query.get(1)
```



**高级查询：**

###### 1）降序排序：

**注意：现在使用的SQLAlchemy的版本是1.3.2，低版本的降序排列写法与此不一样。**

```python
# id降序
stus = Student.query.order_by(-Student.id).all()
```

###### 2）升序排序：

  ```python
# 年龄升序
stus = Student.query.order_by(Student.age).all()
  ```



###### 3）offset 、limit

```python
# 取前3个
stus = Student.query.limit(3).all()
# 跳过前1个，取前3个
stus = Student.query.offset(1).limit(3).all()
```

应用场景：可以实现分页的操作。

```python
page = 1
# 方法一：每页有3个数据
stus = Student.query.offset((page-1)*3).limit(3).all()
print(stus)

# 方法二：
stus = Student.query.all()
print(stus[(page-1)*3:page*3])
```

###### 4）模糊查询

contain方法，检索出包含有目标字符的信息

```python
# 检测名字有'红'的学生信息
stus = Student.query.filter(Student.s_name.contains('红')).all()
```

like方法，%（匹配任何位的字符） _(匹配任意一个字符)

```python
# 查询名字以'小'开头的名字的信息
stus = Student.query.filter(Student.s_name.like('小%')).all()
# 查询名字有'小'的名字的信息
stus = Student.query.filter(Student.s_name.like('%小%')).all()
```

startswith和endswith方法，检测字符串以什么开头

```python
stus = Student.query.filter(Student.s_name.startswith('张')).all()
stus = Student.query.filter(Student.s_name.endswith('刚')).all()
```

###### 5） 比较

| 代码 | 说明 |      代码|说明      |
| ---- | ---- | ---- | ---- |
| `__gt__(10)` |  大于10| `__lt__(10)` | 小于10 |
| `__ge__(10)` | 大于等于10 | `__le__(10)` | 小于等于10 |

```python
# 查询年龄大于10的学生的信息
stus = Student.query.filter(Student.age.__ge__(10)).all()
print(stus)
# 下面的写法和上面的效果一样
stus = Student.query.filter(Student.age >= 10).all()
print(stus)
```



###### 6） in 和 notin

查询某个字段在或者不在什么范围之类

```python
# where in in [1,2,3,4,5]
stus = Student.query.filter(Student.id.in_([1,2,3,4])).all()
# 查询id不在
stus = Student.query.filter(Student.id.notin_([1,2,3,4])).all()
print(stus)
```



###### 7） 组合查询

查询条件有多个，例如查询年龄等于9，名字以‘小’开头的学生信息：

```python
# 先查询年龄，再查询名字
stus = Student.query.filter(Student.age == 9).filter(Student.s_name.like('小%')).all()
```

我们思考一下，有没有方法能把查询条件放在一个filter里面

```python
# 多个条件放在一个filter里面用逗号隔开，条件之间是并且的关系
stus = Student.query.filter(Student.age == 9,
                            Student.s_name.like('小%')).all()
# and操作
stus = Student.query.filter(Student.age == 22 and Student.s_name.like('%红%')).all()
```



或的条件

```
stus = Student.query.filter(Student.age == 22 or Student.s_name.like('%红%')).all()
```



sqlalchemy库中and, not, or

```python
from sqlalchemy import and_, not_, or_


stus = Student.query.filter(and_(Student.age == 22, 
                                     Student.s_name.like('张%'))).all()

stus = Student.query.filter(or_(Student.age == 22,
                                Student.s_name.like('张%'))).all()

stus = Student.query.filter(not_(Student.age == 2)).all()
# 等同于下面的语句
# stus = Student.query.filter(Student.age != 20).all()
```





##### 4、删除记录：

先查询出符合要求的数据，然后删除：

数据库的查询无需使用会话，增加，更改和删除需要使用到会话。

```python
@blue.route('/del_stu/')
def del_stu():
    # 删除年龄等于0的信息
    stus = Student.query.filter_by(age=0).all()
    for stu in stus:
        db.session.delete(stu)
    db.session.commit()
    return '删除数据成功'
```

##### 5、修改数据

```python
@blue.route('/update_stu/')
def update_stu():
    stu = Student.query.filter_by(s_name='小红2').first()
    stu.age = 22
    db.session.add(stu) # 这句话可以不写
    db.session.commit()
    return '修改数据成功'
```



##### 6、封装保存和修改方法

```python
class Student(db.Model):
    # 定义id主键，自增字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 定义不能为空且唯一的姓名字段
    s_name = db.Column(db.String(10), unique=True, nullable=False)
    # 定义整型，默认为20的年龄字段
    age = db.Column(db.Integer, default=20)

    # 设置在数据库中数据库表的名字
    __tablename__ = 'stu'

    def save(self):
        # 保存与修改
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
```

