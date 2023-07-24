import subprocess  # For executing a shell command

def speedtest():
    speedtest_result = subprocess.Popen('speedtest', shell = True, stdout = subprocess.PIPE, 
        stderr = subprocess.PIPE, universal_newlines=True, bufsize = 1)
    out,err = speedtest_result.communicate()
    print('std_out: ' + out)
    print('std_err: ' + err)
    print('returncode: ' + str(speedtest_result.returncode))
    return out