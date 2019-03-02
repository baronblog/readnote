### Shell 入门

#### 什么是Shell
* 一般在程序员来说，shell就是shell脚本，是一种可以和Linux打交道的语言，学习好这门语言可以帮助我们做很多事情。

### 初次使用
#### 变量
* 和其他语言一样，比如说louis="yang"
* 变量名和等号之间不能有空格
* 使用变量就是$louis即可
* 可以使用readonly让变量成为只读变量，只读变量的值不能修改，修改会报错
* 使用unset louis删除变量，删除变量后再次打印变量将会没有任何输出

#### 字符串
* 字符串可以用单引号，也可以用双引号，也可以什么也不用，但一般来说为了友好度，一般会使用引号
* 单引号里面的任何字符会原样输出，但双引号里面可以有变量，会引用变量
* 单引号里面不能嵌套单引号，但双引号可以

#### 函数
* 可以function func(){}定义函数，也可以func(){}定义
* 函数参数不是写到括号里面，是使用$n来获取参数，当大于等于10个参数时，需要${10}才行

#### 判断语句
* 语句格式如下：
```
if condition1 then
  command
elif condition2
  command
 fi
```

#### case语句
* 语句格式如下：
```
case 值 in
模式1)
    command1
    command2
    ...
    commandN
    ;;
模式2）
    command1
    command2
    ...
    commandN
    ;;
esac
```
* 比如经典的service httpd start，中的start就是第一个参数，被case语句捕捉到了，然后调用start部分的语句完成服务的启动的
