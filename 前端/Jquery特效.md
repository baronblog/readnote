## 收集一些在刚学编程之前不理解的js内容




### 点击出现下面选项
思路：如果网页禁用掉js，将会展示实现效果的页面，需要用js把需要隐藏的html代码删掉，如果点击了按钮，再把相应的html代码插入即可。


### 点击出现模态框
思路：采用的是bootstrap的插件，把写好的模态框代码放到html中，然后给模态框绑定id，通过id绑定事件，如果点击触发了这个事件，便展示这个模态框即可。


### [生成树形结构](https://www.cnblogs.com/AutumnRhyme/p/5915769.html)
思路：使用zTree插件实现相关功能，首先需要定义zTree的相关设置值，值里面需要体现树关系，然后在html页面引用zTree的js和css，之后声明变量，之后调用zTree
方法，把相关设置参数传进去即可


### js全局变量和局部变量问题
思路：如果变量声明在函数外面就是全局变量，如果在函数内部就是局部变量。

```
var a = 10;
function test(){
    a = 100;
    console.log(a);
    console.log(this.a);
    var a;
    console.log(a);
}
test();
```

### 解题思路
第一个打印为100，第二个打印10，第三个打印100.js在执行前都会对变量做完整分析，从而确定变量的作用域。在执行前，会确定一个全局变量a，test函数内部也会确定
一个局部变量a

```
var a = 100;
function test(){
    console.log(a);
    var a = 10;
    console.log(a);
}
test();
```

### 解题思路
第一个打印undefind，第二个打印10，因为虽然js在执行前会对变量做完整分析，但是不会定义，所以第一个打印为undefind，第二个在定义局部变量a后打印自然为10


```
var a = 100;
function test(){
    console.log(a);
    a = 10;
    console.log(a);
}
test();
console.log(a);
```

### 解题思路
第一个打印全部变量a，为100，第二个打印全部变量10，最后一个打印10。如果函数内部不使用var声明变量，就是全部变量
