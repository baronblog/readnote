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




### WSGI Server端实现代码(以下思路为自己思路，尚未验证)
* 每次请求或者是每次会话都是同一个实例，在调用application的时候，把self.start_response当做参数传入，然后根据框架传入的状态码和头部信息修改实例的信息即相当于这个回调函数已经在这里返回了一些信息
* 最后等框架处理完成后返回response即可

```
# 重点关注逻辑
                # 准备一个字典，里面存放需要传递给web框架的数据
                env = dict()
                # ----------更新---------
                env['PATH_INFO'] = file_name  # 例如 index.py（模拟请求信息）
                
                # 重点关注逻辑
                # 服务器调用框架中实现的application函数,并将包含请求信息的字典和获取响应头的函数传入
                response_body = self.application(env, self.start_response)
​
                
                # 合并header和body（响应客户端的请求，这个逻辑不用关注）
                response_header = "HTTP/1.1 {status}\r\n".format(status=self.headers[0])
                response_header += "Content-Type: text/html; charset=utf-8\r\n"
                response_header += "Content-Length: %d\r\n" % len(response_body.encode("utf-8"))
                for temp_head in self.headers[1]:
                    response_header += "{0}:{1}\r\n".format(*temp_head)
​
                response = response_header + "\r\n"
                response += response_body
​
                client_socket.send(response.encode('utf-8'))
​
    # 重点关注逻辑
    # server端实现了start_response函数的定义
    def start_response(self, status, headers):
        """这个方法，会在 web框架中被默认调用"""
        response_header_default = [
            ("Data", time.time()),
            ("Server", "ItCast-python mini web server")
        ]
​
        # 将状态码/相应头信息存储起来
        # [字符串, [xxxxx, xxx2]]
        self.headers = [status, response_header_default + headers]

```

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
