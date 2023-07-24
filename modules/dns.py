import subprocess  # For executing a shell command

def dns(host):
    command = ['nslookup', host]
    dns_result = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, 
        stderr = subprocess.PIPE, universal_newlines=True, bufsize = 1)
    out,err = dns_result.communicate()
    print('std_out: ' + out)
    print('std_err: ' + err)
    print('returncode: ' + str(dns_result.returncode))
    return out