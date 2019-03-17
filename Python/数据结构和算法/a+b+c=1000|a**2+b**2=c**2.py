'''
已知a+b+c=1000，a**2+b**2=c**2，分别求出a，b，c

'''


'''
import time

start_time=time.time()
for a in range(0,1000):
    for b in range(0,1000):
        for c in range(0,1000):
            if a + b + c == 1000 and a**2 + b**2 == c**2:
                print("a,b,c的值分别为： %s， %s， %s" % (a,b,c))


end_time=time.time()
cost_time=end_time-start_time
print("最终花费事件：%s"%cost_time)

a,b,c的值分别为： 0， 500， 500
a,b,c的值分别为： 200， 375， 425
a,b,c的值分别为： 375， 200， 425
a,b,c的值分别为： 500， 0， 500
最终花费事件：250.65439200401306
'''

#改进
'''
import time

start_time=time.time()
for a in range(0,1000):
    for b in range(0,1000):
        c=1000-a-b
        if a + b + c == 1000 and a**2 + b**2 == c**2:
            print("a,b,c的值分别为： %s， %s， %s" % (a,b,c))


end_time=time.time()
cost_time=end_time-start_time
print("最终花费事件：%s"%cost_time)

a,b,c的值分别为： 0， 500， 500
a,b,c的值分别为： 200， 375， 425
a,b,c的值分别为： 375， 200， 425
a,b,c的值分别为： 500， 0， 500
最终花费事件：1.7888848781585693
'''
