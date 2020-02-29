#!/usr/bin/env bash
DEVICE=/dev/video0
FRAMERATE=30
DESTIP=224.1.1.1
DESTPORT=5000
gst-launch-1.0 \
        v4l2src device=$DEVICE ! \
        videoconvert ! \
        videorate ! \
        video/x-raw,framerate=$FRAMERATE/1 ! \
        x264enc interlaced=true tune=zerolatency speed-preset=ultrafast ! \
        rtph264pay ! \
        udpsink host=$DESTIP auto-multicast=true port=$DESTPORT
