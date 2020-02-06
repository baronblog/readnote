### Python3学习心得

<br/>

#### 目的
* 工作中Python版本升级的需要
* 加深对Python版本变化的理解

<br/>

#### 具体目录
* Python3对比Python2优缺点以及改动点
* Python3升级会造成哪些库需要改动

<br/>

##### Python3对比Python2优缺点以及改动点
* **语法的改变**
	* 输出内容：print由关键字改为了函数，python2中print后面接需要打印的内容，python3中print是作为一个函数调用
	* 获取用户输入：python2中是raw_input，python3中是input
	* 使用局部变量：nonlocal关键字用来在函数或其他作用域中使用外层(非全局)变量
	* 创建整数列表：python2中有range，xrange，其中range是用来生成整数的列表的，xrange也是用来生成整数的列表，但是xrange生成的是生成器，数据
				需要的时候才会被生产出来；python3中合并了这两种用法，只有range一个函数
	* 符号的改变：由<>改为了!=
	* 除法运算的改变：python中1/2这样的，只要是分子分母都是整数，得到的必然是整数，python2中得到的是0，python3中得到的是0.5
	* 代码缩进：python2中1个tab键和8个space是等价的，在python3中会直接报错
	* 判断字典中存在key：python2中使用dict.has_key('key')判断是否存在'key'为键的值，python3中只能用in，且建议使用'key' in dict，而不是'key'
				in dict.keys()，因为后者会返回列表，前者是使用哈希先计算散列值，然后进行判断的，复杂度是O(1),后者是O(n)
	* for循环会导致变量泄漏为全局变量，示例代码如下：
		```
		#python2,下述代码最后输出为9，而不是想象中的是1，python3解决了这个问题，输出为1，可以放心使用
		i=1
		[for i in range(10)]
		print i  
		```

<br/>

* **修改了对字符编码的支持**
	* python2默认就是str对象，即字节串(bytes，网络传输中使用的便是该类型)，如果接收方没有正确的接收该数据，便会报编码错误
	* 在django中，充斥着大量对字符编码的判断，如果是python2最好直接用默认的str对象，防止多次进入编码解码的过程,影响效率
	* 如果要对字符串进行编码转换，需要以unicode字符编码为中间码进行转换：str(gbk)-(decode)->unicode-(encode)->str(utf-8)
	* python3中默认字符编码为unicode字符编码，如果使用django时，源码中应该会有unicode转为bytes类型的转换
	* python3转为bytes类型的过程为：bytes-(decode)->str(unicode)-(encode)->bytes
	* 有一句话叫输入决定输出，比如说我爬取了一个xx字符编码的网页(编码类型是我自定义的)，需要在cmd中显示中文字符(cmd以gbk编码)，
	python2中就必须先转换为中间码unicode，然后转换为gbk再输出才能看到完整的文字；python3获取到的就是unicode编码，直接转为gbk即可
	
<br/>

* **类相关**
	* python2有新式类和旧式类，默认是旧式类，如果想用新式类，必须显示继承object；python3移除了旧式类，默认继承object
	* 新式类对比旧式类的不同点：
		* 旧式类不支持某些魔法方法，这点在以前工作中遇到过，具体没做笔记，留坑待填
		* 新式类继承顺序变了：python2是深度优先，python3是广度优先
	
<br/>

#### Python2升级到Python3会造成哪些库需要改动
* python2使用MySQLdb连接数据库，python3使用PyMySQL连接数据库
* python3.4引入的asyncio模块，虽然目前开发业务使用的是同步编程模型，但是该模块可以用来进行编写守护进程，比如说
  监控平台代码是否有更改，如果有更改，重启服务，使用异步IO可以监控多个事情更简单，这样写更为简洁，一个函数就是
  一个监控服务，demo如下：
  ```
  #!/usr/bin/python
  # -*- coding: utf-8 -*-

  import asyncio

  monitorSize = {'monitor':0} #初始值为0


  @asyncio.coroutine
  def monitorService():
     cmd = 'stat /var/www/'
     rd1 = Execmd(cmd)
     monitorSize['monitor'] = rd1['info']
     asyncio.sleep(3)
     rd2 = Execmd(cmd)
     if monitorSize['monitor'] != rd2['info']:
         Execmd('service httpd restart')

  if __name__ == '__main__':
      while True:
         tasks = [monitorService]
         loop=asyncio.get_event_loop()
         loop.run_until_complete(asyncio.wait(tasks))
        loop.close()
  ```
* requests/urllib2等相关HTTP请求的包需要更新，需要对应找到对应版本，比如说[requests3](https://pypi.org/project/requests3/)不对python2进行
  兼容；urllib2合并成了urllib
* 


#### 参考资料
* [Python字符编码](http://aju.space/2015/11/10/Python-character-encoding-explained.html)
