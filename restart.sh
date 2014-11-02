kill -9 `ps aux | grep "python main.py 36000" | grep -v grep|awk '{print $2}'`
nohup python main.py 36000 >/dev/null 2>&1 &
