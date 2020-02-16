# File: camera_client_udp.py
# Author: Ethan Martin
# Date: 2 February 2020
# Brief: Client program for PiCar video

import cv2
import numpy as np
import socket
import struct
import time

BUF_SIZE = 500
WIDTH = 640
HEIGHT = 480
SCALE = 0.5
FPS_INTERVAL = 0.5

start = time.time()
frame_count = 0
dim = (int(WIDTH * SCALE), int(HEIGHT * SCALE))
size = dim[0] * dim[1] * 3

print('startup')
addr = ('10.0.1.6', 5556)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(addr)
print('socket bound')

buf = bytearray(size)
while True:
    frame_count += 1
    if (time.time() - start) > FPS_INTERVAL:
        fps = frame_count / (time.time() - start)
        print('FPS: {:.3}'.format(fps))
        frame_count = 0
        start = time.time()

    msg = b''

    while msg != b'PICAR_FRAME':
        msg, addr = sock.recvfrom(BUF_SIZE)
        if len(msg) != BUF_SIZE:
            continue
        seq, data = struct.unpack('>H498s', msg)
        offset = 498 * seq
        if offset + len(data) > size:
            continue
        buf[offset : offset + len(data)] = data

    frame = np.frombuffer(buf, dtype=np.uint8).reshape(dim[1], dim[0], 3)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
