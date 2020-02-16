#!/usr/bin/env bash
gst-launch-1.0 v4l2src device=/dev/video0 ! videoconvert ! x264enc ! rtph264pay ! udpsink host=10.0.10.2 port=5000
