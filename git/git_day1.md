 > Author: 陈伦巨
 >
 > Data: 2019-07-19
 >
 > Email: 545560793@qq.com
 >
 > github: https://github.com/smartisantt



## 一、Git简介



##### 1、最重要的问题，Git是什么？

Git是目前世界上最先进的分布式版本控制系统（没有之一）。

什么是版本控制系统？如果你用Microsoft Word写过毕业论文，你就明白Git的重要性。

Microsoft Word想找到之前删除的文字，通过撤销只能是有限的次数，如果保存后然后打开再想看上次删除的文字就很困难。你可能会想到复制一个相同文件然后再在复制出来的文件上更改，然后就会有很多word文档，每个文档具体改变了什么时间久了也会忘记。你的文档会交给老师更改，然后发给你，你再更改。

重点来了：

于是你想，如果有一个软件，不但能自动帮我记录每次文件的改动，还可以协作编辑，这样就不用自己管理一堆类似的文件了，也不需要把文件传来传去。



##### 2、Git的诞生

Git的作者是 Linus Torvalds（林纳斯·托瓦兹，同时也是 Linux 之父）

1969 年，Linus Torvalds 生于芬兰一个知识分子家庭。父亲 Nils Torvalds 毕业于赫尔辛基大学，是一名活跃的电台记者。母亲 Anna Torvalds 同样毕业于赫尔辛基大学，也是一名记者。有趣的是，他的祖父奥 Ole Torvalds 也是一名记者。除此之外，**Torvalds 的外祖父 Leo Tornqvist 是芬兰第一批统计学教授**。优秀的家庭背景为 Torvalds 奠定了接受良好教育的基础。**Torvalds 在 11 岁时，应其外祖父要求用 BASIC 语言编写一些统计学方面的小程序**。大众普遍认为，这是他编程经历之始。

在 git 诞生之前，Torvalds 选择使用 BitKeeper 进行 Linux 版本管理。后来与Bitkeeper没有合作，Torvalds花了两周时间自己用C写了一个分布式版本控制系统，这就是Git！Git迅速成为最流行的分布式版本控制系统，尤其是2008年，GitHub网站上线了，它为开源项目免费提供Git存储，无数开源项目开始迁移至GitHub。



## 二、安装Git

##### 1、在Mac OS X上安装Git

安装homebrew，然后通过homebrew安装Git，具体方法请参考homebrew的文档：<http://brew.sh/>。

##### 2、在Windows上安装Git

在Windows上使用Git，可以从Git官网直接[下载安装程序](https://git-scm.com/downloads)

##### 3、Centos安装Git

`yum install git`

##### 4、Ubuntu 安装Git

`sudo apt-get install git



安装完成后，还需要最后一步设置，在命令行输入：

```
$ git config --global user.name "Your Name"
$ git config --global user.email "email@example.com"
```





## 三、名词解释



![](D:\python-100days\Python-100days\git\res\bg2015120901.png)

- Workspace：工作区，就是你平时存放项目代码的地方
- Index / Stage：暂存区，用于临时存放你的改动，事实上它只是一个文件，保存即将提交到文件列表信息
- Repository：仓库区（或版本库），就是安全存放数据的位置，这里面有你提交到所有版本的数据。其中HEAD指向最新放入仓库的版本
- Remote：远程仓库，托管代码的服务器，可以简单的认为是你项目组中的一台电脑用于远程数据交换



文件的四种状态：

**Untracked**: 未跟踪, 此文件在文件夹中, 但并没有加入到git库, 不参与版本控制. 通过git add 状态变为Staged。

**Unmodify**：文件已经入库, 未修改, 即版本库中的文件快照内容与文件夹中完全一致. 这种类型的文件有两种去处, 如果它被修改, 而变为Modified。

**Modified:** 文件已修改, 仅仅是修改, 并没有进行其他的操作. 这个文件也有两个去处, 通过git add可进入暂存staged状态, 使用git checkout 则丢弃修改过,返回到unmodify状态, 这个git checkout即从库中取出文件, 覆盖当前修改。

**Staged:** 暂存状态. 执行git commit则将修改同步到库中, 这时库中的文件和本地文件又变为一致, 文件为Unmodify状态. 执行git reset HEAD filename取消暂存,文件状态为Modified



新建文件--->Untracked

使用add命令将新建的文件加入到暂存区--->Staged

使用commit命令将暂存区的文件提交到本地仓库--->Unmodified

如果对Unmodified状态的文件进行修改---> modified

如果对Unmodified状态的文件进行remove操作--->Untracked