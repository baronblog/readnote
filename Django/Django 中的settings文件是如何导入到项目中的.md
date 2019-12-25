### Django 中的settings文件是如何导入到项目中的


#### 起源
工作中发现这样一个问题，有时候在Django项目的settings文件中修改配置文件不生效，居然要修改Django源码中的settings文件(django.conf.global_settings)，这让我很是好奇，所以决心探查下其中原理，是如何覆盖的


#### 解读之前的理解
* 项目中的settings文件中的字段会默认覆盖django.conf.global_settings文件，如果没有的字段，才会去读django.conf.global_settings文件

#### 源码阅读过程
* 部署后的项目是通过wsgi文件启动项目的，所以调用该文件时会设置默认环境变量，也就是项目setting文件的相对项目的目录
    ```
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "xxxx.settings")
    ```


* 导入后就是调用get_wsgi_applicationh函数，其中要执行setup，也就是对环境进行操作,会从源码目录django.conf文件中导入settings实例对象


* 导入settings实例对象后，会获取该实例对象的属性，该实例对象中有__getattr__魔法方法，会判断实例属性_wrapped为空的话，就会调用_setup方法


* 具体解析_setup方法：
    * 首先是会得到settings文件的相对项目的路径，然后初始化Settings类，该类初始化首先是获取django.conf.global_settings文件，然后遍历该文件中的属性，如果不是大写的，全部丢弃

    * 然后使用动态导入该settings文件
        ```
        mod = importlib.import_module(self.SETTINGS_MODULE)
        ```
    
    * 导入后使用dir获取相关属性进行遍历，如果不是大写的，丢弃; 如果是大写的，就获取该模块的属性值，如果该模块没有属性值为空，或者没获取到，就使用global_settings文件中的默认值


#### 问题
* 按照上述阅读源码过程所说，岂不是settings文件必须写全默认值，至少要有这个属性，否则的话，连遍历的机会都没有？？？

    * 以上担忧是属于错误的
    * 首先初始化Settings类的时候，就会获取global_settings文件中的属性，对文件中的每一个属性进行遍历(属性必须全为大写)，并且把其中的属性值设置给实例化的对象
    * 然后再动态导入项目的settings文件，然后进行遍历，把其中有的属性值在对象的基础上进行修改，如果settings文件中没有遍历到的，就使用上一步设置的(即django.conf.global_settings文件中的默认值)

    ```
    class Settings(BaseSettings):
    def __init__(self, settings_module):
        # update this dict from global settings (but only for ALL_CAPS settings)
        for setting in dir(global_settings):
            if setting.isupper():
                setattr(self, setting, getattr(global_settings, setting))

        # store the settings module in case someone later cares
        self.SETTINGS_MODULE = settings_module

        mod = importlib.import_module(self.SETTINGS_MODULE)

        tuple_settings = (
            "ALLOWED_INCLUDE_ROOTS",
            "INSTALLED_APPS",
            "TEMPLATE_DIRS",
            "LOCALE_PATHS",
        )
        self._explicit_settings = set()
        for setting in dir(mod):
            if setting.isupper():
                setting_value = getattr(mod, setting)

                if (setting in tuple_settings and
                        isinstance(setting_value, six.string_types)):
                    raise ImproperlyConfigured("The %s setting must be a tuple. "
                            "Please fix your settings." % setting)
                setattr(self, setting, setting_value)
                self._explicit_settings.add(setting)
    ```
