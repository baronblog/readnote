## 解读关于free命令的相关参数


### free命令详解
* free命令是查看Linux系统中空闲，已用物理内存以及交换内存，以及被内核使用buffer
* 命令格式：
  ```
  free [参数]
  -b  以Byte为单位显示内存
  -k  以KB为单位显示内存
  -m  以MB为单位显示内存
  -g  以GB为单位显示内存
  -o 不显示缓冲区相关数据
  
  
  total 总共多少物理内存
  used  已经使用了多少内存
  free  还剩下多少可以使用的内存
  shared 多个进程共享的内存总额
  Buffers/cached  磁盘缓存
  系统可用内存 = free内存 + buffers + cached
  ```
