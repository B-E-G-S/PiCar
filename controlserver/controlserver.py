import struct
import socket
from picar.front_wheels import *
from picar.back_wheels import *

HOST = '10.0.10.100'
PORT = 39281

MAGIC = 0x5049
VERSION = 0x0001

FMT_HEADER = '>HHBB'
FMT_STATE = '>bb'

fw = Front_Wheels(channel=0)
ct = Front_Wheels(channel=1)
cp = Front_Wheels(channel=2)
bw = Back_Wheels()


def main():
    speed = 0
    angle = 0

    print('Creating socket...')
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))

    while True:
        data, client = sock.recvfrom(4096)
        print('Message from {}'.format(client))

        header = struct.unpack(FMT_HEADER, data[:struct.calcsize(FMT_HEADER)])

        if header[0] != MAGIC or header[1] != VERSION:
            print('Invalid magic or version mismatch')

        if header[3] == 0x01:
            # Send out updated state
            state = struct.unpack(FMT_STATE, data[struct.calcsize(FMT_HEADER):])

            speed = state[0]
            angle = state[1]

            print(speed, angle)

            print('setting speed')
            bw.speed = abs(speed)
            if speed > 0:
                bw.forward()
            if speed < 0:
                bw.backward()
            else:
                bw.stop()

            fw.turn(angle + 90)

        if header[3] == 0x00 or header[3] == 0x01:
            # Health check, send current state
            resp = struct.pack(FMT_HEADER, MAGIC, VERSION, header[2], 0x00) + struct.pack(FMT_STATE, speed, angle)
            sock.sendto(resp, client)
            continue

if __name__ == "__main__":
    main()