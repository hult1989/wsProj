import os
import subprocess
import time

os.popen('touch ./log_file/server.log')
subprocess.Popen('tail -f ./log_file/server.log&', shell=True)

initPid = os.popen('ps axu | grep \[i]nit.py').read().strip()
if initPid == '':
    os.popen('python init.py&')
    print '1. main program init'
else:
    print '1. main program exists'


time.sleep(1)
siterPid = os.popen('ps axu | grep \[b]abysiter.py').read().strip()
if siterPid == '':
    os.popen('python ./common/babysiter.py&')
    print '2. babisiter program init'
else:
    print '2. babisiter program exists'

os.popen('pkill twistd')
os.popen('twistd web --port=8083 --path=../')
print '3. twistd program init'


