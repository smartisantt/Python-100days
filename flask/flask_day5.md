> Author: 陈伦巨
>
> Data: 2019-04-09
>
> Email: 545560793@qq.com
>
> github: https://github.com/smartisantt



flask中模型关系

[参考文档](http://flask-sqlalchemy.pocoo.org/2.3/models/#many-to-many-relationships)

模型使用的字段

| 字段           | 说明           |
| -------------- | -------------- |
| Integer        | 整数           |
| String（size） | 最大长度字符串 |
| Text           | 长文本         |
| DateTime       | 日期和时间     |
| Float          | 浮点值         |



#### 一对多( one-to-many relationships)

班级（1）对学生（多）

外键写在多的一方，1的一方用relationship()表示关系。

班级模型：

```python
class Grade(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g_name=db.Column(db.String(10), nullable=False)
    stus = db.relationship('Student', backred='p')
```



学生模型：

```python
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    s_name = db.Column(db.String(10), unique=True, nullable=False)
    age = db.Column(db.Integer, default=20)
    g_id = db.Column(db.Integer, db.ForeignKey('grade.id'),nullable=True)
    
    __tablename__ = 'stu'
```



通过班级查询学生：

```python
@blue.route('/sel_stu_by_grade/')
def sel_stu_by_grade():
    # 查询Python班级所有学生信息
    g = Grade.query.filter(Grade.g_name == 'Python').first()
    print(g.stus)
    stu_names = [stu.s_name for stu in g.stus]
    print(stu_names)
    return '通过班级查询学生成功'
```

通过学生查询班级：

```python
@blue.route('/sel_grade_by_stu/')
def sel_grade_by_stu():
    # 学生名叫‘小张2’的同学所在班级信息
    stu = Student.query.filter(Student.s_name == '小张2').first()
    print(stu.g_id)
    # 通过反向引用查询
    print(stu.p)

    return '通过学生查询班级成功'
```



#### 多对多( many-to-many relationships)

学生（多）对课程表（多）

学生模型

```python
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    s_name = db.Column(db.String(10), unique=True, nullable=False)
    age = db.Column(db.Integer, default=20)
    g_id = db.Column(db.Integer, db.ForeignKey('grade.id'),nullable=True)

    __tablename__ = 'stu'
```



课程和学生的中间表（中间表在这里不是模型，所以无需基础db.Model）

```python
c_s = db.Table('c_s',
               db.Column('s_id', db.Integer, db.ForeignKey('stu.id')),
               db.Column('c_id', db.Integer, db.ForeignKey('course.id'))
               )
```



课程表模型

```python
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    c_name = db.Column(db.String(10), nullable=False, unique=True)
    stus = db.relationship('Student', secondary=c_s, backref='cou', lazy='dynamic')
```



relationship 的 `lazy` 属性指定 sqlalchemy 数据库什么时候加载数据：

- select：就是访问到属性的时候，就会全部加载该属性的数据
- joined：对关联的两个表使用联接
- subquery：与joined类似，但使用子子查询
- dynamic：不加载记录，但提供加载记录的查询，也就是生成query对象

[lazy用法参考文档](https://www.jianshu.com/p/8427da16729a)



学生表和课程表之间的操作：

```python
@blue.route('/add_cou_to_stu/')
def add_cou_to_stu():
    # 学生添加课程
    # 给id=1的学生添加线代和高数课程
    stu = Student.query.get(1)
    print(stu.cou)
    cou1 = Course.query.filter(Course.c_name == '线代').first()
    cou2 = Course.query.filter(Course.c_name == '高数').first()
    # stu.cou返回的值为该学生选择的课程对象组装成的列表结果
    stu.cou.append(cou1)
    stu.cou.append(cou2)
    # 提交
    db.session.commit()
    return '学生添加课程成功'


@blue.route('/del_stu_cou/')
def del_stu_cou():
    # 删除id为1学生所选择的高数这门课
    stu = Student.query.get(1)
    cou2 = Course.query.filter(Course.c_name == '高数').first()
    # 删除remove()
    stu.cou.remove(cou2)
    db.session.commit()
    return '删除课程成功'
```



总结

| 一(班级)对多（学生）                   | 多（课程）对多（学生）                     |
| ---------------------------------- | ---------------------------------- |
| `stus=db.relationship('Student',backref='p')` | `stus = db.relationship('Student', secondary=c_s, backref='cou')` |
| 没有中间表（ForeignKey写在多的一方）| 需要中间表（ForeignKey写在中间表） |
| 知道班级查学生：`班级对象.stus` | 知道课程查学生：`课程对象.stus` |
| 知道学生查班级：`学生对象.backref` | 知道学生查课程：`学生对象.backref` |



附：在此项目中Flask使用的第三方库版本

```python
Flask==1.0.2
flask-blueprint==1.2.7
Flask-Script==2.0.6
Flask-Session==0.3.1
Flask-SQLAlchemy==2.3.2
PyMySQL==0.9.3
redis==3.2.1
SQLAlchemy==1.3.2
```