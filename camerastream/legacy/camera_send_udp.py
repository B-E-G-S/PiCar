import cv2
import numpy as np
import socket
import struct
import time

BUF_SIZE = 500
SCALE = 0.5
WIDTH = 640
HEIGHT = 480
FPS_INTERVAL = 0.5

start = time.time()
frame_count = 0
dim = (int(WIDTH * SCALE), int(HEIGHT * SCALE))

cap = cv2.VideoCapture(0)

addr = ('10.0.10.2', 5556)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    frame_count += 1
    if (time.time() - start) > FPS_INTERVAL:
        fps = frame_count / (time.time() - start)
        print('FPS: {:.3}'.format(fps))
        frame_count = 0
        start = time.time()

    ret, frame = cap.read()
    frame = cv2.resize(frame, dim)
    seq = 0

    data = frame.tostring()
    sock.sendto(b'PICAR_FRAME', addr)

    while data:
        msg = struct.pack('>H498s', seq, data[:BUF_SIZE - 2])
        sent = sock.sendto(msg, addr)
        data = data[sent - 2:]
        seq += 1

cap.release()
cv2.destroyAllWindows()
