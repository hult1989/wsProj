import os

pid1 = os.popen('ps aux | grep init.py').readline().split()[1]
pid2 = os.popen('ps aux | grep babysiter.py').readline().split()[1]


os.system('kill -9 %s %s' %(pid1, pid2))
os.system('pkill tail')
