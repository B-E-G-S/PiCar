import gi
import sys
import traceback
import cv2
import numpy as np
from time import sleep

gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

Gst.init(None)


class Video:
    def __init__(self, port=5000):
        """Grabs a Gstreamer h264 encoded video stream"""
        self.pipeline = Gst.parse_launch("udpsrc port=5000 ! \
                            application/x-rtp,payload=96 ! \
                            rtph264depay ! decodebin ! \
                            videoconvert ! \
                            video/x-raw,format=(string)BGR ! \
                            videoconvert ! \
                            appsink emit-signals=true sync=false max-buffers=2 drop=true")
        self.bus = self.pipeline.get_bus()
        # Allow bus to emit messages to main thread
        self.bus.add_signal_watch()
        # Start pipeline
        self.pipeline.set_state(Gst.State.PLAYING)
        # Get Video Sink
        self.video_sink = self.pipeline.get_by_name('appsink0')
        self.bus.connect('message', self.on_message)
        self.video_sink.connect('new-sample', self.on_video)
        self.EOS = False # End of Stream
        self._frame = None
    def on_video(self, sink):
        """Handles video input"""
        sample = sink.emit('pull-sample')
        buffer = sample.get_buffer()
        caps = sample.get_caps()
        self._frame = np.ndarray(
            (
                caps.get_structure(0).get_value('height'),
                caps.get_structure(0).get_value('width'),
                3
            ),
            buffer=buffer.extract_dup(0, buffer.get_size()),
            dtype=np.uint8
        )
        return Gst.FlowReturn.OK
    def on_message(self, bus: Gst.Bus, message: Gst.Message):
        """Handles messages from the stream"""
        if message.type == Gst.MessageType.EOS:
            # Handle End of Stream
            self.EOS = True
            self.quit()
        elif message.type == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            print(err, debug)
            loop.quit()
        elif message.type == Gst.MessageType.WARNING:
            err, debug = message.parse_warning()
            print(err, debug)
        return True
    def get_frame(self):
        frame = self._frame
        self._frame = None
        return frame
    def frame_available(self):
        """States whether or not another frame is available for grabbing"""
        return self._frame is not None
    def quit(self):
        self.pipeline.set_state(Gst.State.NULL)
        self.EOS = False
        

video = Video()
FPS = 30
try:
    while not video.EOS:
        if not video.frame_available():
            continue
        frame = video.get_frame()
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        sleep(1. / FPS)
except Exception:
    traceback.print_exc()
    video.quit()

cv2.destroyAllWindows()
