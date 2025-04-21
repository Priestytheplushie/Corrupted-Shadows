from colorama import Fore, Back, Style
import os
import sys
import shutil
import re
import time
from new_game import character_creation
from text_utils import *


def credits_screen():
    os.system('cls' if os.name == 'nt' else 'clear') 
    animate_title(Fore.MAGENTA+"Credits")
    print("")
    animate_title(Fore.LIGHTGREEN_EX+"Game by Priesty")   
    time.sleep(3)
    title_screen()

def title_screen():
    os.system('cls' if os.name == 'nt' else 'clear') 
    animate_title(Fore.MAGENTA+"Priesty's Quest")
    print(center_text(Fore.WHITE + ""))
    print(center_text("- Play -"))
    print(center_text("- Credits -"))
    print(center_text("- Quit -"))
    
    option = input(Fore.YELLOW + "> ").lower()
    while option not in ['play', 'credits', 'quit']:
        print(Fore.RED + "Invalid input! Please use a Valid Command!\n")
        option = input(Fore.YELLOW + "> ").lower()

    if option == "play":
        character_creation()
    elif option == "credits":
        credits_screen()
    elif option == "quit":
        sys.exit()