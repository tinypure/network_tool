import subprocess  # For executing a shell command
import re

def get_host_info():
    pattern_host = re.compile(r'IPv4 地址 . . . . . . . . . . . . : (.*)\n   子网掩码  . . . . . . . . . . . . : .*\n   默认网关. . . . . . . . . . . . . : (.*)\n')   # 丢包
    get_host_info_result = subprocess.Popen('ipconfig', shell = True, stdout = subprocess.PIPE, 
        stderr = subprocess.PIPE, universal_newlines=True, bufsize = 1)
    out,err = get_host_info_result.communicate()
    print('std_out: ' + out)
    print('std_err: ' + err)
    print('returncode: ' + str(get_host_info_result.returncode))
    host = pattern_host.findall(out, re.S)
    print(host)
    for i in host:
        if i[1] == '':
            continue
        else:
            ip_addr = i[0]
            gateway = i[1]
    return ip_addr, gateway

#ip_addr, gateway = get_host_info()

#print(ip_addr)
#print(gateway)