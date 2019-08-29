## 紧接上文，对实现rest framework接口再次细说


### 已知步骤
* 创建一个序列化的类
* 把数据库中的数据交给序列类完成序列化
* 把序列化的数据返回给前端


### 操作流程
#### 安装rest framework模块
```
pip install djangorestframework
```

#### 注册以及添加权限模块
```
* 需要在settings文件中注册
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
]


* 需要在settings文件中添加权限模块
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

```


#### 创建序列化类

```
* 序列化类
from rest_framework import serializers
from api.models import Person

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('first_name', 'last_name')
        
* 补上模型部分
from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
```


#### 数据库中获取数据并交给序列化类处理
留坑
