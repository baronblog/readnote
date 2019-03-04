### 记录关于Django的基础语法

#### 标签
* if/for 样的用法都是标签的用法，Django Template内置的函数，可以对模板接收到的变量进行一系列操作的内置函数
,用 {% if xxx %}表示
* 比如当视图函数传过来一个字典，模板可以对传过来的字典进行遍历或者循环
```
#视图函数
def index(request):
  context = {"louis":111}
  return HttpResponse(request,context)
  
#模板
#如果传过来的context为真，下面的html代码就会展示
{% if context %}
  <h1>hello world </h1>
{% endif %}
```

#### Django 模板
* Django的模板系统是一个python的库，在任何地方都可以使用，不仅仅是在Django视图中可以使用
* 如何使用：创建 Template 对象 –> 创建 Context –> 调用 render() 方法
```
#创建Template对象
from django import template
t = template.Template("my name is {{ name }}")

#创建context
c = template.Context({"name":"louis"})

#调用render方法
print t.render(c)

#结果:返回的结果是Unicode对象，不是一个python字符串
my name is louis
```

#### 变量
* 变量会由context传入模板里面渲染，如果变量不存在，不会报错，会展示空字符


#### 模板中的数据类型

* 字典：
```
from django.template Template, Context
t = Template("I am {{ age }} ")
c = Context({"age":12}}
t.render(c)

```

* 列表
```
from django.template Template, Context
t = Template("I am {{ age.0 }} ")
c = Context([12])
t.render(c)

```

#### 过滤器
* 过滤器主要是起管道的作用，过滤器的输出等于另外一个管道的输入
```
{{ date | date:"YYYY-MM-DD" }}
```






