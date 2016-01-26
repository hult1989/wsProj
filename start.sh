touch ./log_file/server.log
touch ./log_file/babysiter.log
tail -f ./log_file/server.log&
python init.py&
echo '1. main program init'
python babysiter.py&
echo '2. babsiter program init'
#python ./common/log_observer.py&
twistd web --port=8083 --path=../
echo '3. twistd web server init'
