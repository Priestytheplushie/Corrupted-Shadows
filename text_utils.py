import os
import sys
import shutil
import re
import time
from colorama import Fore

ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def center_text(text):
    visible_text = ansi_escape.sub('', text)
    terminal_width = shutil.get_terminal_size().columns
    spaces_needed = (terminal_width - len(visible_text)) // 2
    return ' ' * spaces_needed + text

def animate_title(text, delay=0.1):
    terminal_width = shutil.get_terminal_size().columns
    visible_text = ansi_escape.sub('', text)
    spaces_needed = (terminal_width - len(visible_text)) // 2
    padding = ' ' * spaces_needed

    for char in text:
        print(padding + char, end='', flush=True)
        time.sleep(delay)
        padding = ''
    print()

def typewriter(text, delay=0.05):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()