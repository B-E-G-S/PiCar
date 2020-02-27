#!/usr/bin/env bash
DEVICE=/dev/video0
FRAMERATE=15
DESTIP=10.0.10.2
DESTPORT=5000
gst-launch-1.0 \
	v4l2src device=$DEVICE ! \
	videoconvert ! \
	videorate ! \
	video/x-raw,framerate=$FRAMERATE/1 ! \
	x264enc interlaced=true tune=zerolatency speed-preset=ultrafast ! \
	rtph264pay ! \
	udpsink host=$DESTIP port=$DESTPORT
