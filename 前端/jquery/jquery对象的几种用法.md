### Jquery对象的几种用法

#### 属性选择器
* 帮助我们获取DOM元素或者更改DOM元素，包括节点和元素
```
<h1 style="display:none">hello world</h1>

<script>
$("h1").css("display","block");
</script>

```


#### 函数
* 当传进去是一个函数的时候，则在document对象上绑定一个ready事件，当DOM结构加载完成后便执行
* 以下传入js匿名函数
```
$(function () {
       alert("DOM节点已经加载完毕");
})

$(document).ready(function (){
        alert("DOM节点已经加载完毕");
})
```


