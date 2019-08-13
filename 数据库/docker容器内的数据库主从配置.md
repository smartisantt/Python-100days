> Author: 陈伦巨
>
> Data: 2019-08-12
>
> Email: 545560793@qq.com
>
> github: https://github.com/smartisantt



## MySQL主从复制原理

MySQL 主从复制默认是异步的模式。主服务器数据库的每次操作都会记录在其二进制文件mysql-bin.xxx（该文件可以在mysql目录下的data目录中看到）中，从服务器的I/O线程使用专用账号登录到主服务器中读取该二进制文件，并将文件内容写入到自己本地的中继日志relay-log文件中，然后从服务器的SQL线程会根据中继日志中的内容执行SQL语句

其中Master负责写操作的负载，也就是说一切写的操作都在Master上进行，而读的操作则分摊到Slave上进行。这样一来的可以大大提高读取的效率。

使用场景：

- 读写分离
- 数据实时备份
- 架构扩展



## 基于docker的Mysql主从复制

首先拉取docker镜像，这个默认是最新的版本。

```
docker pull mysql
```

查看Mysql的版本信息：

![](https://github.com/smartisantt/Python-100days/blob/master/%E6%95%B0%E6%8D%AE%E5%BA%93/res/1565597202(1).jpg?raw=true)



然后使用此镜像启动容器，这里需要分别启动主从两个容器



#### Master数据库（主）：

`docker run -p 8037:3306 --name mastermysql -v /root/mysql/mastermysqldata:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=123456 -d mysql`



#### Slaves数据库（从）：

`docker run -p 8036:3306 --name slavemysql -v /root/mysql/slavemysqldata:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=123456 -d mysql`



说明：主数据库对外映射的是8037端口，从数据库对外映射的是8036端口。



使用Navicat连接数据库，出现如下错误（看对应的IP和端口是否输入正确，如果是阿里云则是否开启了此端口）

![](https://github.com/smartisantt/Python-100days/blob/master/%E6%95%B0%E6%8D%AE%E5%BA%93/res/1565597815(1).jpg?raw=true)

如果是以下错误：

![](https://github.com/smartisantt/Python-100days/blob/master/%E6%95%B0%E6%8D%AE%E5%BA%93/res/1565598919(1).jpg?raw=true)

解决方案如下：

```
# 如用 Navicat 远程连接Docker容器中的mysql 报错：1251 - Client does not support authentication protocol 解决办法如下。
# 对远程连接进行授权
grant all privileges on *.*  to 'root'@'%'; 
# 更改密码的加密规则
ALTER USER 'root'@'%' IDENTIFIED BY 'password' PASSWORD EXPIRE NEVER;
# 更改root的密码
ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY '123456'; 
# 刷新权限
flush privileges; 
```



#### 配置Master（主）

通过`docker exec -it mastermysql /bin/bash`命令进入到Master容器内部，

`cd /etc/mysql`切换到/etc/mysql目录下，然后`vi my.cnf`对my.cnf进行编辑。此时会报出`bash: vi: command not found`，需要我们在docker容器内部自行安装vim。

##### 安装vim：

执行`apt-get update`，然后再次执行`apt-get install vim`即可成功安装vim

在my.cnf中添加如下配置：

```
[mysqld]
## 同一局域网内注意要唯一
server-id=100  
## 开启二进制日志功能，可以随便取（关键）
log-bin=mysql-bin
# 修改数据库的时区
default-time-zone = '+8:00'
```



配置完成之后，需要重启mysql服务使配置生效。`docker restart mastermysql`启动容器

下一步在Master数据库创建数据同步用户，授予用户 slave REPLICATION SLAVE权限和REPLICATION CLIENT权限，用于在主从库之间同步数据。



```
CREATE USER 'slave'@'%' IDENTIFIED WITH mysql_native_password BY '123456';
GRANT REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'slave'@'%';
```





#### 配置Slave(从)

和配置Master(主)一样，在Slave配置文件my.cnf中添加如下配置：

```
[mysqld]
## 设置server_id,注意要唯一
server-id=101  
## 开启二进制日志功能，以备Slave作为其它Slave的Master时使用
log-bin=mysql-slave-bin   
## relay_log配置中继日志
relay_log=edu-mysql-relay-bin 
# 修改数据库的时区
default-time-zone = '+8:00'
```



#### 链接Master(主)和Slave(从)

在Master进入mysql，执行`show master status;`

![](https://github.com/smartisantt/Python-100days/blob/master/%E6%95%B0%E6%8D%AE%E5%BA%93/res/1565596510(1).png?raw=true)

File和Position字段的值后面将会用到，在后面的操作完成之前，需要保证Master库不能做任何操作，否则将会引起状态变化，File和Position字段的值变化。

##### 在Slave 中进入 mysql，执行

```
change master to master_host='39.105.49.244', master_user='slave', master_password='123456', master_port=8037, master_log_file='mysql-bin.000001', master_log_pos= 1799;
```



在Slave 中的mysql终端执行`show slave status \G;`用于查看主从同步状态。

![](https://github.com/smartisantt/Python-100days/blob/master/%E6%95%B0%E6%8D%AE%E5%BA%93/res/1565596812(1).jpg?raw=true)



正常情况下，SlaveIORunning 和 SlaveSQLRunning 都是No，因为我们还没有开启主从复制过程。使用`start slave`开启主从复制过程，然后再次查询主从同步状态`show slave status \G;`。



正常情况如下：SlaveIORunning 和 SlaveSQLRunning 都是Yes，说明主从复制已经开启。此时可以测试数据同步是否成功。

![](https://github.com/smartisantt/Python-100days/blob/master/%E6%95%B0%E6%8D%AE%E5%BA%93/res/1565596599(1).jpg?raw=true)





如果出现	

![](https://github.com/smartisantt/Python-100days/blob/master/%E6%95%B0%E6%8D%AE%E5%BA%93/res/1565596709(1).jpg?raw=true)

使用`start slave`开启主从复制过程后，如果SlaveIORunning一直是Connecting，则说明主从复制一直处于连接状态，可以看到报错信息。

创建用户时：

```

# CREATE USER 'slave'@'%' IDENTIFIED BY '123456';  输入这句就会报错，正确如下：
CREATE USER 'slave'@'%' IDENTIFIED WITH mysql_native_password BY '123456';
```



如果都配置正确：

在Master中创建一个数据库，则在从数据库中则可以看到。



**在master上删除一条记录，而slave上找不到，则会报错**

```
Last_SQL_Error: Could not execute Delete_rows event on table master.t1; Can't find record in 't1', Error_code: 1032; handler error HA_ERR_KEY_NOT_FOUND; the event's master log mysql-bin.000001, end_log_pos 3735
```

解决方法：master要删除一条记录，而slave上找不到报错，这种情况主都已经删除了，那么从机可以直接跳过。

```mysql
stop slave;
set global sql_slave_skip_counter=1;
start slave;
```

##### MySQL主从同步报错故障处理记录可以参考：<https://blog.51cto.com/hujiangtao/1932166>

