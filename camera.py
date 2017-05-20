#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Webcam api wrapper
"""
import cv2
import threading


class CameraWrapper(object):
    """
    A basic wrapper for opencv python camera API
    """
    _loop_thread = None
    _keep_the_loop_running = None

    def __init__(self, camera_id):
        """
        Initialize selected camera and a preview window.
        :type camera_id: int
        """
        self._keep_the_loop_running = True
        camera = cv2.VideoCapture(camera_id)
        if not camera.isOpened():
            raise IOError("Failed to open camera with id " + str(camera_id))
        self._loop_thread = threading.Thread(target=self._the_loop, args=(camera,))
        self._loop_thread.start()

    def _the_loop(self, camera):
        """The main loop of the preview intended to be run in a separate thread.
        :param: Video source"""
        while camera.isOpened() and self._keep_the_loop_running:
            ret, frame = camera.read()
            cv2.imshow("frame", frame)
            time.sleep(1.0/30.0)
            # without waitKey the gui will not show up
            cv2.waitKey(1)

        self._vc.release()
        # Try kicking the windows main loop and killing it. This is a known problem with the openCV
        for _ in range(10):
            cv2.waitKey(1)
            cv2.destroyWindow("frame")

    def take_picture(self, output_file_path):
        """Save jpg picture from the camera to file specified by the parameter
        :type output_file_path: str"""
        raise NotImplementedError

    def close(self):
        """Stop the camera and destroy the preview"""
        self._keep_the_loop_running = False
        self._loop_thread.join()

if __name__=="__main__":
    print "PyInwentaryzator.camera - module responsible for making photos using a webcam."
    import time
    for x in range(10):
        c = CameraWrapper(x)
        time.sleep(10)
        c.close()