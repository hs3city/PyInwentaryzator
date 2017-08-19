from unicurses import keyname, getch, initscr, noecho, cbreak, curs_set, keypad, \
    endwin, nocbreak, echo, getmaxyx, mvaddstr


class UserInput(object):
    def next(self):
        return keyname(getch())
    
    def __iter__(self):
        return self


class CursesScreen(object):
    _LOG_CONSOLE_SIZE = 10
    _log_console = ["" for _ in range(_LOG_CONSOLE_SIZE)]

    def __enter__(self):
        self.stdscr = initscr()
        noecho()
        cbreak()
        curs_set(0)
        keypad(self.stdscr, True)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        endwin()
        nocbreak()
        keypad(self.stdscr, False)
        echo()
    
    def log(self, msg):
        self._log_console.append(msg)
        self._log_console = self. _log_console[1:self._LOG_CONSOLE_SIZE]
        height, width = getmaxyx(self.stdscr)
        y_pos = height - len(self._log_console) - 1
        mvaddstr(y_pos - 1, 1, "DEBUG:")
    
        for offset in range(len(self._log_console)):
            mvaddstr(y_pos + offset, 1, self._log_console[offset][0:width - 2])
