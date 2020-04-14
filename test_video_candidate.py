from time import sleep
from threading import Event
import cv2
from camerastream import PiCarVideo

video = PiCarVideo()
stop_program = Event()

@video.subscribe
def show_frame(frame):
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        stop_program.set()

stop_program.wait()
cv2.destroyAllWindows()
