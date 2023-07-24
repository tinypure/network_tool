#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput
from pycallgraph import Config
from pycallgraph import GlobbingFilter

from tkinter import *
import subprocess  # For executing a shell command
import time
import threading

from modules import get_host_info
from modules import dns
from modules import traceroute
from modules import ping
from modules import speedtest
from modules import find_net_issue
from modules import http_get_answer

LOG_LINE_NUM = 0

ip_addr = ''
gw = ''
ip_addr, gw = get_host_info.get_host_info()

class MY_GUI():
    def __init__(self,window):
        self.window = window


    #设置窗口
    def set_init_window(self):
        self.window.title("网络质量定位分析工具 V1.0")                      #窗口名
        self.window.geometry('1100x700+10+10')                         #1024 768为窗口大小，+10 +10 定义窗口弹出时的默认展示位置   

        #标签
        self.input_label = Label(self.window, text="请输入地址或域名")
        self.input_label.grid(row=0, column=0)
        self.output_label = Label(self.window, text="输出结果")
        self.output_label.grid(row=0, column=12)
        self.log_label = Label(self.window, text="日志")
        self.log_label.grid(row=12, column=0)
        #文本框
        self.input_text = Text(self.window, width=67, height=35)  #原始数据录入框
        self.input_text.grid(row=1, column=0, rowspan=10, columnspan=10)
        self.output_text = Text(self.window, width=70, height=49)  #处理结果展示
        self.output_text.grid(row=1, column=12, rowspan=13, columnspan=8)
        self.log_text = Text(self.window, width=66, height=9)  # 日志框
        self.log_text.grid(row=13, column=0, rowspan=3, columnspan=10)

        #按钮
        self.exec_get_host_info_button = Button(self.window, text="获取本机IP信息", bg="lightblue", width=12,command=self.exec_get_host_info)
        self.exec_get_host_info_button.grid(row=1, column=11)
        self.exec_dns_button = Button(self.window, text="域名解析测试", bg="lightblue", width=12,command=self.exec_dns)
        self.exec_dns_button.grid(row=2, column=11)
        self.exec_traceroute_button = Button(self.window, text="traceroute", bg="lightblue", width=12,command=self.exec_traceroute)
        self.exec_traceroute_button.grid(row=3, column=11)
        self.exec_ping_button = Button(self.window, text="ping测试", bg="lightblue", width=12,command=self.exec_ping)
        self.exec_ping_button.grid(row=4, column=11)
        self.exec_speedtest_button = Button(self.window, text="网速测试", bg="lightblue", width=12,command=self.exec_speedtest)
        self.exec_speedtest_button.grid(row=5, column=11)
        self.exec_find_net_issue_button = Button(self.window, text="问题定界", bg="lightblue", width=12,command=self.exec_find_net_issue)
        self.exec_find_net_issue_button.grid(row=6, column=11)
        self.exec_http_get_answer_button = Button(self.window, text="询问老王", bg="lightblue", width=12,command=self.exec_http_get_answer)
        self.exec_http_get_answer_button.grid(row=7, column=11)

    #获取本机ip信息
    def exec_get_host_info(self):
        try:
            ip_addr, gateway = get_host_info.get_host_info()
            self.output_text.delete(1.0,END)
            self.output_text.insert(1.0, ('本机IP：' + ip_addr + '\n' + '网关：' + gateway))
            self.write_log_to_Text("INFO:获取本机IP成功")
        except:
            self.output_text.delete(1.0,END)
            self.output_text.insert(1.0,"获取本机IP失败")
            self.write_log_to_Text("ERROR:获取本机IP失败")

    #域名解析测试
    def exec_dns(self):
        src = self.input_text.get(1.0,END).strip().replace("\n","").encode()
        if src == b'':
            self.output_text.delete(1.0,END)
            self.output_text.insert(1.0,"域名解析测试失败，请检查是否正确填写域名")
            self.write_log_to_Text("ERROR:域名解析测试失败，请检查是否正确填写域名")
            return
        try:
            out = dns.dns(src)
            self.output_text.delete(1.0,END)
            self.output_text.insert(1.0, out)
            self.write_log_to_Text("INFO:域名解析测试成功")
        except:
            self.output_text.delete(1.0,END)
            self.output_text.insert(1.0,"域名解析测试失败，请检查是否正确填写域名")
            self.write_log_to_Text("ERROR:域名解析测试失败，请检查是否正确填写域名")

    #traceroute
    def exec_traceroute(self):
        src = self.input_text.get(1.0,END).strip().replace("\n","").encode()
        if src == b'':
            self.output_text.delete(1.0,END)
            self.output_text.insert(1.0,"traceroute失败，请检查是否正确填写目标地址")
            self.write_log_to_Text("ERROR:traceroute失败，请检查是否正确填写目标地址")
            return
        try:
            #out = traceroute.traceroute(src)
            #self.output_text.delete(1.0,END)
            #self.output_text.insert(1.0, out)
            #self.write_log_to_Text("INFO:traceroute成功")
            
            command = ['tracert', '-d', src]
            traceroute_result = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, 
                stderr = subprocess.PIPE, universal_newlines=True, bufsize = 1)
            self.output_text.delete(1.0,END)
            
            while True:
                line = traceroute_result.stdout.readline()               
                print(line)
                self.output_text.insert(END,line)
                self.window.update()
                if subprocess.Popen.poll(traceroute_result)==0:
                    line = traceroute_result.stdout.readlines()
                    self.output_text.insert(END,line)
                    self.window.update()
                    break            

        except:
            self.output_text.delete(1.0,END)
            self.output_text.insert(1.0,"traceroute失败，请检查是否正确填写目标地址")
            self.write_log_to_Text("ERROR:traceroute失败，请检查是否正确填写目标地址")

    #ping
    def exec_ping(self):
        src = self.input_text.get(1.0,END).strip().replace("\n","").encode()
        if src == b'':
            self.output_text.delete(1.0,END)
            self.output_text.insert(1.0,"ping失败，请检查是否正确填写目标地址")
            self.write_log_to_Text("ERROR:ping失败，请检查是否正确填写目标地址")
            return
        try:
            #t = threading.Thread(target=ping.ping, args=(src,), daemon=True)
            #t.start()
            #out = t.result
            #out = ping.ping(src)

            self.write_log_to_Text("INFO:ping测试成功")
            command = ['ping', '-n', '5','-w', '1500', src]
            ping_result = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, 
                stderr = subprocess.PIPE, universal_newlines=True, bufsize = 1)
            self.output_text.delete(1.0,END)
            while True:
                line = ping_result.stdout.readline()               
                print(line)
                self.output_text.insert(END,line)
                self.window.update()
                if subprocess.Popen.poll(ping_result)==0:
                    line = ping_result.stdout.readlines()
                    self.output_text.insert(END,line)
                    self.window.update()
                    break
        
        except:
            self.output_text.delete(1.0,END)
            self.output_text.insert(1.0,"ping测试失败，请检查是否正确填写目标地址")
            self.write_log_to_Text("ERROR:ping测试失败，请检查是否正确填写目标地址")

    #网速测试
    def exec_speedtest(self):
        try:
            #out = speedtest.speedtest()
            #self.output_text.delete(1.0,END)
            #self.output_text.insert(1.0, out)
            #self.write_log_to_Text("INFO:网速测试成功")
            speedtest_result = subprocess.Popen('speedtest', shell = True, stdout = subprocess.PIPE, 
                stderr = subprocess.PIPE, universal_newlines=True, bufsize = 1)
            self.output_text.delete(1.0,END)
            while True:
                line = speedtest_result.stdout.readline()               
                print(line)
                self.output_text.insert(END,line)
                self.window.update()
                if subprocess.Popen.poll(speedtest_result)==0:
                    line = speedtest_result.stdout.readlines()
                    self.output_text.insert(END,line)
                    self.window.update()
                    break
        except:
            self.output_text.delete(1.0,END)
            self.output_text.insert(1.0,"网速测试失败")
            self.write_log_to_Text("ERROR:网速测试失败")

    #问题定界
    def exec_find_net_issue(self):
        global gw
        try:
            loss_gw, avg_latency_gw, loss_MB, avg_latency_MB, loss_PB, avg_latency_PB, loss_BAIDU, avg_latency_BAIDU = find_net_issue.find_net_issue(gw)
            s = ''
            s += '网关丢包数：' + loss_gw[0]
            if int(loss_gw[0]) != 5:
                s +='\n网关平均时延：' + avg_latency_gw[0] + 'ms'
            s += '\n\n汇聚层丢包数：' + loss_MB[0]
            if int(loss_MB[0]) != 5:
                s += '\n汇聚层平均时延：' + avg_latency_MB[0] + 'ms'
            s += '\n\n核心层丢包数：' + loss_PB[0]
            if int(loss_PB[0]) != 5:
                s += '\n核心层平均时延：' + avg_latency_PB[0] + 'ms'
            s += '\n\n互联网丢包数：' + loss_BAIDU[0]
            if int(loss_BAIDU[0]) != 5:
                s += '\n互联网平均时延：' + avg_latency_BAIDU[0] + 'ms'
            self.output_text.delete(1.0,END)
            self.output_text.insert(1.0, s)
            self.write_log_to_Text("INFO:find_net_issue成功")
        except:
            self.output_text.delete(1.0,END)
            self.output_text.insert(1.0,"find_net_issue失败，请检查是否正常获取IP")
            self.write_log_to_Text("ERROR:find_net_issue失败，请检查是否正常获取IP")
    
    def exec_http_get_answer(self):
        src = self.input_text.get(1.0,END).strip().replace("\n","")
        if src == '':
            self.output_text.delete(1.0,END)
            self.output_text.insert(1.0,"询问失败，请检查是否正确填写询问内容")
            self.write_log_to_Text("ERROR:询问失败，请检查是否正确填写询问内容")
            return
        try:
            out = http_get_answer.http_get_answer(src)
            self.output_text.delete(1.0,END)
            self.output_text.insert(1.0, out)
            self.write_log_to_Text("INFO:询问成功")
        except:
            self.output_text.delete(1.0,END)
            self.output_text.insert(1.0,"询问失败，请检查是否正确填写询问内容")
            self.write_log_to_Text("ERROR:询问失败，请检查是否正确填写询问内容")


    #获取当前时间
    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return current_time


    #日志动态打印
    def write_log_to_Text(self,logmsg):
        global LOG_LINE_NUM
        current_time = self.get_current_time()
        logmsg_in = str(current_time) +" " + str(logmsg) + "\n"      #换行
        if LOG_LINE_NUM <= 7:
            self.log_text.insert(END, logmsg_in)
            LOG_LINE_NUM = LOG_LINE_NUM + 1
        else:
            self.log_text.delete(1.0,2.0)
            self.log_text.insert(END, logmsg_in)


def gui_start():
    init_window = Tk()              #实例化出一个父窗口
    my_gui = MY_GUI(init_window)
    # 设置根窗口默认属性
    my_gui.set_init_window()

    init_window.mainloop()          #父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示

def main():
    gui_start()
    
if __name__ == "__main__":
    config = Config()
    graphviz = GraphvizOutput()
    graphviz.output_file = 'graph.png'
    with PyCallGraph(output=graphviz, config=config):
        main()