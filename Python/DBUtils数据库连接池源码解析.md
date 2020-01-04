### DButils 数据库连接池的使用

<br/>

#### 如何使用数据库连接池
* 曾经写过的demo如下：主要使用到了DBUtils库帮助我管理了连接池，这是我参照别人的写法写的demo，我理解的好像连接池只有一个(_pool)，具体如何仔细看看源码分析即可知道
    ```
        # -*- coding:utf-8 -*-
        import MySQLdb
        import DBUtils
        import time
        from MySQLdb.cursors import DictCursor
        from DBUtils.PooledDB import PooledDB


        class MySQLPool:

            __pool = None
            
            def __init__(self):
                self._conn = MySQLPool.__getConn()
                self._cursor = self._conn.cursor()
                
            @staticmethod
            def __getConn():
                if MySQLPool.__pool is None:
                    __pool = PooledDB(creator=MySQLdb,mincached=1 , maxcached=20 ,
                                    host='10.10.3.111' , port=111 , user='11' , passwd='1111@1111' ,
                                    db='kpf',use_unicode=False,charset='utf8',cursorclass=DictCursor)
                return __pool.connection()
                                    
            def func_time(func):
                def inner(*args,**kw):
                    start_time = time.time()
                    func(*args,**kw)
                    end_time = time.time()
                    print '数据库连接池运行时间为：%s' %(str(end_time-start_time))
                return inner
            
            @func_time
            def getAll(self,sql):
                count = self._cursor.execute(sql)
                self._conn.commit()
                self._cursor.close()
                self._conn.close()
                return count
                

        class MySQL:
            
            def __init__(self):
                self._conn = MySQLdb.connect(host='10.10.1.162',port=111,
                                                    user='ssss',
                                                    passwd='111@1111',
                                                    db='sss',
                                                    connect_timeout=100,
                                                    charset='utf8')
                                                    
            def func_time(func):
                def inner(*args,**kw):
                    start_time = time.time()
                    func(*args,**kw)
                    end_time = time.time()
                    print '数据库连接时间为：%s' %(str(end_time-start_time))
                return inner
                
                
            @func_time
            def getAll(self,sql):
                cursor = None
                cursor = self._conn.cursor()
                count = cursor.execute(sql)
                cursor.close()
                self._conn.commit()
                self._conn.close()
                return count
            
            

        def func_time(func):
            def inner(*args,**kw):
                start_time = time.time()
                func(*args,**kw)
                end_time = time.time()
                print '函数运行时间为：%s' %(str(end_time-start_time))
            return inner
            
            
        def testMySQL():
            sql = 'select count(*) from tbl_kpf_volumn'
            for r in range(0,301):
                mysql = MySQL()
                result = mysql.getAll(sql)
            
        def testMySQLPool():
            sql = 'select count(*) from tbl_kpf_volumn'
            for r in range(0,301):
                mysqlpool = MySQLPool()
                result = mysqlpool.getAll(sql)
                

        if __name__ == '__main__':
            testMySQL()
            testMySQLPool()
    ```


<br/>


#### DButils模块连接池源码分析
* 使用DBUtils.PooledDB.PooledDB创建连接池即可，后续的连接都是从该类的实例中获取即可，这里是如何管理的呢？首先需要注意几个参数，这几个参数帮助我们控制了该类连接池中连接的相关数据
    * creator： 使用创建连接池的驱动，比如说MySQLdb
    * mincached: 最小生成的连接池个数
    * idle: 该类变量是根据mincached来的，把该参数传入range中，然后调用类方法dedicated_connection预先生成最小的连接，然后放入ide列表中，放入后再一个个close掉，写的是专有连接，目前没明白作用
    * _idle_cache：实际的空闲连接池，所有的连接都是从这里读取

<br/>

* 如何获取连接池中的连接呢？
    * 有一个点提的提一下就是connect函数默认参数是线程安全的，对新手使用比较友好
    * 首先是如何创建连接？
        * 获取连接时首先是获取线程锁
        * 获取线程锁了之后再去_idle_cache里面去pop出来一个连接，如果没有，便调用类里面的参数，再次生成一个连接，然后检测连接是否可用
    * **为什么该包是线程安全的？从代码来看，每次获取连接前总是需要acquire，去获取锁，另外一个线程在工作，当然不能获取锁啦，难道是这个的作用就只是获取连接，有了连接就可以为所欲为了？**
