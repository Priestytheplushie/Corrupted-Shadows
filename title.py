import os
import sys
import time
from colorama import Fore
from new_game import character_creation
from text_utils import animate_title, center_text

def credits_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    animate_title(Fore.MAGENTA + "=== CREDITS ===")
    print("")
    animate_title(Fore.LIGHTGREEN_EX + "A Game by: ")
    time.sleep(1)
    animate_title(Fore.YELLOW + "░▒▓█ PRIESTY █▓▒░")
    print("")
    time.sleep(3)
    title_screen()

def title_screen():
    os.system('cls' if os.name == 'nt' else 'clear') 
    animate_title(Fore.MAGENTA + "Corrupted Shadows")
    print(center_text(Fore.WHITE + ""))
    print(center_text("- Play -"))
    print(center_text("- Credits -"))
    print(center_text("- Quit -"))
    
    option = input(Fore.YELLOW + "> ").lower()
    while option not in ['play', 'credits', 'quit']:
        print(Fore.RED + "Invalid input! Please use a valid command!\n")
        option = input(Fore.YELLOW + "> ").lower()

    if option == "play":
        return character_creation()
    elif option == "credits":
        credits_screen()
    elif option == "quit":
        sys.exit()