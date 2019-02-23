## 记录关于 WebService 写法

### 简介
* WebService是一个SOA（面向服务的编程）的架构，它是不依赖于语言，不依赖于平台，可以实现不同的语言间的相互调用，通过Internet进行基于Http协议的网络应用间的交互;。
* WebService实现不同语言间的调用，是依托于一个标准，webservice是需要遵守WSDL（web服务定义语言）/SOAP（简单请求协议）规范的;
* WebService=WSDL+SOAP+UDDI（webservice的注册），Soap是由Soap的part和0个或多个附件组成，一般只有part，在part中有Envelope和Body;
* Web Service是通过提供标准的协议和接口，可以让不同的程序集成的一种SOA架构.


### WebService 优点
* 可以让异构的程序相互访问(跨平台);
* 松耦合;
* 基于标准协议（通用语言，允许其他程序访问）.

### WebService 的缺点： 
* WebService使用了XML对数据封装，会造成大量的数据要在网络中传输;
* WebService规范没有规定任何与实现相关的细节，包括对象模型、编程语言，这一点，它不如CORBA.


### WebService 的基本原理
* Service Provider采用WSDL描述服务;
* Service Provider 采用UDDI将服务的描述文件发布到UDDI服务器（Register server）;
* Service Requestor在UDDI服务器上查询并 获取WSDL文件;
* Service requestor将请求绑定到SOAP，并访问相应的服务.

### 用法(Python + Django)
* 服务端: 主要视图代码如下，在写完服务端代码后，通过url获取到WebService的接口即可
```
from soaplib.core.service import DefinitionBase, soap

class UserService(DefinitionBase):

  def getUser(self):
      user = {'name': "louis"}
      return json.dumps(user)
      
#把接口集成到django中，直接使用django来对外提供服务
from soaplib.core.server.wsgi import Application
from django.http import HttpResponse

import  StringIO
class DumbStringIO(StringIO.StringIO):
    def read(self, n):
        return self.getvalue()

class DjangoSoapApp(Application):
    def __call__(self, request):
        django_response = HttpResponse()
        def start_response(status, headers):
            status, reason = status.split(' ', 1)
            django_response.status_code = int(status)
            for header, value in headers:
                django_response[header] = value

        environ = request.META.copy()
        environ['CONTENT_LENGTH'] = len(request.raw_post_data)
        environ['wsgi.input'] = DumbStringIO(request.raw_post_data)
        environ['wsgi.multithread'] = False

        try:
            response = super(DjangoSoapApp, self).__call__(environ, start_response)
        except Exception,e:
            error = str(e)
            raise Exception(u'Get the input date exception: '+ error)

        django_response.content = '\n'.join(response)
        return django_response

#添加服务
soap_application = soaplib.core.Application([StudentSoapService], 'tns')
#urls 中配置的是这个名称
get_student_soap = DjangoSoapApp(soap_application)

```




### 参考
* ![WebServoce优缺点](https://www.cnblogs.com/fuyuesoft/p/4248603.html)
* ![WebService demo](https://github.com/orangle/Django-soap-webservice/blob/master/demo/webservice/views.py)
