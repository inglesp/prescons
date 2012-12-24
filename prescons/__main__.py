import sys

from prescons import PseudoInteractiveConsole

path = sys.argv[1]
console = PseudoInteractiveConsole(path)
console.interact()
