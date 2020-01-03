### Python 多线程编程之生产者消费者

<br/>

#### 为什么要写这篇文章
* 一直以来，因为cpython中存在GIL，同一个cpu上只能运行一个线程，所有以前的我一直认为Python多线程编程是鸡肋，而且即使口上说cpu密集型使用多进程，io密集型使用多线程,这仅仅是书上说的而已，从未体验过这样的好处
* 问过其他有除Python以外经验的朋友，多线程是可以跑满多核CPU的，这一点比Python强，但是既然选择了Python，我们要享受的应该是Python的优势：灵活，轮子多，而不是一直纠结于Python的GIL问题
* 看Python连接池的库DButils，看到这个库为了应对多线程连接使用的连接池，感觉这样的用法好厉害，特写此文

<br/>

#### 如何使用生产者和消费者
* 启动一个进程后，可以启动多个线程来负责不同的事情，以word为例，打开word后会有一个进程，复制会起一个线程，粘贴又是一个线程，每个线程互不干扰
* 以锁来控制哪个线程获得活动权，没有获得锁的线程就一直等待
* 以一个简单的生产者和消费者模型来看, 当生产者在生产的时候，消费者就处于一直获取锁的状态，获取不到，就该睡着，现在没有你的施展空间
* 当生产者生产完成后，就处于wait状态，该操作会释放锁，然后使用notify_all/notify函数通知其他线程，说你们该干活了，然后其他线程就会处于live状态，然后去获取锁去干活
* 完整代码如下：
    ```
    # -*- coding:utf-8 -*-
    import threading
    import time


    num = 0
    con = threading.Condition()
    money = 7

    class Producer(threading.Thread):
        """生产者"""
        def run(self):
            global num
            # 获取锁
            con.acquire()
            while True:
                num += 1
                print u'生产了1个，现在有{0}个'.format(num)
                time.sleep(1)
                if num >= 5:
                    print u'已达到5个，不再生产'
                    # 唤醒消费者
                    con.notify_all()
                    # 等待-释放锁；被唤醒-获取锁
                    con.wait()
            # 释放锁
            con.release()


    class Customer(threading.Thread):

        def run(self):
            global num
            global money
            while money > 0:
                # 由于场景是多个消费者进行抢购，如果将获取锁操作放在循环外(如生产者),
                # 那么一个消费者线程被唤醒时会锁住整个循环，无法实现另一个消费者的抢购。
                # 在循环中添加一套"获取锁-释放锁",一个消费者购买完成后释放锁，其他消费者
                # 就可以获取锁来参与购买。
                con.acquire()
                if num <= 0:
                    print u'没货了，{0}通知生产者'.format(
                        threading.current_thread().name)
                    con.notify_all()
                    con.wait()
                money -= 1
                num -= 1
                print u'{0}消费了1个, 剩余{1}个'.format(
                    threading.current_thread().name, num)
                con.release()
                time.sleep(1)
            print u'{0}没钱了-回老家'.format(threading.current_thread().name)


    if __name__ == '__main__':
        p = Producer()
        p.start()
        c= Customer()
        c.start()
    
    ```
