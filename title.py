import os
import sys
import time
from colorama import Fore
from new_game import character_creation
from tower.tower_creation import create_tower_run
from text_utils import animate_title, center_text, clear_screen
from game_data import * 
from discord import connect_to_discord, update_presence, disconnect_from_discord
import random
from strings import splash_messages, get_random_splash

def credits_screen():
    update_presence(
        state="Viewing Credits",
        details="Game by Priesty, Launcher by Donut",
        large_image="corrupted_shadows",
        large_text="Corrupted Shadows",
        small_image="priesty",
        small_text="Game by Priesty",
    )

    os.system('cls' if os.name == 'nt' else 'clear')
    animate_title(Fore.MAGENTA + "=== CREDITS ===")
    print("")
    animate_title(Fore.LIGHTGREEN_EX + "A Game by: ")
    time.sleep(1)
    animate_title(Fore.YELLOW + "░▒▓█ PRIESTY █▓▒░")
    time.sleep(1)
    animate_title(Fore.LIGHTGREEN_EX + "Launcher By:")
    time.sleep(1)
    animate_title(Fore.YELLOW + "░▒▓█ Donut █▓▒░")
    print("")
    time.sleep(3)
    return

def display_options_menu():
    update_presence("In Options", "Adjusting Game Settings")
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
    update_presence("In Options", "Adjusting text speed")
    global text_speed
    os.system('cls' if os.name == 'nt' else 'clear')
    animate_title(Fore.MAGENTA + "Select Text Speed")
    print(center_text(Fore.WHITE + ""))
    print(center_text("- Slow -"))
    print(center_text("- Normal (Current) -"))
    print(center_text("- Fast -"))
    print(center_text("- Very Fast -"))
    print(center_text("- Fastest -"))
    print(center_text("- Back to Options -"))

    choice = input(Fore.YELLOW + "> ").lower()
    while choice not in ['slow', 'normal', 'fast', 'very fast', 'fastest', 'back to options']:
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
    elif choice == "fastest":
        text_speed = "fastest"
        print(Fore.GREEN + "Text speed set to Fastest.")
        time.sleep(2)
    elif choice == "back to options":
        return "back_to_options" 

    return "text_speed_changed"  

def title_screen():
    global tower
    os.system('cls' if os.name == 'nt' else 'clear')

    animate_title(Fore.MAGENTA + "Corrupted Shadows")

    splash, discord_splash = get_random_splash()
    update_presence("In the Title Screen", discord_splash)

    print(center_text(Fore.YELLOW + splash))
    print(center_text(Fore.WHITE + "v0.4.0"))
    print(center_text(""))
    print(center_text("- Play -"))
    print(center_text("- Tower -"))
    print(center_text("- Credits -"))
    print(center_text("- Options -"))
    print(center_text("- Quit -"))

    option = input(Fore.YELLOW + "> ").lower().strip()
    while option not in ['play', 'tower', 'credits', 'options', 'quit']:
        print(Fore.RED + "Invalid input! Please use a valid command!\n")
        option = input(Fore.YELLOW + "> ").lower().strip()

    if option == "play":
        return character_creation()
    elif option == "tower":
        return create_tower_run()
    elif option == "credits":
        credits_screen()
        return title_screen()
    elif option == "options":
        result = display_options_menu()
        return title_screen()  # Always return after options
    elif option == "quit":
        confirm = input(Fore.RED + "Are you sure you want to quit? (yes/no) > ").lower().strip()
        if confirm == "yes":
            disconnect_from_discord()
            sys.exit()
        else:
            return title_screen()
