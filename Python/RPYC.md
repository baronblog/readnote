## Python RPYC包的应用

### 简介
Python的rpyc包是用来实现分布式计算的一个库，支持同步，异步，回调和远程服务的一个库，可以轻松帮我们实现操作远端机器。

### 用法
* 思路以及注意事项：
  * 主动发起调用的是客户端，被动连接的是服务端，如果需要相互调用，需要每一端都需要有一个服务端来响应
  * 两端都需要安装rpyc包
  * rpyc 调用远端命令的权限取决于服务端进程的权限
  * rpyc没有安全认证权限，稍微比较保险的是如果不知道服务端方法是不可能执行相关命令的，也可以在防火墙进行安全设置
  * 服务端的方法前端必须添加exposed_打头，不然无法识别，客户端可以只写exposed_后面的名字
  * 如果服务端执行任务时间太长，最好使用异步的方法和加一个延迟限制，不然客户端迟迟得不到反应
  
  
### demo
  
  * 服务端
  ```
 # coding:utf-8  
      
  from rpyc import Service  
  from rpyc.utils.serverimport ThreadedServer  

  class TestService(Service):  

      defexposed_test(self, num):  
          return 1+num  

  sr = ThreadedServer(TestRpyc, port=9999, auto_register=False)  
  sr.start()  
  ```
  
  * 客户端
  ```
 # coding:utf-8  

  import rpyc  

  conn =rpyc.connect('localhost',9999)  
  cResult =conn.root.test(11)  
  conn.close()  

  print cResult  
  ```
