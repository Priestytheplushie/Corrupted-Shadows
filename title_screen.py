from colorama import Fore, Back, Style
import os
import shutil
import re
from new_game import character_creation

ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

def center_text(text):
    visible_text = ansi_escape.sub('', text)
    terminal_width = shutil.get_terminal_size().columns
    spaces_needed = (terminal_width - len(visible_text)) // 2
    return ' ' * spaces_needed + text

def title_screen():
    os.system('cls' if os.name == 'nt' else 'clear') 
    print(center_text(Fore.MAGENTA+"Priesty's Quest"))
    print(center_text(Fore.WHITE+""))
    print(center_text("- Play -"))
    print(center_text("- Credits -"))
    print(center_text("- Quit -"))
    Fore.YELLOW
    option = input(Fore.YELLOW+"> ")
    if option.lower == "play":
        character_creation()
    elif option.lower == "credits":
        credits()
