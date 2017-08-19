#!/usr/bin/env python
from curses_utils import UserInput, CursesScreen
from state_machine import run_state_machine

MAIN = 'main'

states_map = {
    MAIN: {
        'e': lambda state, input_generator: exit(0)
        
    }
}

if __name__ == "__main__":
    with CursesScreen() as screen:
        exit_state_name, exit_data = run_state_machine(states_map, MAIN,
                                                       screen.log, UserInput(),
                                                       default_state_data=None)

