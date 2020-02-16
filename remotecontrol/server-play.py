'''import zmq
import json'''
from picar.front_wheels import *
from picar.back_wheels import *

# Setup PiCar
fw = Front_Wheels(channel=0)
camera_pan = Front_Wheels(channel=1)
camera_tilt = Front_Wheels(channel=2)
bw = Back_Wheels()

'''
port = "5557"
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://10.0.1.100:%s" % port)
'''
while True:
    #message = json.loads(socket.recv())
    message = {"command" : "turn"}
    # Skip if not valid command message
    if 'command' not in message:
        continue
    # Parse command and remove it from dictionary
    #command = message['command']
    del message['command']
    command = "turn"
    execute = None
    # Bind the relevant command
    if command == "forward":
        execute = bw.forward
    elif command == "backward":
        execute = bw.backward
    elif command == "speed":
        execute = bw.speed
    elif command == "turn":
        execute = fw.turn(30)
    elif command == "pan":
        # Pan the camera
        execute = camera_pan.turn
    elif command == "tilt":
        # Tilt the camera
        execute = camerate_tilt.turn
    else:
        print("Command not recognized")
    # Execute the command with whatever parameters necessary
    execute(**command)




