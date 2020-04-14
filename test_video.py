from camerastream import VideoReceive
import cv2
from time import sleep

def show_frame(frame):
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        return False
    return True

v = VideoReceive(show_frame)
v.start()
sleep(20)
v.stop()

cv2.destroyAllWindows()
