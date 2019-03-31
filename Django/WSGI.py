# coding:utf-8
"""
@目标：解析WSGI源码，该文件做为WSGI接口
@作者：louis

"""


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
    #以上表示实现最简单的WSGI，那Django呢？是如何实现WSGI的呢？留坑，等待Django源码解读再次深入理解