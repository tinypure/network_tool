import subprocess  # For executing a shell command

def traceroute(host):
    command = ['tracert', '-d', host]
    traceroute_result = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, 
        stderr = subprocess.PIPE, universal_newlines=True, bufsize = 1)
    out,err = traceroute_result.communicate()
    print('std_out: ' + out)
    print('std_err: ' + err)
    print('returncode: ' + str(traceroute_result.returncode))
    return out