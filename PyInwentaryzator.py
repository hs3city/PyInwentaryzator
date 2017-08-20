#!/usr/bin/env python
from curses_utils import UserInput, CursesScreen
from state_machine import run_state_machine
from camera import CameraWrapper
import re


def is_alfa_num(char):
    return re.match('^[\w]$', char) is not None

camera = None

def next_camera_state(state, log):
    global camera
    camera = switch_camera(camera, camera.camera_index+1)
    return CAMERA_MENU, state


def prev_camera_state(state, log):
    global camera
    camera = switch_camera(camera, camera.camera_index-1)
    return CAMERA_MENU, state


def switch_camera(old_camera, desired_camera_index):
    """
    Try to open and return camera with selected index. In case of any problems
    reopens and returns old camera.
    :raises: None
    :type old_camera: CameraWrapper
    :int desired_camera_index: CameraWrapper
    :rtype: CameraWrapper
    """
    old_camera_index = old_camera.camera_index
    old_camera.close()
    del old_camera
    try:
        return CameraWrapper(desired_camera_index)
    finally:
        return CameraWrapper(old_camera_index)


def goto_state(name):
    return lambda state, log: (name, state)

MAIN = 'main'
CAMERA_MENU = 'camera_menu'
RECORD_INPUT = 'record_input'
SAVE_RECORD = 'save_record'


def record_input_state(state, char):
    """
    
    :type state: dict
    :param log: log method    :param char:
    :return:
    """
    state.setdefault('user_input', "")
    if char == '^J':
        state['user_input'] += '\n'
    if is_alfa_num(char) or char in '#@':
        state['user_input'] += char
    elif char == 'KEY_BACKSPACE':
        pass
        
    if state['user_input'][-2:] == '\n\n':
        state['user_input'] = state['user_input'][:-2]
        return SAVE_RECORD, state
        
    return RECORD_INPUT, state

states_map = {
    MAIN: {
        'e': lambda state, log: exit(0),
        'c': goto_state(CAMERA_MENU),
        'a': goto_state(RECORD_INPUT),
    },
    CAMERA_MENU: {
        'j': next_camera_state,
        'k': prev_camera_state,
        '^[': goto_state(MAIN)
    },
    RECORD_INPUT: {
        '*': record_input_state
    }
    
}

if __name__ == "__main__":
    camera = CameraWrapper(0)
    try:
        with CursesScreen() as screen:
            exit_state_name, exit_data = \
                    run_state_machine(states_map, MAIN, screen.log, UserInput(),
                                      default_state_data={})
    finally:
        camera.close()

