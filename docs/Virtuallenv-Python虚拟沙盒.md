## Virtuallenv-Python虚拟沙盒

---

### 安装

> pip install virtualenv

### 创建虚拟环境

> virtualenv test_env
>
> 这个过程会将setuptools,pip等基本的工具库卡拷贝到新环境中，
>
> 注意：默认清晰下，虚拟环境会依赖系统环境中的site packages，就是说系统中安装好的第三方package也会安装在虚拟环境中，如果不想依赖这些库，可以加上参数` --no-site-packages`

创建成功后会在当前目录下生成对应的目录文件，其中包含/bin,/include,/lib等目录

### 启动虚拟环境

> 进入上一步创建的虚拟环境目录，然后执行`source ./bin/active` 激活该虚拟环境，然后后面所有的工作都是在虚拟环境中进行的

### 退出虚拟环境

> deactivate

### 删除虚拟环境

> 只需要删除创建时候的目录即可



:grey_question:virtualenv创建的虚拟环境是Python2的还是Python3的？

使用的pip是哪个环境的，安装的Virtualenv就是哪个环境的，比如是pip是python2.7下的，则Virtualenv是也python2.7



## 参考

[virtualenv -- python虚拟沙盒](http://www.cnblogs.com/tk091/p/3700013.html)

