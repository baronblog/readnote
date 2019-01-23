### IP 

* IP 是网络层主要协议，该层的ARP, ICMP, IGMP协议都以IP协议为为数据报格式传送
* IP 层协议不提供可靠，连接的数据报，准确性由高层来控制准确性
* 两个命令：ifconfig和netstate
<br/>

#### 问题
* ifconfig和ipconfig有什么区别
```
windows用法ipconfig，linux用ifconfig
```
* ifconfig 怎么用
```
ifconfig 不带任何参数，可以展示相关网卡信息
ifconfig 网络端口 ip地址 hw 类型 mac地址 netmask 掩码地址 broadmask 广播地址
ifconfig eth0 192.168.1.99      给该网卡配置临时网络信息，如果需要永久生效，需要编辑eth0网络
ifconfig eth0 up                启用该网卡

```
* netstat 怎么用
