def log(msg):
    print msg


def text_input(state, input_generator, char):
    """
    Swallow all input up to "\n\n" sequence.
    :param state:
    :param input_generator: iterable
    :param char:
    :return: swallowed input
    """
    state = state or ''
    state += char
    if state[-2:] == '\n\n':
        return 'state1', state[0:-2]
    return 'text_input', state


class UserIputMock(object):
    def __init__(self, data):
        self.data = data
        self._offset = 0
    
    def __iter__(self):
        return self
    
    def next(self):
        self._offset += 1
        if self._offset > len(self.data):
            raise StopIteration
        return self.data[self._offset - 1]