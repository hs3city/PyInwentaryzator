#!/usr/bin/env python
from getch import getch
from camera import CameraWrapper

print("Witaj inwentaryzatorze!")

#with open('./data.csv', 'a') as data_file:

#print("Goodbye")


def choose_camera():
  def change_camera(current_camera, next_camera, opened_camera):
    """try to open and return the next camera. In case of failure open current
    :type current: int
    :type next_camera: int
    :param current: index of the currently opened camera
    :param next_camera: index of the currently opened camera
    :return: tuple containing opened camera id and instance of the CameraWrapper"""
    opened_camera.close()
    try:
      return next_camera, CameraWrapper(next_camera)
    except:
      return current_camera, CameraWrapper(current_camera)


  choosen_camera = 0
  camera_instance = CameraWrapper(choosen_camera)
  _exit = False
  actions = {
    'j': lambda: change_camera(choose_camera, choosen_camera+1, camera_instance),
    'k': lambda: change_camera(choose_camera, choosen_camera-1, camera_instance),
    '\r': lambda: None,
  }
  while _exit == False:
    print("press [j]/[k] to switch to next/previous camera, or enter to accept the current one")
    try:
      choosen_camera, camera_instance = actions[getch()]()
    except KeyError:
      print "unknown command, please try again"



camera = choose_camera()
