import os
import platform

from termcolor import colored

if platform.system() == "Windows":
    os.environ['TERM'] = 'xterm-color'
    from colorama import init
    init()

def log(message, color="green"):
    print(colored(message, color))