import os
import sys
import shutil
import re
import time
from colorama import Fore
import random
from pynput import keyboard


skip_typing = False

def on_press(key): # for skipping
    global skip_typing
    if key == keyboard.Key.space:
        skip_typing = True
        
listener_started = False
    

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
        smart_sleep(delay)
        padding = ''
    print()

def typewriter(text, delay=0.05):
    global skip_typing, listener_started

    skip_typing = False  

    if not listener_started:
        listener = keyboard.Listener(on_press=on_press)
        listener.daemon = True
        listener.start()
        listener_started = True

    for i, char in enumerate(text):
        print(char, end='', flush=True)
        smart_sleep(delay, reset_skip=False)  
        if skip_typing:
            print(text[i+1:], end='', flush=True)
            break
    print()

def smart_sleep(seconds, check_interval=0.01, reset_skip=True):
    global skip_typing
    start = time.time()
    while time.time() - start < seconds:
        if skip_typing:
            break
        time.sleep(check_interval)
    if reset_skip:
        skip_typing = False 

    

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
        smart_sleep(corruption_delay)

    sys.stdout.write("\r" + text + "\n")

def dice_roll_animation(stat_name, stat_value):
    print(Fore.CYAN + "Rolling " + stat_name + "...", end="\r")
    sys.stdout.flush()
    for i in range(5):
        roll = random.randint(1, 6)
        print(Fore.CYAN + "Rolling " + stat_name + ": " + str(roll) + "  ", end="\r")
        smart_sleep(0.2)
    print(Fore.CYAN + stat_name + " roll completed: " + str(stat_value) + "     ")
    smart_sleep(1)