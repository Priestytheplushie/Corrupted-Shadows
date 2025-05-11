from colorama import Fore, Style
from text_utils import *
from tower.tower_data import *
import time
import random
from tower.tower_data import *
import sys

def corrupted_death_screen():
    global floor, tower_score  # Access the global variables

    # Simulate a corruption effect with color changes and distortion
    corruption_effects = [
        Fore.BLACK + Style.BRIGHT + "The world around you distorts..." + Style.RESET_ALL,
        Fore.RED + Style.BRIGHT + "The corruption spreads... You lose control..." + Style.RESET_ALL,
        Fore.MAGENTA + "Your vision fades as the corruption overwhelms you..." + Style.RESET_ALL,
        Fore.GREEN + "You were corrupted... No escape..." + Style.RESET_ALL
    ]
    
    print(Fore.RED + "-" * 50)
    print(Fore.MAGENTA + "Corruption Death" + Style.RESET_ALL)
    print(Fore.RED + "-" * 50)
    time.sleep(1)
    
    # Animation loop for corruption effects
    for effect in corruption_effects:
        print(effect)
        time.sleep(random.uniform(0.5, 1.5))  # Randomized time between effects

    print(Fore.BLACK + Style.BRIGHT + "\nYou were Corrupted..." + Style.RESET_ALL)
    time.sleep(1)
    
    # Display the player's floor and tower score
    print(Fore.YELLOW + "\nFloor Reached: " + str(floor))
    print(Fore.YELLOW + "Score: " + str(tower_score))
    
    print(Fore.RED + "-" * 50)
    print(Fore.YELLOW + "\nOptions:")
    print(Fore.CYAN + "[1] Restart Tower")
    print(Fore.CYAN + "[2] Quit")
    print(Fore.RED + "-" * 50)
    
    # Input for restarting or quitting
    option = input(Fore.YELLOW + "> ").lower()
    while option not in ['1', '2']:
        print(Fore.RED + "Invalid input! Please use a valid command!\n")
        option = input(Fore.YELLOW + "> ").lower()

    if option == "1":
        # Restart the tower (call the main function or restart logic)
        from tower.tower_main import main
        main()  # Call your main tower function to restart
    elif option == "2":
        # Quit the game
        sys.exit()


def death_screen(player):
    global floor, tower_score
    clear_screen()
    print("")
    typewriter(center_text(Fore.RED + "YOU DIED" + Style.RESET_ALL))
    print("")

    # Display the floor reached and tower score
    print(Fore.YELLOW + "Floor Reached: " + str(floor) + Style.RESET_ALL)
    print(Fore.YELLOW + "Tower Score: " + str(tower_score) + Style.RESET_ALL)

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

def give_up_screen(player):
    global floor, tower_score
    clear_screen()
    print("")
    animate_title(Fore.MAGENTA + "YOU GAVE UP" + Style.RESET_ALL)
    print("")

    # Display the floor reached and tower score
    print(Fore.YELLOW + "Floor Reached: " + str(floor) + Style.RESET_ALL)
    print(Fore.YELLOW + "Tower Score: " + str(tower_score) + Style.RESET_ALL)
    print("")

    # Present options
    print(center_text("- Return to Title -"))
    print(center_text("- Quit -"))

    option = input(Fore.YELLOW + "> ").lower()
    while option not in ['return', 'quit', 'title']:
        print(Fore.RED + "Invalid input! Please use a valid command!\n")
        option = input(Fore.YELLOW + "> ").lower()

    if option in ["return", "title"]:
        from title import title_screen
        title_screen()
    elif option == "quit":
        sys.exit()

def display_corruption_bar(player):
    from colorama import Fore, Style

    max_corruption = 100
    bar_length = 10

    # Clamp corruption between 0 and 100
    corruption = min(max(player.corruption, 0), 100)
    filled_length = int(corruption / max_corruption * bar_length)
    unfilled_length = bar_length - filled_length

    # Choose color based on corruption severity
    if corruption < 35:
        fill_color = Fore.GREEN
    elif corruption < 70:
        fill_color = Fore.YELLOW
    else:
        fill_color = Fore.RED

    bar = fill_color + "█" * filled_length + Fore.WHITE + "░" * unfilled_length
    percent_text = f"{corruption:.0f}%".rjust(4)

    # Display formatted bar
    print(Fore.MAGENTA + "╔" + "═" * 26 + "╗")
    print(Fore.CYAN + "║  Corruption: [" + bar + "] " + percent_text + Fore.CYAN + " ║")
    print(Fore.MAGENTA + "╚" + "═" * 26 + "╝" + Style.RESET_ALL)
