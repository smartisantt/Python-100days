> Author: 陈伦巨
>
> Data: 2019-04-06
>
> Email: 545560793@qq.com
>
> github: https://github.com/smartisantt



## 一、装饰器

装饰器条件
1.外层函数嵌套内层函数
2.外层函数返回内层函数
3.内层函数调用外层函数的参数

在这里我们用装饰用来给用户做验证，例如下面是大体的装饰器框架：

```python
def is_login(func):

    def check():
        return func() # 2.后执行

    return check # 1.先执行
```

在需要验证的地方使用`@ is_login`来装饰，装饰器先执行，然后再执行被装饰的函数。





我们在工程同级目录下新建一个utils包，在里面新建一个`functions.py`文件

```python
from functools import wraps

from flask import session,render_template

# 创建验证用户登陆功能装饰器
def is_login(func):
    @wraps(func)
    def check():
        try:
            session['login_status']
            # 登录过后,再执行被装饰的函数。访问index.html 页面
            return func()
        except:
            # 没有登录不让访问，跳转到session_login.html页面
            return render_template('session_login.html')
    return check
```

-  装饰器的作用:    在不改变原有功能代码的基础上,添加额外的功能,如用户验证等
-  @wraps(view_func)的作用:     不改变使用装饰器原有函数的结构(如\_\_name\_\_, \_\_doc__)
-  不使用wraps可能出现的ERROR:   view_func...endpoint...map...









## 二、蓝图

MVC

M:模型(Model)  定义一个类关联数据表

V：视图(View) templates

C: 控制器(controller) 业务逻辑

我们安装MVC把原来的文件拆分。

在同级目录下新建app包，在里面新建app.py文件，之前更路由相关功能的函数全都剪切到这个文件里面，然后完成相应导包工作，然后运行程序，发现输入原来正确的地址并无法访问网页。

这个要使用第三方库管理路由。安装第三方库 `pip install flask-blueprint`



使用范例：

```python
from flask import Blueprint # 安装完之后在views.py文件中导包

# 蓝图，管理路由地址
# 第一步，在views.py设置蓝图
blue = Blueprint('first', __name__)

# 第二步：在工程文件下注册蓝图
app.register_blueprint(blueprint=blue)

```

redirect 是跳转到指定页面，浏览器地址是你跳转的地址

 url_for是反向解析，通过`蓝图的第一个参数.跳转函数名`的语法格式实现跳转。

```python
# 页面跳转
redirect('/login/')

# url_for('蓝图的第一个参数.跳转的函数名') 反向解析路由地址
redirect(url_for('first.login'))
```

建议使用第二种，路由地址变化时但无需更改代码。



我们现在回头再看看之前写的模拟登陆注册的代码：

注册模块：

```python
# app.route 更改为blue来管理路由
@blue.route('/register/', methods=['GET', 'POST'])
def register():
    print(request.method)
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        username= request.form.get('username')
        password= request.form.get('password')
        password2= request.form.get('password2')
        if username == 'ququ' and password == password2 == '123456':
            # 下面的代码只是重新渲染当前页面，浏览器地址还是register
            # return render_template('login.html')
            # 下面的代码，实现页面重新选项，浏览器的地址也变成login
            return redirect(url_for('first.login'))
        else:
            return render_template('register.html')
```

登陆模块：

```python
# app.route 更改为blue来管理路由
@blue.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'ququ' and password  == '123456':
            # res = make_response(render_template('index.html'))
            # res.set_cookie('token', '12345', max_age=100)
            # return res
            # 反向解析生成响应对象，然后设置token
            response = redirect(url_for('first.index'))
            response.set_cookie('token', '12345')
            return response
        else:
            return render_template('login.html')
```

之前写的相关跳转页面本质只是重新渲染，浏览器路由地址并非实现跳转，我们只是在html文件的form表单的action参数中配置成提交表单的跳转，改成url_for跳转的代码，则无需配置form表单的action参数。

**反向解析的时候路由怎么传参数？**

```python
@blue.route('/redirect_func/')
def redirect_func():
    # url_for第二个参数是传给路由参数的值
    return redirect(url_for('first.s_id', id=6666))

@blue.route('/s_id/<int:id>/')
def s_id(id):
    return 's_id:%s'% id
```





## 三、模板

模板文件我们把它放在templates里面。

##### 1、模板内容

基础模板,通俗说就是动态内容挖坑。

模版中的坑长成以下几种样子：

- `{{ ... }}`：装载一个变量，模板渲染的时候，会使用传进来的同名参数这个变量代表的值替换掉。
- `{% ... %}`：装载一个控制语句。
- `{# ... #}`：装载一个注释，模板渲染的时候会忽视这中间的值。

##### 2、创建base.html基础模板

```jinja2
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>
        {% block title %}
        {% endblock %}
    </title>
    {# 注意：模板名字不能重名 #}
    {% block css %}
    {% endblock %}

    {% block js %}
    	{# 子模板公有的js文件放在这里 #}
    {% endblock %}
</head>
<body>
    {% block content %}
    {% endblock %}
</body>
</html>
```



##### 3、继承基础模板的模板文件

```jinja2
{% extends 'base.html' %}

{% block js %}
    {{ super() }}
    <script src="23.js"></script>
{% endblock %}
{# 给子模板添加多个js #}
```

最终模板显示的顺序跟子模板的顺序跟父模板挖坑的顺序有关，跟子模板顺序无关。

父模板挖的坑，子模板不是所有的坑都要填，而是根据实际需求动态选择性地去填充父模板中定义的block的坑，{% block name%} 动态内容 {% endblock %}。

调用父模板中的内容，如果不调用super，则子模板会覆盖掉父模板中的内容。



 	



##### 4、引入静态文件

静态文件主要包括有`CSS`样式文件、`JavaScript`脚本文件、图片文件、字体文件等静态资源。

在`Jinja`中加载静态文件只需要通过`url_for`全局函数就可以实现：

```jinja2
{% block css %}
    {# 引入样式的第一种写法 #}
    <link rel="stylesheet" href="/static/css/style.css">
    {# 引入样式的第二种写法 #}
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
{% endblock %}
```

改变静态文件之后，要清除浏览器的缓存，最新的样式才会显示出来。



##### 5、后端返回数据

在渲染的时候就加参数，多个参数用逗号分隔。

```python
@blue.route('/student/')
def stu():
    stus_scores = [90, 89, 100, 99, 87, 67]
    # stus_scores = []
    content_h2 = '<h2>你真的很棒！</h2>'
    return render_template('stu.html', scores=stus_scores, content_h2=content_h2)
```



##### 6、变量

在模板中添加变量，可以使用（set）语句。

```jinja2
{% set name='xx' %}
```



##### 7、控制语句

```jinja2
{% if 条件语句1 %}
	符合条件1显示的内容
{% elif 条件语句2 %}
	符合条件2显示的内容
{% else %}
	不符合条件1和条件2显示的内容
{% endif %}
```

##### 8、for循环

1)普通用法

```jinja2
<ul>
{% for user in users %}
<li>{{ user.username|e }}</li>
{% endfor %}
</ul>
```

2)遍历字典

```jinja2
{% for key, value in my_dict.iteritems() %}
<dt>{{ key|e }}</dt>
<dd>{{ value|e }}</dd>
{% endfor %}
```

3）在循环中加入else

for 循环的变量users不存在或者users值为空，则执行else中的语句。

```jinja2
<ul>
{% for user in users %}
<li>{{ user.username|e }}</li>
{% else %}
<li><em>no users found</em></li>
{% endfor %}
</ul>
```

4）for循环中的变量

for循环中的变量都鞋子for循环里面

| 变量                 | 说明                          |
| -------------------- | ----------------------------- |
| {{  loop.index }}    | 当前循环次数（从1开始）       |
| {{ loop.index0 }}    | 当前循环次数（从0开始）       |
| {{ loop.revindex }}  | 当前循环次数（倒序，以1结束） |
| {{ loop.revindex0 }} | 当前循环次数（倒序，以0结束） |
| {{ loop.first }}     |    循环的第一次返回True，否则返回False          |
| {{ loop.last }} |         循环的最后一次返回True，否则返回False     |





**注意：在Jinja2中不可以使用continue和break表达式来控制循环的执行。**

4）Jinja2中for循环内置常量

| 代码          | 说明                      |
| ----------- | ----------------------- |
| loop.index  | 当前迭代的索引（从1开始）           |
| loop.index0 | 当前迭代的索引（从0开始）           |
| loop.first  | 是否是第一次迭代，返回True或者False  |
| loop.last   | 是否是最后一次迭代，返回True或者False |
| loop.length | 序列的长度                   |



##### 9、过滤器

过滤器是通过`|`符号进行使用的，例如：`{{ name|length }}`将返回name的长度。可以看成name是传入length函数的参数，然后过滤器根据自己的功能，再返回相应的值，之后再将结果渲染到页面中。

| 代码    | 说明                                                         |
| ------- | ------------------------------------------------------------ |
| abs     | 返回一个数值的绝对值。示例：`{{ -1|abs }}  `                 |
| length  | 返回一个序列或者字典的长度。示例：{{ msg\|length }}          |
| safe    | `safe`过滤器会使网页解析标签。示例：` {{content_html|safe}} `。 |
| default | 如果当前变量没有值，则会使用参数中的值来代替。示例：`{{name|default('xiaotuo')}}` |
| int     | 将值转换为`int`类型                                          |



自定义过滤器：

```python
def mylen(arg):
    return len(arg)

env = app.jinja_env
# 给filters增加名为'mylen'的过滤器
env.filters['mylen'] = mylen
```



在模板文件文件中使用，`mylen`为过滤器名字，解析的时候找到对应的处理函数，把前面额msg当做参数传给对应的处理函数（在本例子中是`mylen(arg)`）处理，最后返回的结果显示在页面上。

```jinja2
{{ msg|mylen }}
```



