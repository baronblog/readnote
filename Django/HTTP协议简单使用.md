### HTTP协议知识点



<br/>
#### 什么是HTTP协议
http是一个简单的请求-响应协议，它通常运行在TCP之上。它指定了客户端可能发送给服务器什么样的消息以及得到什么样的响应。请求和响应消息的头以ASCII码形式给出；而消息内容则具有一个类似MIME的格式。这个简单模型是早期Web成功的有功之臣，因为它使得开发和部署是那么的直截了当，参考自[百度百科-HTTP协议](https://baike.baidu.com/item/http/243074?fromtitle=HTTP%E5%8D%8F%E8%AE%AE&fromid=1276942&fr=aladdin)


<br/>
#### 开发中的具体应用
* 模拟HTTP数据：有时候，我们可能需要模拟发送HTTP数据给其他服务，但是又没有现成的框架，即可以自己拼接成HTTP协议的数据发送给Web服务器或者浏览器，以Django中的HttpResponse为例，其中的serialize函数其实就是拼接成HTTP协议的格式发送给uWSGI。
    ```
    class HttpResponse(HttpResponseBase):
    """
    An HTTP response class with a string as content.

    This content that can be read, appended to or replaced.
    """

    streaming = False

    def __init__(self, content=b'', *args, **kwargs):
        super(HttpResponse, self).__init__(*args, **kwargs)
        # Content is a bytestring. See the `content` property methods.
        self.content = content

    def serialize(self):
        """Full HTTP message, including headers, as a bytestring."""
        return self.serialize_headers() + b'\r\n\r\n' + self.content
    ```
<br/>

* 根据上面一点，可以得出HTTP协议数据格式是如下格式

    * 请求报文
        ```
        <method> <request-URL> <version>
        <headers>

        <entiry-body>
        ```
    * 响应报文
        ```
        <version> <status> <reason-phrase>
        <headers>

        <entiy-body>
        ```

* 节约资源的应用：主要是对请求头/响应头做处理
    * 请求头/响应头中开启Keep Alive
    * 开启压缩模式
    * 留坑待写
