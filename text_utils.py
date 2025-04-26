import os
import sys
import shutil
import re
import time
from colorama import Fore
import random
from game_data import text_speed

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
    global text_speed
    if text_speed == "slow":
        delay = 0.1
    elif text_speed == "normal":
        delay = 0.05
    elif text_speed == "fast":
        delay = 0.02
    elif text_speed == "very fast":
        delay = 0.005
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def corruption_effect(text, corruption_delay=0.1, corruption_chance=0.1, corruption_duration=3):
    corruption_start = len(text) // 2
    corruption_end = corruption_start + corruption_duration

    print(text, end='', flush=True)
    
    for i, char in enumerate(text):
        if i >= corruption_start and i < corruption_end:
            if random.random() < corruption_chance:
                corrupted_char = random.choice(['#', '@', '%', '&', '$', '!', '?', '^', '~', '*'])
                sys.stdout.write(f'\r{text[:i]}{corrupted_char}{text[i+1:]}')
            else:
                sys.stdout.write(f'\r{text[:i+1]}{text[i+1:]}')
        time.sleep(corruption_delay)

    sys.stdout.write("\r" + text + "\n")

def dice_roll_animation(stat_name, stat_value):
    print(Fore.CYAN + "Rolling " + stat_name + "...", end="\r")
    sys.stdout.flush()
    for i in range(5):
        roll = random.randint(1, 6)
        print(Fore.CYAN + "Rolling " + stat_name + ": " + str(roll) + "  ", end="\r")
        time.sleep(0.2)
    print(Fore.CYAN + stat_name + " roll completed: " + str(stat_value) + "     ")
    time.sleep(1)