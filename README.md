# simplePingmesh
实现一个简单的pingmesh
- 预先安装软件
    ```
    sudo pip install pandas
    ```
    ```
    sudo pip install seaborn
    ```
    ```
    sudo pip install statsmodels
    ```

- 配置pinglist

  `pinglist.txt` 中写了所有服务器的IP地址，pingmesh运行的时候，会根据pinglist的内容，服务器两两之间通信测试RTT。

- 运行main

  执行如下命令生成数据

  ```
  bash main.sh
  ```

  生成的数据存在result文件夹下，result文件夹中以数字n为名称的子文件夹下，存放的是第n对测试的结果。所有的结果以json格式记录。

- 产生可视化结果

  ```
  python visual.py
  ```

  由于程序在4个不同的时间片上记录了4次RTT结果，所以需要选择一个你想查看哪一个时间片上的结果。

- 清理过程文件

  我们提供了垃圾清理脚本，用于清除在simplePingmesh运行过程中，在每一台服务器上生成的结果数据

  ```
  bash clear.sh
  ```

- 即将要做的
    - 写一个配置文件，轮询多少次从配置文件里读取
    首先有一个在各台机器安装Mysql数据库的脚本
    - 将数据存储到MySQL中(ok)
    - C++ 中使用MySQL，需要用到[MySQL++](https://www.cnblogs.com/zhxilin/p/5897211.html)
    - [python MySQL](https://www.runoob.com/python/python-mysql.html)
- 未解决的
    - `sql.py` 未解决重复插入的问题，多次运行`sql.py `会重复插入数据

- [C++读写配置文件](https://blog.csdn.net/jixuxiangqianzou/article/details/9070147)

- 安装`pip install MySQL-python`的时候出现错误，需要先进行下面的安装操作
    `sudo apt-get install libmysqld-dev`

- [Ubuntu 上安装MySQL](https://zhuanlan.zhihu.com/p/64080934)
- [创建新的普通用户](https://blog.csdn.net/sicongfu/article/details/51499050) 注意最后几段的操作，需要在root里建database，然后创建新的账户对root里的database有增删查改的操作
    - [删除用户等其他操作](https://blog.csdn.net/u014453898/article/details/55064312)
    - [查看所有用户](https://blog.csdn.net/qq_37996815/article/details/78934536)
    - [MySQL在Ubuntu上的一些操作](https://www.cnblogs.com/zhuyp1015/p/3561470.html)