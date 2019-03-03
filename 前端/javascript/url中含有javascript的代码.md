### URL中含有Javascript代码

#### 链接中含有#
* href标签中带有#，表示回到页面顶部
```
<a href="#">hello world</a>
```

### 链接中是空白字符串
* href是空白字符串代表刷新当前页面
```
<a href="">hello world</a>
```

### 链接中含有#id名或者name名
* 代表跳转到id那部分或者到name属性那块
```
<a href="#id">hello world</a>
```

### 链接中含有url链接
* 代表跳转到相应的url
```
<a href="https://www.baidu.com">hello world</a>
```

### 链接中含有Javascript代码
* 如果其中的javascript没有返回值，就执行相应的函数
* 如果其中的javascript有返回值，就会用返回值代替新的页面内容

```
#不推荐写法
<a href="javascript:alert('xxx');">hello world</a>

#推荐写法
<a href="javascript:void(0);" onclick="alert('xxx')">hello world</a>
```