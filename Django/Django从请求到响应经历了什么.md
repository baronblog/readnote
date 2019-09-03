## 记录关于Django请求到响应经历的过程


### 最简单请求流程
* 浏览器 > Web服务器(Nginx/Apache) > UWSGI > Django 中间件 > Django 业务实现(即App)
* 其中UWSGI是沟通Web服务器和调用业务框架的桥梁，目前我使用的Apache使用mod_wsgi模块实现UWSGI功能
* 下面代码为最简单实现的一个app, 当使用实现了UWSGI的web server来调用下面的app，就是一次较为完整的流程
```
def simplr_wsgi_app(environ, start_response):
	status = '200 OK'
	headers = [{'Content-type': 'text/plain'}]
	# 初始化响应, 必须在返回前调用
	start_response(status, headers)
	# 返回可迭代对象
	return ['hello world!']
```


### Django 完整数据流
* 用户通过浏览器请求一个页面  
* 求到达Request Middlewares，中间件对request做一些预处理或者直接response请求
	* django通过实现了wsgi协议的server端调用，会调用app，而django的app是这样封装的： application = get_wsgi_application()，调用application的时候就是application()(即get_wsgi_application()(environ,start_response)，为什么可以这样，因为WSGIServer实现了__call__方法)
	* 在初始化application的时候，会加载中间件，用列表包含，分别是视图中间件/响应/出错中间件
* URLConf通过urls.py文件和请求的URL找到相应的View  
* View Middlewares被访问，它同样可以对request做一些处理或者直接返回response  
* 调用View中的函数  
* View中的方法可以选择性的通过Models访问底层的数据  
* 所有的Model-to-DB的交互都是通过manager完成的  
* 如果需要，Views可以使用一个特殊的Context  
* Context被传给Template用来生成页面  
    a.Template使用Filters和Tags去渲染输出  
    b.输出被返回到View  
    c.HTTPResponse被发送到Response Middlewares  
    d.任何Response Middlewares都可以丰富response或者返回一个完全不同的response  
    e.Response返回到浏览器，呈现给用户 
    
    
### 总结
* django启动时，启动了一个WSGIserver以及为每个请求的用户生成一个handler
* 理解WSGI协议，并且WSGIHandler这个类控制整个请求到响应的流程，以及整个流程的基本过程
* 中间件的概念，以及每一个process_request, process_response, process_view, process_exception方法在哪个步骤发挥着什么样的作用
* 中间价的执行时有顺序的，request与view是按照顺序去执行的，而response和exception是反序的，这一步实在WSGIHandler在加载到它的各个列表的时候完成的


参考资料：
[Django请求到响应经历了什么](https://juejin.im/post/5a6c4cc2f265da3e4c080605)
