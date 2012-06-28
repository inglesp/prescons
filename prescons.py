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
from StringIO import StringIO
import sys, termios, tty

# get character from stdin
# based on http://code.activestate.com/recipes/134892/
# *nix only, and doesn't handle arrow keys well
def getch(ch=None):
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        while True:
            tty.setraw(fd)
            gotch = sys.stdin.read(1)
            if ch is None or gotch == ch:
                break
            if ord(gotch) == 3:
                raise KeyboardInterrupt
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

# subclasses InteractiveConsole from code module
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
            if prompt == sys.ps1:
                getch(' ')
            self.write(line)
        return line.rstrip()

    def runcode(self, code):
        sys.stdout, sys.stderr = StringIO(), StringIO()
        InteractiveConsole.runcode(self, code)
        output, errors = sys.stdout.getvalue(), sys.stderr.getvalue()
        sys.stdout, sys.stderr = sys.__stdout__, sys.__stderr__
        if len(output) > 0:
            getch(' ')
            self.write(output)
        if len(errors) > 0:
            getch(' ')
            self.write(errors)

if __name__ == '__main__':
    path = sys.argv[1]
    console = PresentationConsole(path)
    console.interact()
