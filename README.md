# simplePingmesh
实现一个简单的pingmesh

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

