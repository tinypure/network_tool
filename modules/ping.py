from tkinter import *
import subprocess  # For executing a shell command

def ping(host):
    # Option for the number of packets as a function of
    # param = '-n' if platform.system().lower()=='windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', '-n', '5','-w', '1500', host]

    ping_result = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, 
        stderr = subprocess.PIPE, universal_newlines=True, bufsize = 1)
    
    while True:
        line = ping_result.stdout.readline()
        print(line)
        if subprocess.Popen.poll(ping_result)==0:
            break
    return line
    #out,err = ping_result.communicate()
    #print('std_out: ' + out)
    #print('std_err: ' + err)
    #print('returncode: ' + str(ping_result.returncode))
    #return out