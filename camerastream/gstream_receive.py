import gi
import traceback
import cv2
import numpy as np
import threading

gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

Gst.init(None)

class GStream:
    def __init__(self, multicastaddress = "224.1.1.1", port=5000):
        """Grabs a Gstreamer h264 encoded video stream"""
        self.pipeline = Gst.parse_launch(f"udpsrc multicast-group={multicastaddress} auto-multicast=true port={port} ! \
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
        self.EOS = threading.Event() # End of Stream
        self.frame_available = threading.Event()
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
        self.frame_available.set()
        return Gst.FlowReturn.OK
    def on_message(self, bus: Gst.Bus, message: Gst.Message):
        """Handles messages from the stream"""
        if message.type == Gst.MessageType.EOS:
            # Handle End of Stream
            self.EOS.set()
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
        self.frame_available.clear()
        return self._frame
    def quit(self):
        self.pipeline.set_state(Gst.State.NULL)
        self.EOS.set()
        


class VideoReceive(threading.Thread):
    def __init__(self, on_video, fps = 30, multicastaddress = "224.1.1.1", port = 5000):
        """Class that allows you to specify what to do when a frame is received.
        on_video: A function that is given a frame when available, must return true to continue
        FPS: The frames per second to enforce
        port: The port to listen on
        """
        self.on_video = on_video
        self.FPS = fps
        self.gstream = GStream(multicastaddress, port)
        threading.Thread.__init__(self)
    def run(self):
        try:
            while not self.gstream.EOS.wait(1. / self.FPS):
                # Once we've waited the obligated FPS, then we wait for 
                # a frame to actually become available.
                self.gstream.frame_available.wait()
                frame = self.gstream.get_frame()
                resume = self.on_video(frame)
                if resume == False:
                    break
        except Exception:
            traceback.print_exc()
            self.gstream.quit()
    def stop(self):
        self.gstream.EOS.set()
    
