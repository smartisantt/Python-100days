 

#### Docker简介

[Docker](https://docs.docker.com/)属于对Linux容器技术的一种封装（利用了Linux的namespace和cgroup技术），它提供了简单易用的容器使用接口，是目前最流行的 Linux 容器解决方案。Docker将应用程序与该程序的依赖打包在一个文件里面，运行这个文件，就会生成一个虚拟容器。程序在这个虚拟容器里运行，就好像在真实的物理机上运行一样。有了Docker就再也不用担心环境问题了。

目前，Docker主要用于几下几个方面：

1. 提供一次性的环境。
2. 提供弹性的云服务（利用Docker很容易实现扩容和收缩）。
3. 实践微服务架构（隔离真实环境在容器中运行多个服务）。



#### 镜像和容器

- 容器是运行镜像后产生的
- 镜像是一个包含所有需要运行的文件组成的包，比如代码、可运行文件、库、环境变量和配置文件等。

查看运行的容器命令：

`docker ps`

#### 容器和虚拟机的区别

容器和普通进程一样直接在主机操作系统上运行，不占用更多的资源

虚拟机直接模拟一个虚拟操作系统，程序最后实在虚拟操作系统里面运行，占用过多的资源





#### 使用 yum 安装（CentOS 7下）[官网教程](https://docs.docker.com/install/linux/docker-ce/centos/)

Docker 要求 CentOS 系统的内核版本高于 3.10 ，查看本页面的前提条件来验证你的CentOS 版本是否支持 Docker 。

通过 `uname -r `命令查看你当前的内核版本

```
[root@iz2zedqzq67rmtoql43bqvz ~]# uname -r
3.10.0-957.12.2.el7.x86_64
```

删除老版本的docker

```
$ sudo yum remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-engine
```



安装一些必要的系统工具：

`sudo yum install -y yum-utils device-mapper-persistent-data lvm2`

添加软件源信息

```
![docker_hello_world](D:\python-100days\Python-100days\docker\res\docker_hello_world.png)sudo yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
```

更新yum缓存

```
sudo yum makecache fast
```

安装 Docker-ce

```
sudo yum -y install docker-ce
```

测试运行 hello-world

```
[root@iz2zedqzq67rmtoql43bqvz ~]# docker run hello-world
```

![测试运行 hello-world](https://github.com/smartisantt/Python-100days/blob/master/docker/res/docker_hello_world.png?raw=true)

由于本地没有hello-world这个镜像，所以会下载一个hello-world的镜像，并在容器内运行。



#### 删除Docker CE

```
$ sudo yum remove docker-ce
$ sudo rm -rf /var/lib/docker
```





#### 常用命令

| 命令               | 说明                                   |
| :----------------- | :------------------------------------- |
| **docker images**  | 列出本地镜像                           |
| **docker rmi**     | 删除本地一个或多少镜像                 |
| **docker version** | 显示 Docker 版本信息                   |
| **docker info**    | 显示 Docker 系统信息，包括镜像和容器数 |
| **docker search**  | 从Docker Hub查找镜像                   |
| **docker pull**    | 从镜像仓库中拉取或者更新指定镜像       |
| **docker run**     | 创建一个新的容器并运行一个命令         |
| **docker ps**      | 列出容器                               |
| **docker attach**  | 连接到正在运行中的容器                 |
| **docker rm**      | 删除一个或多少容器                     |
| **docker build**   | 使用 Dockerfile 创建镜像               |
| **docker start**   | 启动一个或多个已经被停止的容器         |
| **docker stop**    | 停止一个运行中的容器                   |



Docker安装mysql

```
# 安装最新的mysql
docker pull mysql
# 运行
docker run -itd -p 3306:3306 --name test_mysql -v /root/mysqlData:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=hbb123 mysql
# 进入
docker exec -it test_mysql mysql -uroot -p
```

Docker安装redis

```
# 安装
docker pull redis
# 运行
docker run -p 6379:6379 --name=test_redis -v /root/redisData:/data -d redis redis-server --appendonly yes --requirepass 'hbb123'
# 进入redis
docker exec -it test_redis redis-cli
```

安装Python

 ```
docker pull python:3.6
 ```



Dockfile 配置

```
FROM python:3.6

RUN pwd

ADD storybook_sever /storybook_sever

WORKDIR /storybook_sever

RUN pip install -r requirements.txt

EXPOSE 8000
```

注意：Dockerfile  和storybook_sever  两个文件 是同级文件。                                                                                                          `



打包Django项目

```
docker build -t story:1 . # 注意： 最后的那个点不能少
docker images # 查看打包好的镜像

docker run -it -p 8000:8000 --name story -v /root/storyData:/app story:1 python manage.py runserver 0.0.0.0:8000

```



