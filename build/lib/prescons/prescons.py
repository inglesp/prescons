from code import InteractiveConsole

try:
    # python2
    from StringIO import StringIO
except ImportError:
    # python3
    from io import StringIO

import os.path, sys

try:
    # python2
    input = raw_input
except NameError:
    # python3
    pass

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
        full_path = os.path.join(os.getcwd(), path)
        sys.path.append(os.path.dirname(full_path))
        self.file = open(path)
        InteractiveConsole.__init__(self)

    def switch_mode(self):
        transitions = {
            RealInteractiveConsole: PseudoInteractiveConsole,
            PseudoInteractiveConsole: RealInteractiveConsole
        }

        print('')
        print('switching mode!')
        self.__class__ = transitions[self.__class__]

    def raw_input(self, prompt=''):
        try:
            return self.get_raw_input(prompt)
        except KeyboardInterrupt:
            self.switch_mode()
            return ''

class PseudoInteractiveConsole(PresentationConsole):
    def get_raw_input(self, prompt):
        self.write(prompt)
        sys.stderr.flush()
        if prompt == sys.ps1:
            self.wait_for_user_input()
        line = self.file.readline()
        if len(line) == 0:
            self.file.close()
            raise EOFError
        self.write(line)
        return line.rstrip()

    def runcode(self, code):
        sys.stdout, sys.stderr = StringIO(), StringIO()
        InteractiveConsole.runcode(self, code)
        output, errors = sys.stdout.getvalue(), sys.stderr.getvalue()
        sys.stdout, sys.stderr = sys.__stdout__, sys.__stderr__
        if output or errors:
            self.wait_for_user_input()
        if output:
            self.write(output)
        if errors:
            self.write(errors)

    def wait_for_user_input(self):
        while True:
            gotch = getch()
            if gotch == ' ':
                break
            elif ord(gotch) == 3:
                # Ctrl-C
                raise KeyboardInterrupt
            elif ord(gotch) in (4, 26):
                # Ctrl-D or Ctrl-Z
                print('')
                raise SystemExit

class RealInteractiveConsole(PresentationConsole):
    def get_raw_input(self, prompt):
        return input(prompt)

if __name__ == '__main__':
    path = sys.argv[1]
    console = PseudoInteractiveConsole(path)
    console.interact()

