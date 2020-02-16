import zmq
import json

port = "5557"
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://10.0.1.100:%s" % port)


def main():
    while True:
        cmd = input("picar: ")


        if cmd == "help":
            print("Available Commands:")
            print("help\nforward\nbackward\nturn\npan\ntilt\nexit")
        elif cmd == "backward":
            backward()
        elif cmd == "forward":
            forward()
        elif cmd == "turn":
            turn(direction)
        elif cmd == "pan":
            pan()
        elif cmd == "tilt":
            tilt()
        elif cmd == "exit":
            exit()
        else:
            print("Not valid")

def forward():
    # craft message , encode, and send
    message = json.dumps({"command": "forward"})
    message = message.encode()
    socket.sendall(message)
    pass

def backward():s
    message = json.dumps({"command": "backward"})
    message = message.encode()
    socket.sendall(message)
    pass

def speed(new_speed):
    message = json.dumps({"command": "speed"},
                         {"speed" : int(new_speed)})
    message = message.encode()
    socket.sendall(message)
    pass

def turn(new_direction):
    message = json.dumps({"command": "turn"},
                        {"turn" : new_direction})


    pass

def pan(direction):
    pass

def tilt():
    pass

main()
