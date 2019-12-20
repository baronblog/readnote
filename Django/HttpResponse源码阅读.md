### HttpResponse源码阅读收获



#### HttpResponse作用
* 传递一个HttpResponse对象给uWSGI协议，然后该协议解析该对象，获取到传递给前端的HTTP协议数据
  * HttpResponse对象中有多个字段分别保存HTTP协议数据，比如说content保存的就是byte类型的html数据，headers保存的就是头部信息
  * uWSGI 首先解析HTTP头部信息，然后协议html数据，最后按照HTTP协议拼接成对应的数据发给Web服务器
* 同理，Django中的render也是这个道理，render只是多了一步把模板，数据渲染成html字符串，然后再调用HttpResponse返回
  ```
  content = loader.render_to_string(
            template_name, context, context_instance, dirs, dictionary,
            using=using)
  ```
  
  
  #### HttpResponse是怎么做的
  * 初始化
    * 把传入的字符串赋给属性content，包括头部信息等
    * 初始化父类，给实例赋予相关属性
      ```
      super(HttpResponse, self).__init__(*args, **kwargs)
      ```
  * 属性操作：使用了property和setter的用法
    * 把content做为了一个可读属性
    * 使用setter把content作为了一个可修改属性，中间件可以对传输的字符串做修改
    
  * 自由的添加头部信息：使用了魔法方法__setitem__，__getitem__，__delitem__
    * 因为HttpResponse中是没有我们自己可以自由添加的属性的，但是我们却可以自由添加HTTP协议头部的相关信息，是因为使用了魔法方法setitem，可以自由设置键值对
    
    
