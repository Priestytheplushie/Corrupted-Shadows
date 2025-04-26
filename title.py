import os
import sys
import time
from colorama import Fore
from new_game import character_creation
from text_utils import animate_title, center_text, clear_screen
from game_data import * 

def credits_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    animate_title(Fore.MAGENTA + "=== CREDITS ===")
    print("")
    animate_title(Fore.LIGHTGREEN_EX + "A Game by: ")
    time.sleep(1)
    animate_title(Fore.YELLOW + "░▒▓█ PRIESTY █▓▒░")
    print("")
    time.sleep(3)
    return

def display_options_menu():
    global text_speed
    os.system('cls' if os.name == 'nt' else 'clear')
    animate_title(Fore.MAGENTA + "Options")
    print(center_text(Fore.WHITE + ""))
    print(center_text("- Text Speed: " + Fore.YELLOW + text_speed.capitalize() + " -"))
    print(center_text("- Back to Main Menu -"))
    
    option = input(Fore.YELLOW + "> ").lower()
    while option not in ['text speed', 'back to main menu']:
        print(Fore.RED + "Invalid input! Please use a valid command!\n")
        option = input(Fore.YELLOW + "> ").lower()

    if option == "text speed":
        return change_text_speed()  
    elif option == "back to main menu":
        print(Fore.CYAN + "Returning to main menu...")
        time.sleep(1)
        return "back_to_main_menu" 

def change_text_speed():
    global text_speed
    os.system('cls' if os.name == 'nt' else 'clear')
    animate_title(Fore.MAGENTA + "Select Text Speed")
    print(center_text(Fore.WHITE + ""))
    print(center_text("- Slow -"))
    print(center_text("- Normal (Current) -"))
    print(center_text("- Fast -"))
    print(center_text("- Very Fast -"))
    print(center_text("- Back to Options -"))

    choice = input(Fore.YELLOW + "> ").lower()
    while choice not in ['slow', 'normal', 'fast', 'very fast', 'back to options']:
        print(Fore.RED + "Invalid input! Please use a valid command!\n")
        choice = input(Fore.YELLOW + "> ").lower()

    if choice == "slow":
        text_speed = "slow"
        print(Fore.GREEN + "Text speed set to Slow.")
        time.sleep(1)
    elif choice == "normal":
        text_speed = "normal"
        print(Fore.GREEN + "Text speed set to Normal.")
        time.sleep(1)
    elif choice == "fast":
        text_speed = "fast"
        print(Fore.GREEN + "Text speed set to Fast.")
        time.sleep(1)
    elif choice == "very fast":
        text_speed = "very fast"
        print(Fore.GREEN + "Text speed set to Very Fast.")
        time.sleep(1)
    elif choice == "back to options":
        return "back_to_options" 

    return "text_speed_changed"  



def title_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    animate_title(Fore.MAGENTA + "Corrupted Shadows")
    print(center_text(Fore.WHITE + ""))
    print(center_text("- Play -"))
    print(center_text("- Credits -"))
    print(center_text("- Options -"))
    print(center_text("- Quit -"))
    
    option = input(Fore.YELLOW + "> ").lower()
    while option not in ['play', 'credits', 'options', 'quit']:
        print(Fore.RED + "Invalid input! Please use a valid command!\n")
        option = input(Fore.YELLOW + "> ").lower()

    if option == "play":
        return character_creation()  
    elif option == "credits":
        credits_screen()
    elif option == "options":
        result = display_options_menu()
        if result == "back_to_main_menu":
            return None  
        elif result == "text_speed_changed":
            return title_screen() 
    elif option == "quit":
        sys.exit()
