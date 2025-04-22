import sys
from text_utils import center_text, typewriter, clear_screen
from colorama import Fore, Style
import msvcrt
import os
from game_data import *
import shutil

def death_screen():
    clear_screen()
    print("")
    typewriter(center_text(Fore.RED + "YOU DIED" + Style.RESET_ALL))
    print("")
    print(center_text("- Restart -"))
    print(center_text("- Quit -"))

    option = input(Fore.YELLOW + "> ").lower()
    while option not in ['restart', 'quit']:
        print(Fore.RED + "Invalid input! Please use a valid command!\n")
        option = input(Fore.YELLOW + "> ").lower()

    if option == "restart":
        from title import title_screen
        title_screen()
    elif option == "quit":
        sys.exit()

def show_character_sheet(player,clear_screen=True):
    if clear_screen == True:
        os.system('cls' if os.name == 'nt' else 'clear')

    width = shutil.get_terminal_size().columns
    line = '-' * width
    
    title = " CHARACTER SHEET "
    title_bar = '-' * ((width - len(title)) // 2 - 1) + title + '-' * ((width - len(title)) // 2 - 1)

    print(Fore.MAGENTA + title_bar)
    print("")

    # Basic Info
    print(Fore.YELLOW + "Name".ljust(15) + ": " + str(player.name))
    print(Fore.YELLOW + "Difficulty".ljust(15) + ": " + str(difficulty))
    print("")
    
    # Combat Stats
    print(Fore.GREEN + "HP".ljust(15) + ": " + str(player.hp) + " / " + str(player.max_hp))
    print(Fore.CYAN + "Strength".ljust(15) + ": " + str(player.strength))
    print(Fore.RED + "Defense".ljust(15) + ": " + str(player.defense))
    print(Fore.BLUE + "Speed".ljust(15) + ": " + str(player.speed))
    print("")
    
    # Intelligence & Money
    print(Fore.WHITE + "Intelligence".ljust(15) + ": " + str(player.intelligence))
    print(Fore.GREEN + "Money".ljust(15) + ": $" + str(player.money))
    print("")

    print(Fore.MAGENTA + line)
    print(Style.RESET_ALL)

    print(Fore.YELLOW + "\nPress any key to continue...")
    msvcrt.getch()