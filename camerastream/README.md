# Scripts for Camera Streaming

Currently there are two options available for streaming the PiCar camera video. Ethan's custom UDP implementation and Brandon's gstreamer-based implementation

## To Test Video
To do a simple test to see if the PiCar can access its own camera, run the `scripts/camera_test.py` script.

## Ethan's UDP Implementation
On the PiCar run `legacy/camera_send_udp.py` and on the processing computer run `legacy/camera_client_udp.py`. Make sure that the IP address on both the client and server computers are set properly.

## Brandon's Gstreamer Implementation
On the PiCar run the `scripts/gstream_send.bash` script while on the processing computer run `gstream_receive.py`. Make sure the IP address on both the client and server computers are set properly.

If there is a problem with the H264 encoding, make sure that the `gstreamer1.0-plugins-ugly` package is installed.
