from tkinter import *

from modules import get_host_info
from modules import dns
from modules import traceroute
from modules import ping
from modules import speedtest
from modules import find_net_issue


#获取本地地址信息
ip_addr, gateway = get_host_info.get_host_info()
print('本机IP：' + ip_addr + '\n' + '网关：' + gateway)

#域名解析测试
dns.dns('www.baidu.com')

#traceroute测试
traceroute.traceroute('112.4.0.55')

#ping测试
ping.ping('112.4.0.55')

#测速
speedtest.speedtest()

#问题定界
find_net_issue.find_net_issue(gateway)
