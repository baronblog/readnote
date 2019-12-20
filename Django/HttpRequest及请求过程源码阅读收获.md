### HttpRequest及请求过程源码阅读收获


#### 什么是request

* request是django视图函数中必须传递的第一个参数，也可以不写成requests，写成其他值也可以，毕竟这个就是一个参数名
* request包含了一些uWSGI协议服务端传过来的一些请求信息等




#### requets是怎么做的

* request实际是WSGIRequest是该类的实例化对象，接收uWSGI协议传过来的envir参数，获取相关信息，比如说编码，请求路径等
    ```
    class WSGIRequest(http.HttpRequest):
    def __init__(self, environ):
        script_name = get_script_name(environ)
        path_info = get_path_info(environ)
        if not path_info:
            path_info = '/'
        self.environ = environ
        self.path_info = path_info
        self.path = '%s/%s' % (script_name.rstrip('/'),
                               path_info.replace('/', '', 1))
        self.META = environ
        self.META['PATH_INFO'] = path_info
        self.META['SCRIPT_NAME'] = script_name
        self.method = environ['REQUEST_METHOD'].upper()
        _, content_params = cgi.parse_header(environ.get('CONTENT_TYPE', ''))
        if 'charset' in content_params:
            try:
                codecs.lookup(content_params['charset'])
            except LookupError:
                pass
            else:
                self.encoding = content_params['charset']
        self._post_parse_error = False
        try:
            content_length = int(environ.get('CONTENT_LENGTH'))
        except (ValueError, TypeError):
            content_length = 0
        self._stream = LimitedStream(self.environ['wsgi.input'], content_length)
        self._read_started = False
        self.resolver_match = None
    ```

* 大致请求顺序如下：(该流程只会包含操作，目前不包含导包，设置环境变量等比较细的流程)

    * uWSGI协议server通过wsgi调用get_wsgi_application, 然后该函数调用WSGIHandlerg该类，该类因为有__call__魔法方法，即使是类也可以调用
    
    * 首先申请一把线程锁，然后加载中间件的时候调用该锁，意味着即使使用uWSGI同一个进程下面的2个线程同时服务，加载中间件的时候只能有一个线程在操作，另外多个线程就只能等待这把锁的释放，这里使用了with的方法，可以自动释放锁

    * 加载中间件出了错误直接就是raise，没有做容错处理

    * 然后把uWSGI协议传过来的environ参数传入WSGIRequestl类，实例化成我们常见的request

    * 然后就是获取[response](https://github.com/yangyang510/readnote/blob/master/Django/HttpResponse%E6%BA%90%E7%A0%81%E9%98%85%E8%AF%BB.md)

    * 获取response中有一个匹配路由的过程，也有一个执行中间件的过程，留坑，待写。

    * 获取response后再返回

    
    
