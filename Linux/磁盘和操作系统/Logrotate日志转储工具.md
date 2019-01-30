## Logrotate 

### 简介
logrotate是一个日志管理的工具，用来把旧的文件删除或者备份，这个过程称为转储。

### 原理
logrotate 的执行由crond(定时任务)来执行，在/etc/cron.daily/下面有一个logrotate脚本，每天定时由crond启动运行，每次执行logrotate的时候，
需要指定配置文件，如果配置文件ok的话，那就写好配置文件放到/etc/logrotate.d下面即可，后面的事就是每天crond定时启动/etc/cron.daily/logrotate
脚本，该脚本会读取/etc/logrotate.d/下面的文件即可。

### 配置文件写法
/var/log/syslog
{
    rotate 7        #保留7份日志文件；
    daily           #每天轮换一次；
    missingok       #如果日志丢失，不报错；
    minsize 10M     #定义日志必须大于10M才会去轮换；
    notifempty      #如果是空文件就不进行转存；
    compress        #压缩日志； 
    delaycompress   #延迟压缩，和compress一起使用时，转储的日志文件到下一次转储时才压缩；
    postrotate      #轮换过后重启rsyslog服务；
    invoke-rc.d rsyslog rotate > /dev/null
    endscript       #结束脚本；
}
