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

    print(center_text(Fore.WHITE + "╔════════════════════════════════╗"))
    print(center_text("║ " + Fore.CYAN + "1. Text Speed" + Fore.WHITE + f" [{text_speed.capitalize()}]     ║"))
    print(center_text("║ " + Fore.CYAN + "2. Back to Main Menu" + Fore.WHITE + "           ║"))
    print(center_text("╚════════════════════════════════╝"))

    choice = input(Fore.YELLOW + "\nEnter choice (1-2): ").strip()

    while choice not in ['1', '2']:
        print(Fore.RED + "Invalid input! Please enter 1 or 2.")
        choice = input(Fore.YELLOW + "\nEnter choice (1-2): ").strip()

    if choice == '1':
        return change_text_speed()
    elif choice == '2':
        print(Fore.CYAN + "Returning to main menu...")
        time.sleep(1)
        return "back_to_main_menu"


def change_text_speed():
    update_presence("In Options", "Adjusting text speed")
    global text_speed
    os.system('cls' if os.name == 'nt' else 'clear')
    animate_title(Fore.MAGENTA + "Text Speed Settings")

    options = ['Slow', 'Normal', 'Fast', 'Very Fast', 'Fastest']
    current = text_speed.capitalize()

    print(center_text(Fore.WHITE + "╔════════════════════════════════╗"))
    for i, option in enumerate(options, 1):
        selected = " (Current)" if option.lower() == text_speed else ""
        print(center_text("║ " + Fore.CYAN + f"{i}. {option}" + Fore.WHITE + f"{selected:<22}║"))
    print(center_text("║ " + Fore.CYAN + "6. Back to Options" + Fore.WHITE + "             ║"))
    print(center_text("╚════════════════════════════════╝"))

    choice = input(Fore.YELLOW + "\nSelect a number (1-6): ").strip()

    while choice not in [str(i) for i in range(1, 7)]:
        print(Fore.RED + "Invalid input! Please enter a number between 1 and 6.")
        choice = input(Fore.YELLOW + "\nSelect a number (1-6): ").strip()

    if choice == '6':
        return "back_to_options"

    new_speed = options[int(choice) - 1].lower()
    text_speed = new_speed
    print(Fore.GREEN + f"Text speed set to {new_speed.capitalize()}.")
    time.sleep(1.5)
    return "text_speed_changed"


def title_screen():
    global tower
    os.system('cls' if os.name == 'nt' else 'clear')

    animate_title(Fore.MAGENTA + "Corrupted Shadows")

    splash, discord_splash = get_random_splash()
    update_presence("In the Title Screen", discord_splash)

    print(center_text(Fore.YELLOW + splash))
    print(center_text(Fore.WHITE + "v0.4.1"))
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

    if option == "play" or option == "1":
        return character_creation()
    elif option == "tower" or option == "2":
        return create_tower_run()
    elif option == "credits" or option == "3":
        credits_screen()
        return title_screen()
    elif option == "options" or option == "4":
        result = display_options_menu()
        return title_screen()  # Always return after options
    elif option == "quit" or option == "5":
        confirm = input(Fore.RED + "Are you sure you want to quit? (yes/no) > ").lower().strip()
        if confirm == "yes":
            disconnect_from_discord()
            sys.exit()
        else:
            return title_screen()
