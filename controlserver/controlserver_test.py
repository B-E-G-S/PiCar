import struct
import socket
import time

RHOST = '10.0.10.100'
RPORT = 39281
LHOST = '10.0.10.20'
LPORT = 39280

MAGIC = 0x5049
VERSION = 0x0001

FMT_HEADER = '>HHBB'
FMT_STATE = '>bb'

def main():
    print('Creating socket...')
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((LHOST, LPORT))

    print('Sending status request')
    msg = struct.pack(FMT_HEADER, MAGIC, VERSION, 0x00, 0x00)
    sock.sendto(msg, (RHOST, RPORT))

    print('Waiting for response...')
    data, _ = sock.recvfrom(4096)
    print('Got response from server')
    header = struct.unpack(FMT_HEADER, data[:struct.calcsize(FMT_HEADER)])
    state = struct.unpack(FMT_STATE, data[struct.calcsize(FMT_HEADER):])
    print(header, state)

    print('Sending command')
    msg = struct.pack(FMT_HEADER, MAGIC, VERSION, 0x01, 0x01) + struct.pack(FMT_STATE, 30, 30)
    sock.sendto(msg, (RHOST, RPORT))

    print('Waiting for response...')
    data, _ = sock.recvfrom(4096)
    print('Got response from server')
    header = struct.unpack(FMT_HEADER, data[:struct.calcsize(FMT_HEADER)])
    state = struct.unpack(FMT_STATE, data[struct.calcsize(FMT_HEADER):])
    print(header, state)

    time.sleep(5)

    print('Sending command')
    msg = struct.pack(FMT_HEADER, MAGIC, VERSION, 0x02, 0x01) + struct.pack(FMT_STATE, 0, 0)
    sock.sendto(msg, (RHOST, RPORT))

    print('Waiting for response...')
    data, _ = sock.recvfrom(4096)
    print('Got response from server')
    header = struct.unpack(FMT_HEADER, data[:struct.calcsize(FMT_HEADER)])
    state = struct.unpack(FMT_STATE, data[struct.calcsize(FMT_HEADER):])
    print(header, state)

if __name__ == "__main__":
    main()
