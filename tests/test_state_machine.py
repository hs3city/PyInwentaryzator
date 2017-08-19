from . import *
from tests.mock_utils import log, UserIputMock, text_input
from state_machine import run_state_machine


states_map = {
    'state1': {
        'n': lambda state, input_generator: ('state2', state),
        'e': lambda state, input_generator: ('text_input', state)
    },
    'state2': {
            'p': lambda state, input_generator: ('state1', state)
        },
    'text_input': {
            '*': text_input
        },
}
        
        
class StateMachineTests(TestCase):
    def test_single_transition(self):
        end_state_name, end_state_data = run_state_machine(
            states_map,
            'state1',
            log,
            UserIputMock("n"),
            default_state_data=None)
        self.assertEqual(end_state_name, 'state2')

    def test_no_transition(self):
        end_state_name, end_state_data = run_state_machine(
            states_map,
            'state1',
            log,
            UserIputMock("x"),
            default_state_data=None)
        self.assertEqual(end_state_name, 'state1')
        
    def test_multiple_transitions_1(self):
        end_state_name, end_state_data = run_state_machine(
            states_map,
            'state1',
            log,
            UserIputMock("npnp"),
            default_state_data=None)
        self.assertEqual(end_state_name, 'state1')
        
    def test_multiple_transitions_2(self):
        end_state_name, end_state_data = run_state_machine(
            states_map,
            'state1',
            log,
            UserIputMock("npnpn"),
            default_state_data=None)
        self.assertEqual(end_state_name, 'state2')
        
    def test_text_input(self):
        end_state_name, end_state_data = run_state_machine(
            states_map,
            'state1',
            log,
            UserIputMock("eTHIS IS A TEXT\n\n"),
            default_state_data=None)
        self.assertEqual(end_state_data, "THIS IS A TEXT")
