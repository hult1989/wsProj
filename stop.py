import os

pid1 = os.popen('ps aux | grep \[i]nit.py').readline().split()[1]
pid2 = os.popen('ps aux | grep \[b]abysiter.py').readline().split()[1]


os.system('kill -9 %s %s' %(pid1, pid2))
os.system('pkill tail')
