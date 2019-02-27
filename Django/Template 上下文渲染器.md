## 记录关于Django上下文渲染器

### 常规携带变量内容的做法
* 在每个视图内部都带上相应的参数

```
def login(request):
  context = {'name': setttings.name}
  return render(request, 'index.html', context)
```

### 便利做法
* 使用Template自带的上下文渲染器，比如模板如下文所示，可以自己自定义一个上下文渲染器，然后调用
```
#模板文件
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'app.context'
            ],
        },
    },
]

#context.py文件
def settings(request):
    return {'settings': settings}  #这里可以打印settings文件里面的属性
    
#html用法
Debug：{{ settings.debug }}

```
