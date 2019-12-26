### Django使用manage命令发生了什么

<br/>

#### 起因
今日来了一位同事问我关于socket的问题，我说了句使用python manage.py runserver可以算是socket的具体应用，可能说的不全对，草草的看了下django本地启动的代码，其实用到的socket只是很少，就是一个监听用到了，所以特地写下此文研究下

<br/>

#### 研究过程：使用python manage.py runserver 究竟发生了什么？

<br/>

* 输入python manage.py runserver后首先会实例化django.core.management.ManagementUtility类，然后调用其中的execute方法, 如果执行错误，就会把输入的参数改为help，展示帮助信息；
    ```
    def execute_from_command_line(argv=None):
    """
    A simple method that runs a ManagementUtility.
    """
    utility = ManagementUtility(argv)
    utility.execute()
    ```

<br/>

* 接下来便开始处理外部的参数, 可以指定配置文件，环境变量和其他参数，以及把[Django项目中的settings文件导入到环境中](https://github.com/yangyang510/readnote/blob/master/Django/Django%20%E4%B8%AD%E7%9A%84settings%E6%96%87%E4%BB%B6%E6%98%AF%E5%A6%82%E4%BD%95%E5%AF%BC%E5%85%A5%E5%88%B0%E9%A1%B9%E7%9B%AE%E4%B8%AD%E7%9A%84.md), 直至运行到self.fetch_command(subcommand).run_from_argv(self.argv)这句代码才是发生的重点


    ```
        def execute(self):

        try:
            subcommand = self.argv[1]
        except IndexError:
            subcommand = 'help'  # Display help if no arguments were given.

        parser = CommandParser(None, usage="%(prog)s subcommand [options] [args]", add_help=False)
        parser.add_argument('--settings')
        parser.add_argument('--pythonpath')
        parser.add_argument('args', nargs='*')  # catch-all
        try:
            options, args = parser.parse_known_args(self.argv[2:])
            handle_default_options(options)
        except CommandError:
            pass  

        no_settings_commands = [
            'help', 'version', '--help', '--version', '-h',
            'compilemessages', 'makemessages',
            'startapp', 'startproject',
        ]

        try:
            settings.INSTALLED_APPS
        except ImproperlyConfigured as exc:
            self.settings_exception = exc
            if subcommand in no_settings_commands:
                settings.configure()

        if settings.configured:
            django.setup()

        self.autocomplete()

        if subcommand == 'help':
            if '--commands' in args:
                sys.stdout.write(self.main_help_text(commands_only=True) + '\n')
            elif len(options.args) < 1:
                sys.stdout.write(self.main_help_text() + '\n')
            else:
                self.fetch_command(options.args[0]).print_help(self.prog_name, options.args[0])
        elif subcommand == 'version' or self.argv[1:] == ['--version']:
            sys.stdout.write(django.get_version() + '\n')
        elif self.argv[1:] in (['--help'], ['-h']):
            sys.stdout.write(self.main_help_text() + '\n')
        else:
            self.fetch_command(subcommand).run_from_argv(self.argv)
    ```

    <br/>

    * 使用django.core.management.ManagementUtility对象调用fetch_command方法最后返回了<django.contrib.staticfiles.management.commands.runserver.Command object at 0x0000000003B13208>对象，为什么会这样呢？
        * 首先获取了runserver映射的路径是django.contrib.staticfiles，然后通过拼接，获取到了完整路径，然后动态导入，最后返回该实例
            ```
            def load_command_class(app_name, name):
                module = import_module('%s.management.commands.%s' % (app_name, name))
                return module.Command()
            ```
    
    <br/>

    * 上述代码返回后再调用run_from_argv，为什么可以调用呢？因为这里有个连锁继承的关系：Command类继承自RunserverCommand，RunserverCommand继承BaseCommand，所以才可以调用，然后调用django.contrib.staticfiles.management.commands.runserver.Command.excute函数，然后通过多继承找到了BaseCommand的execute函数

    <br/>

    * 然后执行该excute函数的时候，调用Command类的handler函数，最后由run到inner_run函数，最后再到run函数，如果开启了多线程，就使用元类创建一个WSGIServer类，然后实例化，然后一直坚听
        ```
        def run(addr, port, wsgi_handler, ipv6=False, threading=False):
            server_address = (addr, port)
            if threading:
                httpd_cls = type(str('WSGIServer'), (socketserver.ThreadingMixIn, WSGIServer), {})
            else:
                httpd_cls = WSGIServer
            httpd = httpd_cls(server_address, WSGIRequestHandler, ipv6=ipv6)
            if threading:
                httpd.daemon_threads = True
            httpd.set_app(wsgi_handler)
            httpd.serve_forever()
        ```

    <br/>

    * 然后就是起监控的流程,使用IO多路复用的方法一直坚听对应的端口进行循环

        ```
            def serve_forever(self, poll_interval=0.5):
                self.__is_shut_down.clear()
                try:
                    while not self.__shutdown_request:
                        r, w, e = _eintr_retry(select.select, [self], [], [],
                                            poll_interval)
                        if self.__shutdown_request:
                            break
                        if self in r:
                            self._handle_request_noblock()
                finally:
                    self.__shutdown_request = False
                    self.__is_shut_down.set()
        ```



#### 总结
* 目前源码的解析都写的不是很清楚，因为只能看懂一大段的代码，并不能完全理解为什么这么做，甚至学到一招半式最后用于实际写代码中，这是一个比较大的缺点，是为了学源码而学源码，有点得不偿失
