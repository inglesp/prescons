# presentation console
# - a python interpreter for "pseudo-interative" demos
#
# usage: $ python prescons.py <filename>
#
# <filename> should be a file that contains python code as would be entered
# directly in a terminal - see example.py
#
# while running, press 'space' to move through the code
#
# github.com/inglesp/prescons

from code import InteractiveConsole
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import sys

# get character from stdin
# based on http://code.activestate.com/recipes/134892/
try:
    # *nix
    import termios, tty
    def getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        gotch = None
        try:
            tty.setraw(fd)
            gotch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return gotch
except ImportError:
    # Windows
    import msvcrt
    def getch():
        return msvcrt.getch()

class PresentationConsole(InteractiveConsole):
    def __init__(self, path):
        self.file = open(path)
        InteractiveConsole.__init__(self)

    def raw_input(self, prompt=''):
        line = self.file.readline()
        if len(line) == 0:
            self.file.close()
            raise EOFError
        if line.startswith('#!'):
            line = line[2:]
        else:
            self.write(prompt)
            sys.stderr.flush()
            if prompt == sys.ps1:
                self.get_user_input()
            self.write(line)
        return line.rstrip()

    def runcode(self, code):
        sys.stdout, sys.stderr = StringIO(), StringIO()
        InteractiveConsole.runcode(self, code)
        output, errors = sys.stdout.getvalue(), sys.stderr.getvalue()
        sys.stdout, sys.stderr = sys.__stdout__, sys.__stderr__
        if len(output) > 0:
            self.get_user_input()
            self.write(output)
        if len(errors) > 0:
            self.get_user_input()
            self.write(errors)

    def get_user_input(self):
        while True:
            if getch() == ' ':
                break


if __name__ == '__main__':
    path = sys.argv[1]
    console = PresentationConsole(path)
    console.interact()
