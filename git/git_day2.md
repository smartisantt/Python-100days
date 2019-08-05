> Author: 陈伦巨
>
> Data: 2019-08-05
>
> Email: 545560793@qq.com
>
> github: https://github.com/smartisantt



## 一、Git命令

#### 分支相关命令

| 命令                             | 说明                               |
| -------------------------------- | ---------------------------------- |
| `git branch`                     | 列出本地所有分支                   |
| `git branch -r`                  | 列出所有远程分支                   |
| `git branch -a`                  | 列出所有本地分支和远程分支         |
| `git branch [branch_name]`       | 新建一个分支，但依然停留在当前分支 |
| `git checkout -b [branch_name]`  | 新建一个分支，并切换到该分支       |
| `git checkout -`                 | 切换到上一个分支                   |
| `git branch -d [branch_name]`    | 删除指定分支                       |
| `git branch -dr [remote/branch]` | 删除远程分支                       |



#### 本地分支和远程分支的映射关系

| 命令                                            | 说明                             |
| ----------------------------------------------- | -------------------------------- |
| `git branch -vv`                                | 查看本地和远程分支的映射关系     |
| `git branch --set-upstream-to [remote][branch]` | 建立当前分支与远程分支的映射关系 |
| `git branch -u [remote][branch]`                | 建立当前分支与远程分支的映射关系 |
| `git branch --unset-upstream`                   | 撤销本地分支与远程分支的映射关系 |

#### 同步命令

| 命令                         | 说明                                 |
| ---------------------------- | ------------------------------------ |
| `git fetch [remote]`         | 下载远程仓库的所有变动               |
| `git remote -v`              | 显示所有远程仓库                     |
| `git pull [remote] [branch]` | 取回远程仓库的变化，并与本地分支合并 |
| `git push [remote] [branch]` | 上传本地指定分支到远程仓库           |

#### 远程操作

| 命令                             | 说明                     |
| -------------------------------- | ------------------------ |
| `git clone <版本库的网址>`       | 从远程主机克隆一个版本库 |
| `git remote`                     | 列出所有远程主机         |
| `git remote -v`                  | 参看远程主机的网址       |
| `git remote add <主机名> <网址>` | 添加远程主机             |
| `git remote rm <主机名>`         | 删除远程主机             |

#### 查看信息

| 命令         | 说明                             |
| ------------ | -------------------------------- |
| `git status` | 显示工作目录和暂存区的状态       |
| `git log`    | 显示项目历史的信息               |
| `git diff`   | 修改之后还没有暂存起来的变化内容 |
|              |                                  |
|              |                                  |





## 二、使用场景

#### 场景一：本地有项目，并且已经更新过版本。需要关联远程仓库

新建一般本地仓库和远程仓库关联（如果创建远程仓库时勾选了创建README.md，则需先创建一个README.md文档）

```
echo "# test" >> README.md
git init
git add README.md
git commit -m "first commit"
git remote add origin https://github.com/smartisantt/test.git
git push -u origin master
```

或者把已经存在的本地仓库和远程仓库关联起来

```
git remote add origin https://github.com/smartisantt/test.git
git push -u origin master
```



#### 场景二：没有本地仓库只有远程仓库

先进入你打算保存项目的目录下，`git clone <url>` - 将服务器上的项目(仓库)克隆



#### 合并冲突：

现在有两个分支master和dev，分别对文件a.txt做出修改，当在master分支上合并dev分支时，出现冲突

```
$ git merge dev
Auto-merging a.txt
CONFLICT (content): Merge conflict in a.txt
Automatic merge failed; fix conflicts and then commit the result.
```

a.txt文件中的冲突

```
<<<<<<< HEAD
master add this line!!
=======
dev add this line
>>>>>>> dev
```

在工作中，需要和你的同伴商量。接下来我们需要手动去修改它。

```
master and dev both add this line!!
```

然后`git add .`，`git commit`，就解决了冲突。注意：此时我们是在master上对a.txt文件做修改，修改的内容并不会影响到dev分支的a.txt文件中的内容。