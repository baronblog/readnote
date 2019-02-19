## 记录JS和Jquery如何获取相关的值


### val 用法
如果直接就是val，会直接获取input元素的value的值；
如果在val添加了值，就会把之前的值设置为val里面的值。

```
<html>
<head>
<script type="text/javascript" src="/jquery/jquery.js"></script>
<script type="text/javascript">
$(document).ready(function(){
  $("button").click(function(){
    $(":text").val("Hello Kitty");
    alert($(":text").val());
  });
});
</script>
</head>
<body>
<p>Name: <input type="text" name="user" value="Hello World" /></p>
<button>改变文本域的值</button>
</body>
</html>

```

### show和hide用法
如果使用hide的话，就会把选中标签内的html代码全部隐藏，
如果使用show的话，就会把之前hide隐藏的代码恢复

