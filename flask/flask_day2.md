

> Author: 陈伦巨
>
> Data: 2019-04-05
>
> Email: 545560793@qq.com
>
> github: https://github.com/smartisantt



## 一、响应

响应是后端响应给前端的内容。

##### 1、导包:

`from flask import make_response`

##### 2、响应

`make_response('响应内容', 状态码)`

成功响应的状态码是200，也可以手动修改状态码（不建议手动修改）。

响应的内容可以是页面的源码。

也可以响应页面。（在工程目录下新建两个文件夹，分别是static和templates，在templates中新建index.html)

例如：

```python
@app.route('/make_res/')
def make_res():
    # 响应状态码
    # return make_response('Hello', 200)
    # 响应网页源码
    # return make_response('<div style="color:red; font-size:34px;">hello flask day02</div>')
    # 响应页面
    index = render_template('index.html')
    return make_response(index, 200)    # 200为状态码，不写默认200
```





## 二、模拟注册页面

在templates文件下准备两个html文件

register.html文件，内容如下：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>注册页面</title>
</head>
<body>
    <!--action是请求提交的地址，不写默认是当前的地址-->
    <form action="" method="post">
        <p>姓名：<input type="text" name="username"></p>
        <p>密码：<input type="password" name="password"></p>
        <p>确认密码：<input type="password" name="password2"></p>
        <p><input type="submit" value="提交"></p>
    </form>
</body>
</html>
```

login.html文件，内容如下：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>登录页面</title>
</head>
<body>
    <!--action是请求提交的地址，不写时当前的地址-->
    <form action="/login/" method="post">
        <p>姓名：<input type="text" name="username"></p>
        <p>密码：<input type="password" name="password"></p>
        <p><input type="submit" value="提交"></p>
    </form>
</body>
</html>
```



后端文件：

注册：

```python
@app.route('/register/', methods=['GET', 'POST'])
def register():
    print(request.method)
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        # 模拟注册功能
        # 获取前端传来的值
        username= request.form.get('username')
        password= request.form.get('password')
        password2= request.form.get('password2')
        # 校验前端前传来的值
        if username == 'ququ' and password == password2 == '123456':
            return render_template('login.html')
        else:
            return render_template('regist.html')
```

注意：`if request.methos == 'GET'` 是判断请求方式。



登录：

```python
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        # 获取前端传来的值
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'ququ' and password  == '123456':
            return render_template('index.html')
        else:
            return render_template('login.html')
```









## 二、cookie

##### 1、什么是cookie

登录网址，登录网址的时候是一直登录的，打开该网站其他页面怎么知道我是登录的？

由于HTTP无状态协议，无法记录当前用户是否登录。为了解决登录状态的保持我们要使用cookie，**cookie 用来识别用户。**cookie保存一个令牌（标识符）用于识别用户的登录状态。cookie是不能跨浏览器的。比如：你用IE浏览器登录你的淘宝账号，你同时打开火狐浏览器的淘宝，是未登录状态。



##### 2、设置

cookie是在用户登录成功的时候设置的。这个cookie好比一个同行证。

```python
# 获取响应对象
res = make_response(render_template('index.html'))
# 设置cookie
res.set_cookie('token', '12345', max_age=600)
return res # 响应给页面的时候给cookie添加了一个参数token
```



设置好cookie之后，用户下次再来访问，我们从request中的cookie去获取token值，校验value是否和设置的相等。校验成功则无需再次输入用户名和密码登录。实际项目中token值设置成随机数。



##### 3、校验登录

```python
@app.route('/index/')
def index():
    # 登录之后才能看到index.html页面，没有登录跳到登录页面
    token = request.cookies.get('token')
    if token == '12345':
        # 判断登录成功
        return render_template('index.html')
    else:
        return render_template('login.html')
```





##### 4、退出登录

退出登录就是要删除当前用户的token

```python
 res = make_response()
res.delete_cookie('token')
```

注意：cookie中设置的参数有字节限制，一般用来保存token，不能无限的存储参数，cookie不能跨浏览器浏览。

## 三、session



session数据保存在客户端(flask默认存储session的形式)

导包：`from flask import session`

设置：`session[key]=value`

用session的方式实现登录：

```python
@app.route('/session_login/', methods=['GET', 'POST'])
def session_login():
    if request.method == 'GET':
        return render_template('session_login.html')

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'ququ' and password == '123456':
            # 启动permanent修改为True
            session.permanent = True
            session['login_state'] = 1
            return render_template('index.html')
        else:
            return render_template('session_login.html')
```

运行上面的代码，输入用户名和密码后会报错：

```
RuntimeError: The session is unavailable because no secret key was set.  Set the secret_key on the application to something unique and secret.
```

这里需要设置`app.secret_key`加密复杂程度和设置有关。



```python
# session加密方式
app.secret_key = '123'

# 设置过期时间，5秒后session失效
app.permanent_session_lifetime = 5
```

用session方式验证用户是否登录：

```python
@app.route('/session_index/')
def session_index():
    if 'login_status' in session:
        return render_template('index.html')
    else:
        return render_template('session_login.html')
```

注意:

1）设置一个持久化会话的存活时间，必须修改session.permanent的属性和flask对象app的permanent_session_lifetime属性，permanent_session_lifetime属性作为datetime.timedelta对象，从Flask0.8开始也可以用一个整数表示多少秒后过期。

2）加密的强度取决于SECRET_KEY的复杂程度。一般SECRET_KEY可以通过os.urandom(24)随机生成。







## 四、应用

Session和Cookie的结合使用，一般有两种存储方式：

**第一种**：session数据存储在客户端：

Flask采用‘secure cookie’方式保存session，即session数据是使用base64编码后保存在客户端的cookie中。也就是说无需依赖第三方数据库保存session数据。

**第二种**：session数据存储在服务端：

步骤1：客户端发送请求到服务端，服务端会校验cookie中的sessionid值，如果cookie中不存在sessionid则认为客户端访问服务端时，是发起了一个新的会话

步骤2：如果是新的会话，则服务端传递给客户端一个cookie，并在cookie中存储一个新的sessionid值，并将相关数据保存在session中。

步骤3：客户端下次再次发送请求的时候，请求上下文对象会携带cookie，通过校验cookie中的sessionid值，即可判断是否是同一会话。

步骤4：如果校验是同一会话，则可以从session中获取到之前保存的数据。

安装第三库：`pip install flask-session`

还要安装redis ：`pip install redis`



```python
# 配置session
from flask_session import Session
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.Redis()
app.secret_key = '1234567890' # 设置加密程度
Session(app)
```





