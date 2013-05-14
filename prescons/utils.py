import platform
import subprocess

def clear_screen():
    if platform.system() == 'Windows':
        subprocess.call('cls')
    else:
        subprocess.call('clear')
