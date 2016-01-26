import os

try:
    pid1 = os.popen('ps aux | grep \[i]nit.py').readline().split()[1]
    os.system('kill -9 %s' %(pid1,))
    print '1. main program quit'
except Exception as e:
    print '1. main program not exist'
try:
    pid2 = os.popen('ps aux | grep \[b]abysiter.py').readline().split()[1]
    os.system('kill -9 %s' %(pid2,))
    print '2. babsiter quit'
except Exception as e:
    print '2. babysiter program not exist'
try:
    os.system('pkill tail')
    pid3 = os.popen('ps aux | grep \[l]og_observer.py').readline().split()[1]
    os.system('kill -9 %s' %(pid3,))
    print '3. log observer quit'
except Exception as e:
    print '3. log observer program not exist'


os.system('pkill twistd')
print '4, twistd quit'
