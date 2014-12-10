#!/bin/bash

raspivid -t 0 -h 320 -w 480 -fps 25 -b 2000000 -o - | gst-launch-1.0 -v fdsrc ! h264parse ! rtph264pay config-interval=1 pt=96 ! gdppay ! tcpserversink host=rpi.local port=5000