 > Author: 陈伦巨
 >
 > Data: 2019-08-14
 >
 > Email: 545560793@qq.com
 >
 > github: https://github.com/smartisantt 



## Django工程下的settings.py中日志配置

```python
LOGGING = {
    'version': 1,
    # 是否禁用已经存在的日志器
    'disable_existing_loggers': False,
    # 日志格式化器
    'formatters': {
        'simple': {
            'format': '%(asctime)s %(module)s.%(funcName)s: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        # 详细
        'verbose': {
            'format': '%(asctime)s %(levelname)s [%(process)d-%(threadName)s] '
                      '%(module)s.%(funcName)s line %(lineno)d: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        }
    },
    'filters': {
        # 只有在Django配置文件中DEBUG值为True时才起作用
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        # 输出到控制台
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'formatter': 'simple',
        },
        # 输出到文件(每周切割一次)
        'file1': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'access.log',
            'when': 'W0',
            'backupCount': 12,              #备份份数
            'formatter': 'simple',          #使用哪种formatters日志格式
            'level': 'DEBUG',
        },
        # 输出到文件(每天切割一次)
        'file2': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'error.log',
            'when': 'D',
            'backupCount': 31,
            'formatter': 'verbose',
            'level': 'WARNING',
        },
        # 输出到文件(每周切割一次) -- 用户访问IP和访问的路径
        'file3': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'ipandpath.log',
            'when': 'W0',
            'backupCount': 12,              #备份份数
            'formatter': 'simple',          #使用哪种formatters日志格式
            'level': 'INFO',
        },
    },
    # CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTEST
    'loggers': {
        'django': {
            # 需要使用的日志处理器
            'handlers': ['console', 'file1', 'file2'],
            # 是否向上传播日志信息
            'propagate': True,
            'level': 'DEBUG',
        },
        'ipandpath': {
            # 需要使用的日志处理器
            'handlers': ['file3'],
            # 是否向上传播日志信息
            'propagate': False,
            'level': 'INFO',
        },
    }
}
```



#### 说明：现在服务器要打印用户的真实IP地址，并单独保存在一个文件中。

配置代码如下：`handlers `指定了日志输出文件位置和文件名（就是上面配置的信息）。

```python
'ipandpath': {
    # 需要使用的日志处理器
    'handlers': ['file3'],
    # 是否向上传播日志信息
    'propagate': False,
    'level': 'INFO',
}
```



## 使用

在程序合适的位置，一般是程序鉴权的入口处，放如下代码：

```python
logger = logging.getLogger('ipandpath')

# 日志消息
remote_info = ''
x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
if x_forwarded_for:
    remote_info = ' HTTP_X_FORWARDED_FOR:' + x_forwarded_for.split(',')[0]
else:
    remote_addr = request.META.get('REMOTE_ADDR')
    remote_info += ' REMOTE_ADDR:' + remote_addr

token = request.META.get('HTTP_TOKEN')
user_agent = request.META.get('HTTP_USER_AGENT')

logger.info( remote_info + ' URL:' + request.path + ' METHOD:' + request.method +
                     ' TOKEN:' + token + ' USER_AGENT:' + user_agent)
```



如果此时在日志中查看：打印的日志全是`REMOTE_ADDR:172.18.0.1`，则没有正确的获取用户的IP信息。

![](https://github.com/smartisantt/Python-100days/blob/master/Django/res/%E6%97%A5%E5%BF%97%E4%BF%A1%E6%81%AF.png?raw=true)



### 解决办法：使用nginx代理后，获取用户真实ip，则需要在nginx配置文件中，设置`X-Forwarded-For`

```nginx
server {
    listen 80;
    listen 443 ssl;
    server_name xxx.xxxxx.com;
    #ssl
    ssl_certificate      /etc/nginx/xxxx/xxx.pem;
    ssl_certificate_key  /etc/nginx/xxxx/xxx.key;
    location / {
        proxy_pass http://127.0.0.1:8000;
        #Proxy Settings;
        #proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header   X-Real-IP        $remote_addr;
        proxy_set_header   X-Forwarded-For  $remote_addr;
    }
}
```

然后重启Nginx服务。