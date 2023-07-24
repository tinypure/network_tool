import subprocess  # For executing a shell command
import re

def find_net_issue(gw = '192.168.1.1'):
    pattern_loss = re.compile(r'丢失 = (\d+)')   # 丢包
    pattern_avg_latency = re.compile(r'平均 = (\d+)ms')  ##平均时延
    issue = ''
    
    command_gw = ['ping', '-n', '5', '-w', '1500', gw]
    command_MB = ['ping', '-n', '5', '-w', '1500', '221.181.240.55']
    command_PB = ['ping', '-n', '5', '-w', '1500', '221.181.240.77']
    command_BAIDU = ['ping', '-n', '5', '-w', '1500', 'www.baidu.com']
    command_test = ['ping', '-n', '5', '-w', '1500', '1.2.1.2']


    # GW ping test
    ping_gw_result = subprocess.Popen(command_gw, shell = True, stdout = subprocess.PIPE, 
        stderr = subprocess.PIPE, universal_newlines=True, bufsize = 1)
    out,err = ping_gw_result.communicate()
    print('std_out: ' + out)
    print('std_err: ' + err)
    print('returncode: ' + str(ping_gw_result.returncode))

    loss_gw = pattern_loss.findall(out)
    avg_latency_gw = pattern_avg_latency.findall(out)

    # MB ping test
    ping_MB_result = subprocess.Popen(command_MB, shell = True, stdout = subprocess.PIPE, 
        stderr = subprocess.PIPE, universal_newlines=True, bufsize = 1)
    out,err = ping_MB_result.communicate()
    print('std_out: ' + out)
    print('std_err: ' + err)
    print('returncode: ' + str(ping_MB_result.returncode))

    loss_MB = pattern_loss.findall(out)
    avg_latency_MB = pattern_avg_latency.findall(out)

    # DNS ping test
    ping_PB_result = subprocess.Popen(command_PB, shell = True, stdout = subprocess.PIPE, 
        stderr = subprocess.PIPE, universal_newlines=True, bufsize = 1)
    out,err = ping_PB_result.communicate()
    print('std_out: ' + out)
    print('std_err: ' + err)
    print('returncode: ' + str(ping_PB_result.returncode))

    loss_PB = pattern_loss.findall(out)
    avg_latency_PB = pattern_avg_latency.findall(out)

    # BAIDU ping test
    ping_BAIDU_result = subprocess.Popen(command_BAIDU, shell = True, stdout = subprocess.PIPE, 
        stderr = subprocess.PIPE, universal_newlines=True, bufsize = 1)
    out,err = ping_BAIDU_result.communicate()
    print('std_out: ' + out)
    print('std_err: ' + err)
    print('returncode: ' + str(ping_BAIDU_result.returncode))

    loss_BAIDU = pattern_loss.findall(out)
    avg_latency_BAIDU = pattern_avg_latency.findall(out)

    # total result
    print('网关丢包数：' + loss_gw[0])
    if int(loss_gw[0]) != 5:
        print('网关平均时延：' + avg_latency_gw[0] + 'ms')

    print('汇聚层丢包数：' + loss_MB[0])
    if int(loss_MB[0]) != 5:
        print('汇聚层平均时延：' + avg_latency_MB[0] + 'ms')

    print('核心层丢包数：' + loss_PB[0])
    if int(loss_PB[0]) != 5:
        print('核心层平均时延：' + avg_latency_PB[0] + 'ms')

    print('互联网丢包数：' + loss_BAIDU[0])
    if int(loss_BAIDU[0]) != 5:
        print('互联网平均时延：' + avg_latency_BAIDU[0] + 'ms')

    return loss_gw, avg_latency_gw, loss_MB, avg_latency_MB, loss_PB, avg_latency_PB, loss_BAIDU, avg_latency_BAIDU
