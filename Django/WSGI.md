## WSGI 相关知识


### 什么是WSGI
* WSGI 是一种协议，该协议规定了Web服务器和业务框架之间是如何交流的，具体实现该协议的由Apache的mod_wsgi模块/uWSGI/gunicorn
* 要实现WSGI协议，必须实现web server和web application两部分才行
* web server端要履行的义务
    * 接收/响应HTTP请求
    * 准备调用application时的environ和start_response参数
    * 组织响应头/响应体返回给客户端
* web application端要履行的义务
    * 接收server端发过来的数据，并按照一定逻辑处理后返回结果


```
#在Python PEP333中定义了WSGI接口标准，最简单的函数实现如下
def application(environ,start_response):
    '''
    #接口接收两个参数，
    #environ：一个包含所有的HTTP请求信息的dict对象，包括所有的HTTP信息，里面有相关的html
    #start_response：一个发送HTTP响应的函数，里面包含相应的内容，状态吗，相应的头部内容
    '''
    status ='200 OK'
    response_headers = [('Content-type','text/html;charset=utf-8')]
    start_response(status, response_headers)
    return ['你好，世界']



if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('127.0.0.1',8002,application)
    print("serving http on port 8002")
    httpd.serve_forever()
```




#### 参考资料
* [WSGI协议的作用和实现原理详解](https://www.cnblogs.com/wangcoo/p/10018373.html)
