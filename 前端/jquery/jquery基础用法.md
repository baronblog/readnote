### 记录jquery基础选择用法


#### 基本选择器
* $("#louis")：选取id为louis的元素，选取到了便可以对该对象进行操作，比如添加颜色，可见不可见等
```
$(#louis).css("display","none");
```

#### 层次选择器
* 选择div里面所有span元素：$("div span")
* 选取div下元素名是span的子元素：$("div > span")
* 选取div后面紧跟着的br标签：$("div+br")


#### 过滤选择器
* 选取id为louis中第一个div：$("#louis div:frist")
* 选取当前所选元素获取焦点的元素：$("#louis :foucus")


#### 内容过滤选择器
* 选取含有子元素的div：$("div:parent")


#### 属性过滤选择器
* 选取拥有属性id的div元素：$("div[id]")
* 选取div中title为louis的元素：$("div[title=louis]")
* 
