#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Webcam api wrapper
"""
import cv2
import threading
import time
import Queue


class CameraWrapper(object):
    """
    A basic wrapper for opencv python camera API
    :ivar _message_queue: Internal message queue used to communicate with the main loop. Messages format is: 
                            (<return event>, <message>, *<args)
    :ivar _loop_thread: The main thread containing the main loop
    """
    class Messages(object):
        """List of messages supported by the main loop"""
        TAKE_PHOTO = "photo"
        STOP = "DIE"

    _loop_thread = None
    _message_queue = None

    def __init__(self, camera_id):
        """
        Initialize selected camera and a preview window.
        :type camera_id: int
        """
        self._message_queue = Queue.Queue()
        self._keep_the_loop_running = True
        camera = cv2.VideoCapture(camera_id)
        if not camera.isOpened():
            raise IOError("Failed to open camera with id " + str(camera_id))
        self._loop_thread = threading.Thread(target=self._the_loop, args=(camera,))
        self._loop_thread.start()

    def _the_loop(self, camera):
        """The main loop of the preview intended to be run in a separate thread.
        :param: Video source"""
        while camera.isOpened():

            if not self._message_queue.empty():
                message = self._message_queue.get_nowait()
                return_event, command, args = message[0], message[1], message[2:]
                if command == CameraWrapper.Messages.STOP:
                    break
                if command == CameraWrapper.Messages.TAKE_PHOTO:
                    ret, frame = camera.read()
                    cv2.imwrite(args[0], frame)
                    self._message_queue.task_done()
                    return_event.set()

            ret, frame = camera.read()
            cv2.imshow("frame", frame)
            time.sleep(1.0/30.0)
            # without waitKey the gui will not show up
            cv2.waitKey(1)

        camera.release()
        # Try kicking the windows main loop and killing it. This is a known problem with the openCV
        for _ in range(10):
            cv2.waitKey(1)
            cv2.destroyWindow("frame")
        # Resume the thread that sent the STOP message
        self._message_queue.task_done()
        return_event.set()

    def _send_message_sync(self, *args):
        """Send the massage to the main loop and wait for the completion signal.
        :param args: message name and list of arguments for the message
        """
        return_event = threading.Event()
        self._message_queue.put((return_event,) + tuple(args))
        return_event.wait()

    def take_picture(self, output_file_path):
        """Save jpg picture from the camera to file specified by the parameter
        :type output_file_path: str"""
        self._send_message_sync(CameraWrapper.Messages.TAKE_PHOTO, output_file_path)

    def close(self):
        """Stop the camera and destroy the preview"""
        self._send_message_sync(CameraWrapper.Messages.STOP)

if __name__ == "__main__":
    print "PyInwentaryzator.camera - module responsible for making photos using a webcam."

    for x in range(10):
        print "Trying to open camera number ", x
        try:
            c = CameraWrapper(x)
        except Exception as e:
            print "Failed to open camera number ", x, " because:"
            print str(e)
        else:
            time.sleep(1)
            c.take_picture("/tmp/test" + str(x) + ".jpg")
            time.sleep(1)
            c.close()
