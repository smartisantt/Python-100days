> Author: 陈伦巨
>
> Data: 2019-04-05
>
> Email: 545560793@qq.com
>
> github: https://github.com/smartisantt



Flask是一个轻量级的Web应用框架。


## 一、安装环境

##### 1、使用virtualenv安装

1. 在D盘创建两个文件夹英文名，代码(workspace)和环境(env)两个文件夹
2. 进入env 文件夹 `D: `   再输入`cd env`
3. `pip install virtualenv`
4. 创建一个叫flaskenv的虚拟环境名字   `virtualenv --no-site-packages flaskenv`
5. 进入文件`cd Scripts`
6. windows下输入 `activate`激活, Linux系统输入`source activate`
7. `pip list` 或者`pip freeze`可以查看当前安装环境
8. 安装`pip install flask`，也可以批量安装第三方库，新建一个txt文件里面每行写安装的第三方库和对应的版本，在终端进入环境，输入`python install -r 文件名`
9. 退出环境deactivate

说明：为什么要使用virtualenv？当你有很多项目，同时使用不同版本的Python和第三库的可能性也就越大。很悲观的是：常常Python或第三方库版本升级，升级后有时不向下兼容。所以，当你创建一个项目的时候，virtualenv为每个项目提供一份Python安装，它并没有真正安装多个Python副本，但是他去世提供了一种巧妙的方式来让各项目环境保持独立。

##### 2、flask的安装与使用

先激活环境，再执行pip install flask

Flask依赖两个外部库：Werkzeug和Jinja2。Werkzeug是一个WSGI（在Web应用和多种服务器之间的标准Python接口）工具集。Jinja2负责渲染模板。

说明：这里使用的Python3.3或更高的版本。

##### 3、启动

有两种启动方式：

第一种：flask自带的启动方式`app.run(host, port, debug)`

第二种：使用flask_script库启动

- `pip install flask_script`

- ```python
  from flask_script import Manager
  app = Flask(__name__)
  manage=Manager(app)
  manage.run()
  ```

- 在命令行中输入：`python xxx.py runserver -h -p -d`



## 二、快速入门

一个最小的 Flask 应用看起来会是这样:

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello World!'

if __name__ == '__main__'
	app.run()
```

把上面的文件保持为hello.py 文件（或是类似的），然后用Python解释器来运行：

```python
(flask_env) H:\wordspace\flask\flask>python manage.py
 * Serving Flask app "manage" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

注意：确保你的文件名不是flask.py，因为这将与Flask本身冲突。

现在访问 <http://127.0.0.1:5000/> ，你会看见 Hello World 问候。



那么上面的代码做了什么？

`from flask import Flask`导入了Flask类，这个类的实例将会是WSGI应用程序

`app = Flask(__name__)`，创建一个该类的实例，第一个参数是应用模块或者包的名称。如果你使用单一的模块，你应该使用`__name__`，因为模块的名称将会因其作为单独应用启动还是作为模块导入而有不同（ 也即是 `'__main__'` 或实际的导入名）。

`@app.route('/')`装饰器告诉 Flask 什么样的URL 能触发我们的函数。

`app.run()`函数让应用运行在本地服务器上。其中 `if __name__ =='__main__':` 确保服务器只会在该脚本被 Python 解释器直接执行的时候才会运行，而不是作为模块导入的时候。



欲关闭服务器，在命令行中按 Ctrl+C。



*补充知识：*

Python 中有许多web框架，为了更好读兼容性，python定义了web框架和web服务器之间读接口，即

[PEP-3333](https://www.python.org/dev/peps/pep-3333/)，PEP-333指定了服务器和Python web应用程序或框架之间拟议的标准接口，以促进跨各种web服务器的web应用程序可移植性。

WSGI(全称即：**Python Web Server Gateway Interface**)  

用户（client）发各种请求，发送给server（gateway） 去call    Application层（里面有各种各样的object，比如函数，class等），然后在返回个server在返回给user，server和Application中间有middleware（中间件）。



## 三、调试模式

调试模式：

虽然`app.run()`方法适用于启动本地的开发服务器，但是你每次修改代码后都要手动重启它。这样并不够优雅。

**调试模式绝对不能用于生产环境！！！**

在flask自带的启动方式中有两种途径启动调试模式：

第一种：

```python
app.debug = True
app.run()
```

第二种：

```python
app.run(debug=True)
```

两种方法的效果完全相同。当你运行程序的时候，修改您的代码然后保存程序会自动重启。



## 四、路由

`route()` 装饰器把一个函数绑定到对应的 URL 上。

基本例子：

```python
@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello World'
```



有变量的路由：

语法：`<转化器: 变量名>`

转化器有下面几个

| 转化器类型 | 说明                   |
| ---------- | ---------------------- |
| int        | 接受整数               |
| float      | 接受整数和浮点数       |
| string     | 指定字符串（默认类型） |

`<string:name>`和`<name>`是一样的效果。



```python
@app.route('/echo/<msg>')
def echo(msg):
    return '<h1>Hello, I am a Website I can echo everything: {}</h1>'.format(msg)


@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'Post %d' % post_id


@app.route('/float/<float:num>')
def float(num):
    return 'float num is : {:.2f}'.format(num)
```



看看下面的两个例子，虽然它们看起来着实相似，但它们结尾斜线的使用在 URL *定义* 中不同。

 第一种情况中，指向 projects 的规范 URL 尾端有一个斜线。这种感觉很像在文件系统中的文件夹。访问一个结尾不带斜线的 URL 会被 Flask 重定向到带斜线的规范 URL 去，然而，

第二种情况的 URL 结尾不带斜线，访问结尾带斜线的 URL 会产生一个 404 “Not Found” 错误。

```python
# 第一种情况，URL结尾有斜线
@app.route('/projects/') 
def projects():
    return 'The project page'

# 第二种情况，URL结尾没有斜线
@app.route('/about')
def about():
    return 'The about page'
```





## 五、获取请求参数

get和post传参：

HTTP协议未规定GET和POST传参长度的限制，但是浏览器和web服务器对其有限制，不同浏览器和web服务器限制的长度不一样。

get传参格式：`127.0.0.1：80/login/?username=ququ&password=123`

get是通过路由传参数，？后面的参数无需匹配路由，只匹配？前面的内容。

post传参格式:`127.0.0.1：80/login/`

post请求传参数，请求参数是放在请求体（body）里面的。比如登录的用户名和密码等重要的内容都用POST传参数。

使用到的工具postman。



获取GET请求参数的内容：

```python
@app.route('/params/')
def params():
    # 获取GET请求传递的参数
    name = request.args['name']		# 获取GET请求的参数没有时会报错
	name = request.args.get('name') # 获取GET请求的参数，使用get方法没有值也不会报错
    age = request.args.get('age')
    return '获取GET请求的参数：name=%s age=%s。'%(name, age)
```



获取POST请求参数的内容：

```python
# 默认请求方式个GET，设置了POST则无法接受GET请求
@app.route('/post_params/', methods=['POST'])
def post_params():
    name = request.form['name']
    name = request.form.get('name')
    age = request.form.get('age')
    favourites = request.form.getlist('favourite')
    print(favourites)
    return '获取post参数:name=%s age=%s favourite=%s'%(name, age, [favourite for favourite in favourites])
```

注意：`getlist`是获取POST请求有很多相同变量名的值，结果以列表返回。应用场景，在前端提交有checkbox的表单时，获取checkbox复选框的值得时候。










