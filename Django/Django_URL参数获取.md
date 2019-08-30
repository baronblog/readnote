### 本文意在理解Django中从URL处获取参数



#### Django从URL处获取参数和Ajax传递参数对比
* Ajax 可以使用get/post等方法进行传值，但Django在URL中带参数只能用于get请求，需要请求时直接刷新对应的URL即可
* Ajax 是用于刷新结果的用法， Django 在URL中获取参数必然是刷新页面(如果该请求是处理一些事情需要返回结果的话，还需要重定向到对应的页面)


#### 具体用法(以/github/blog/article_id/8978/为例)
* 在路由层面应该这样去匹配
```
url(r'github/blog/article_id/(?P<article_id>[0-9]{0,4})', viewfunc, name='viewfunc')
#其中article_id是需要在视图函数中明确写出来的


def viewfuc(request, article_id):
    pass
```
