from threading import Thread
import sys
import logging
import numpy as np

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

Gst.init(sys.argv)

class PiCarVideo:
    def __init__(self, multicastaddress="244.1.1.1", port=5000):
        """Grabs a Gstreamer h264 encoded video stream from multicast"""
        self._pipeline = Gst.parse_launch(
            f"udpsrc multicast-group={multicastaddress} auto-multicast=true port={port} ! \
                application/x-rtp,payload=96 ! \
                rtph264depay ! decodebin ! \
                videoconvert ! \
                video/x-raw,format=(string)BGR ! \
                videoconvert ! \
                appsink emit-signals=true sync=false max-buffers=2 drop=true"
        )
        self._bus = self._pipeline.get_bus()
        self._bus.connect('message', self.on_message)
        # Get Video Sink
        self.video_sink = self._pipeline.get_by_name('appsink0')
        self.subscribers = []
        self.video_sink.connect('new-sample', self.publish)
        
        self._pipeline.set_state(Gst.State.PLAYING)
        self.loop = GObject.MainLoop()
        Thread(target=self.loop.run, daemon=True)
    
    def publish(self, sink):
        """Handles video input"""
        sample = sink.emit('pull-sample')
        buffer = sample.get_buffer()
        caps = sample.get_caps()
        frame = np.ndarray(
            (
                caps.get_structure(0).get_value('height'),
                caps.get_structure(0).get_value('width'),
                3
            ),
            buffer=buffer.extract_dup(0, buffer.get_size()),
            dtype=np.uint8
        )
        for subscriber in self.subscribers:
            subscriber(frame)
        
    def subscribe(self, func):
        """Decorators to subscribe for video input"""
        self.subscribers.append(func)
        return func
    
    def on_message(self, _, message: Gst.Message):
        """Handles messages from the stream"""
        if message.type == Gst.MessageType.EOS:
            # Handle End of Stream
            self.quit()
        elif message.type == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            logging.error(err, debug)
        elif message.type == Gst.MessageType.WARNING:
            err, debug = message.parse_warning()
            logging.warning(err, debug)
        return True

    def quit(self):
        self._pipeline.set_state(Gst.State.NULL)
        return self.loop.quit()
