## 初学C语言

### 目的
* Python 很简单，只要有一点计算机编程底子的，稍微努力点，多敲一敲Python代码，我相信不用一个月便可以入门做东西，甚至更少的时间
* 目前市场上用的基本都是Cpython，所以想要把这门语言彻底学懂，C语言是避不开的，而且也不能避开
* 研究下源码，提升下自己的代码水平

### Mac 下编写C语言版本的helloworld
* 首先使用vim编写出c代码，如下：
    ```
    #include<stdio.h>
    int main(){
            printf("hello\n");
            return 0;
    }
    ```
* 使用gcc编译器编译写的c代码：gcc helloworld.c
* 调用命令执行代码：./a.out helloworld.c

### 如何阅读github上的cpython源码结构
* Include：Python提供的所有头文件(著名的python.h，缺少该文件会导致装第三方模块有问题，比如会引发gcc编译问题等，需要安装对应python版本的dev版本即可，比如说pip install python-3.6-dev即可)
* Lib：Python自带的标准库，纯python写的标准库
* Modules：标准库，用c语言写的，对速度要求非常高的库就用c来写，要求不高的就用python来写
* Parser：语法分析部分
* Objects：所有的内建对象，用c语言实现
* Python：compiler和runtime引擎部分，运行核心所在
* Mac：mac平台编译部分
* PCBuild：windows平台编译部分

### C语言格式化输出
* 如何打印格式化输出语句
    ```
    printf("该学生的年龄为：%d\n", st.age)
    ```
* 如何打印字符串
    ```
    printf("输出控制符：%s"，"xxxxx")
    ```
    
