### Python Collections模块解析

<br/>

#### 原由
* 个人认为看了裘宗燕教授的Python数据结构与算法，对于Python的数据结构了解算是入门了，每次写代码也是按照复杂度/耗时最低的方面去写
* 有人说这个模块包含了Python数据结构的精华，打算对比下自己掌握的Python相关数据结构，看看知识是否牢固

<br/>


#### 模块解析

**模块概要**
* 该模块包含五种高级数据结构，分别是：
    * Counter：计数器，用于统计元素个数
    * OrderDict：有序字典
    * defaultdict：带默认值的字典
    * namedtuple：可命名元组，可以通过名字访问元组
    * deque：双向队列，可从任意地方取值

<br/>

**源码分析**
* defaultdict：该类曾经在项目中使用过，可以精简项目代码，而且可以加快速度
    * 在用之前是怎么解决的？为什么要用这个？
        * 项目中需要对遍历一堆数据，然后从一堆数据中找出每个对象的属性，遍历一次只能找到一个对象的属性，而每个对象都有多条属性，我经历了几次优化才用到目前的办法：
            * **第一次**：使用列表包字典的方式，在遍历时，首先获取该对象名，然后再去遍历列表，判断列表中的每一个字典是否有名字叫该对象的字典，如果有，就取出，如果没有，就创一个字典对象放入列表。该方法首先是复杂度高，如果有n个对象，我最多就要查找n次，就是n的平方，而且还要针对创建和已存在走不同的分支
            * **第二次**：使用字典的方式，以对象名为键，因为Python字典判断在不在使用的是哈希表的方式，我去判断是否有这个对象，复杂度是O(1)，但是还是需要根据是否已经有了对象还是没有对象走不同的分支
            * **第三次**：使用defaultdict的方式，把对象的属性封装成一个类，然后实例化，每次就直接从这个实例里面去拿对象，该实例其实也是个字典，只是如果遇到没有的键，就会调用传入的类实例化一个出来，我每次只需要从该实例中拿值，然后填充即可，遍历中如果遇到已经符合了某条条件的属性后，直接continue，因为不可能会符合其他条件了，以上做法是我知道的最低复杂度和最简洁的代码了。
    * 示例代码如下：
        ```
        # -*- coding: utf-8 -*- 

        #仿写collections模块中的defaultdict类，简单实现，默认实例化生成字典，针对默认字典中没有的键，就直接返回一个实例

        class defaultdict:
            
            def __init__(self, customClass):
                self.defaultdict = {}
                self.defaultClass = customClass
            
            def __missing__(self, key):
                return self.defaultClass()
            
            def __getitem__(self,key):
                try:
                    return self.defaultdict[key]
                except Exception, e:
                    return self.__missing__(key)
            
            def __setitem__(self, key, value):
                self.defaultdict[key] = value
                
            def __repr__(self):
                return '%s'% self.defaultdict
                

        class Vol:
            
            def __init__(self):
                self.name = ''
                self.size = '0'
                self.id = 0
                

        if __name__ == '__main__':
            dicts = defaultdict(Vol)
            print dicts
            vol_1 = dicts['vol_1']
            print vol_1
            dicts['vol_1'] = vol_1
            print dicts
        ```






<br/>

#### 参考资料
* [Python高级数据结构-Collections模块](https://www.cnblogs.com/deeper/p/8073412.html)
* [Python中defaultdict的详解](https://www.yunziyuan.com.cn/7702.html)
