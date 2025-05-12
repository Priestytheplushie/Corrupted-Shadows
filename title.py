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
from shadow_gauntlets.gauntlet_selection import gauntlet_selection
import threading

play_menu_cycle_thread = None
stop_cycle = False

credits_cycle_thread = None
stop_credits_cycle = False

def cycle_play_menu_presence():
    from discord import update_presence  # If not already imported at the top
    import time

    modes = [
        ("Choosing a Game Mode", "1/3. Campaign"),
        ("Choosing a Game Mode", "2/3. Tower Mode"),
        ("Choosing a Game Mode", "3/3. Shadow Gauntlets"),
    ]

    i = 0
    while not stop_cycle:
        state, details = modes[i % len(modes)]
        update_presence(state=state, details=details)
        i += 1
        time.sleep(6)  # Delay between cycles

def cycle_credits_presence():
    from discord import update_presence
    import time

    modes = [
        {
            "state": "Viewing Credits",
            "details": "Game by Priesty",
            "large_image": "corrupted_shadows",
            "large_text": "Corrupted Shadows",
            "small_image": "priesty",
            "small_text": "Game by Priesty"
        },
        {
            "state": "Viewing Credits",
            "details": "Launcher by Donut",
            "large_image": "corrupted_shadows",
            "large_text": "Corrupted Shadows",
            "small_image": "donut",
            "small_text": "Special Thanks to Donut"
        }
    ]

    i = 0
    while not stop_credits_cycle:
        presence = modes[i % 2]
        update_presence(**presence)
        time.sleep(5)
        i += 1

def credits_screen():
    global credits_cycle_thread, stop_credits_cycle

    stop_credits_cycle = False
    credits_cycle_thread = threading.Thread(target=cycle_credits_presence, daemon=True)
    credits_cycle_thread.start()

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
    input((center_text(Fore.YELLOW + "Press any button to continue")))

    stop_credits_cycle = True
    if credits_cycle_thread:
        credits_cycle_thread.join(timeout=1)
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

def play_menu():
    global stop_cycle, play_menu_cycle_thread
    stop_cycle = False

    # Start the presence cycling in a separate thread
    play_menu_cycle_thread = threading.Thread(target=cycle_play_menu_presence, daemon=True)
    play_menu_cycle_thread.start()

    clear_screen()
    animate_title(Fore.MAGENTA + "Choose Game Mode")

    print(center_text(Fore.WHITE + "╔══════════════════════════════╗"))
    print(center_text("║ " + Fore.CYAN + "1. Campaign" + Fore.WHITE + "                     ║"))
    print(center_text("║ " + Fore.CYAN + "2. Tower" + Fore.WHITE + "                        ║"))
    print(center_text("║ " + Fore.CYAN + "3. Shadow Gauntlets" + Fore.WHITE + "              ║"))
    print(center_text("║ " + Fore.CYAN + "4. Versus (Coming Soon)" + Fore.WHITE + "          ║"))
    print(center_text("║ " + Fore.CYAN + "5. Back to Main Menu" + Fore.WHITE + "             ║"))
    print(center_text("╚══════════════════════════════╝"))

    choice = input(Fore.YELLOW + "\nSelect a game mode (1-5): ").strip()

    while choice not in ['1', '2', '3', '4', '5']:
        print(Fore.RED + "Invalid choice! Please enter a number from 1 to 5.")
        choice = input(Fore.YELLOW + "\nSelect a game mode (1-5): ").strip()

    # Stop cycling presence
    stop_cycle = True
    if play_menu_cycle_thread:
        play_menu_cycle_thread.join(timeout=1)

    if choice == '1':
        return character_creation()
    elif choice == '2':
        return create_tower_run()
    elif choice == '3':
        return gauntlet_selection()
    elif choice == '4':
        clear_screen()
        animate_title(Fore.RED + "Versus Mode Coming Soon!")
        time.sleep(2)
        return title_screen()
    elif choice == '5':
        return title_screen()

def title_screen():
    global tower
    os.system('cls' if os.name == 'nt' else 'clear')

    animate_title(Fore.MAGENTA + "Corrupted Shadows")

    splash, discord_splash = get_random_splash()
    update_presence("In the Title Screen", discord_splash)

    print(center_text(Fore.YELLOW + splash))
    print(center_text(Fore.WHITE + "v0.5.0"))
    print(center_text(""))

    print(center_text("- Play -"))
    print(center_text("- Credits -"))
    print(center_text("- Options -"))
    print(center_text("- Quit -"))

    option = input(Fore.YELLOW + "> ").lower().strip()

    while option not in ['play', 'credits', 'options', 'quit', '1', '2', '3', '4']:
        print(Fore.RED + "Invalid input! Please use a valid command or number!\n")
        option = input(Fore.YELLOW + "> ").lower().strip()

    if option == "play" or option == "1":
        return play_menu()
    elif option == "credits" or option == "2":
        credits_screen()
        return title_screen()
    elif option == "options" or option == "3":
        result = display_options_menu()
        return title_screen()
    elif option == "quit" or option == "4":
        confirm = input(Fore.RED + "Are you sure you want to quit? (yes/no) > ").lower().strip()
        if confirm == "yes":
            disconnect_from_discord()
            sys.exit()
        else:
            return title_screen()
