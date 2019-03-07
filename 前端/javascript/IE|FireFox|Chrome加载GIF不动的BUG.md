### 记录GIF在三个浏览器不能正常加载的处理方法

#### Chomre
* 不管怎么做，Chrome是支持的做好的，一般不用考虑

### IE
* IE如果不做处理，GIF图会静止到某一帧
* IE做的处理就是删除掉当前img标签，重新生成img标签，或者重新更换src对象内容，先把src更换为空字符串，然后再重新插入GIF图即可
```
$("#id").attr("src","");
$("#id").attr("src","/static/a.gif");
```


### FireFox
* IE做了处理是不能兼容FireFox的，必须重新做处理
* 首先需要先把加载GIF的html代码加载出来，然后延迟0.1毫秒(具体效果自己把控)，然后做跟IE一样的操作即可解决
```
$("#id").css("display","block");
setTimeout(function (){
    $("#id").attr("src","");
    $("#id").attr("src","/static/a.gif");
}
,100)
```

### 总结
* 前端其实不难，难的是耐心，如果可以一直调试下去，再多开动脑筋，即使是再难得兼容性问题也可以解决
