import sys
from text_utils import center_text, typewriter, clear_screen
from colorama import Fore, Style
from new_game import character_creation

def death_screen():
    clear_screen()
    print("")
    typewriter(center_text(Fore.RED + "YOU DIED" + Style.RESET_ALL))
    print("")
    print(center_text("- Restart -"))
    print(center_text("- Quit -"))
    option = input(Fore.YELLOW + "> ").lower()
    while option not in ['restart', 'quit']:
        print(Fore.RED + "Invalid input! Please use a Valid Command!\n")
        option = input(Fore.YELLOW + "> ").lower()
        if option == "restart":
            character_creation()
            break
        elif option == "quit":
            sys.exit()