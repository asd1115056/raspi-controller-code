#!/bin/bash

screen -S mjpg -d -m bash -c '/usr/local/bin/mjpg_streamer -i "input_uvc.so -n -r 1280x720 -d /dev/video0 -f 30" -o "output_http.so -p 8080 -w /usr/local/share/mjpg-streamer/www"'

