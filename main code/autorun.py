from os import system

system("screen -d -m bash -c" + "/usr/local/bin/mjpg_streamer -i 'input_uvc.so -r 1280x720 -d /dev/video0 -f 30 -q 80' -o 'output_http.so -p 8080 -w /usr/local/share/mjpg-streamer/www'")
system("screen -d -m bash -c 'python3 manage.py runserver'")
system("screen -d -m bash -c 'python3 sch.py'")
