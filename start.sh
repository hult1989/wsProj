touch ./log_file/server.log
touch ./log_file/babysiter.log
tail -f ./log_file/server.log&
python init.py&
python babysiter.py&
twistd web --port=8083 --path=../
