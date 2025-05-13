import json
import os
import importlib
from colorama import Fore, Style
from text_utils import animate_title, center_text
from text_utils import clear_screen
from discord import update_presence

# Load gauntlet data from JSON file in the shadow_gauntlets folder
def load_gauntlets():
    gauntlet_file_path = os.path.join('shadow_gauntlets', 'gauntlets.json')  # Correct path
    with open(gauntlet_file_path, 'r') as file:
        data = json.load(file)
    return data['gauntlets']

# Display the gauntlet selection menu
def gauntlet_selection():
    update_presence("Shadow Gauntlets", "Seeking a Challenge")
    clear_screen()
    gauntlets = load_gauntlets()
    
    # Display the title
    animate_title(Fore.MAGENTA + "=== Shadow Gauntlets ===")
    print("\n")
    
    # Display each gauntlet with colored difficulty and length
    for idx, gauntlet in enumerate(gauntlets, 1):
        # Color gauntlet names based on difficulty
        if gauntlet['difficulty'] == "Easy":
            color = Fore.GREEN
        elif gauntlet['difficulty'] == "Medium":
            color = Fore.YELLOW
        elif gauntlet['difficulty'] == "Hard":
            color = Fore.RED
        elif gauntlet['difficulty'] == "Very Hard":
            color = Fore.MAGENTA
        else:
            color = Fore.WHITE  # Default color if difficulty is unknown

        # Print gauntlet name with difficulty color and length
        print(center_text(color + str(idx) + ". " + gauntlet['name']))

    # Ask user for their choice
    choice = input(Fore.YELLOW + "\nEnter choice (1-" + str(len(gauntlets)) + "): ").strip()

    while not choice.isdigit() or int(choice) not in range(1, len(gauntlets) + 1):
        print(Fore.RED + "Invalid input! Please select a valid gauntlet.")
        choice = input((center_text(Fore.YELLOW + "\nEnter choice (1-" + str(len(gauntlets)) + "): ").strip()))

    selected_gauntlet = gauntlets[int(choice) - 1]
    print(Fore.CYAN + "You selected: " + selected_gauntlet['name'])

    # Call gauntlet_info function to display the gauntlet's detailed info
    gauntlet_info(selected_gauntlet)

    # Give the user the option to start the gauntlet or go back
    while True:
        print(Fore.YELLOW + "\n[1] Start Gauntlet")
        print(Fore.YELLOW + "[2] Back to Gauntlet Selection")
        option = input(Fore.YELLOW + "Choose an option (1-2): ").strip()

        if option == "1":
            # Load the corresponding gauntlet's main.py module and start it
            gauntlet_module = selected_gauntlet['module']
            gauntlet_main = importlib.import_module('shadow_gauntlets.' + gauntlet_module + '.main')
            gauntlet_main.start_gauntlet()
            break  # Break out of the loop after starting the gauntlet
        elif option == "2":
            # If user chooses to go back, restart the gauntlet selection
            gauntlet_selection()
            break  # Break the current loop to restart gauntlet selection
        else:
            print(Fore.RED + "Invalid option! Please choose a valid option (1-2).")

# This function will display detailed info about the selected gauntlet
def gauntlet_info(gauntlet):
    clear_screen()
    print(Fore.MAGENTA + "\n=== Gauntlet Info ===")
    print(Fore.CYAN + "Name: " + gauntlet['name'])
    print(Fore.YELLOW + "Difficulty: " + gauntlet['difficulty'])
    print(Fore.GREEN + "Length: " + gauntlet['length'])
    print(Fore.WHITE + "\nDescription:")

    update_presence("Shadow Gauntlet - " + gauntlet['name'], f"Difficulty: {gauntlet['difficulty']} | Length: {gauntlet['length']}")
    
    # Print the description line by line (multi-line handling)
    for line in gauntlet['description']:
        print(Fore.WHITE + line)
    
    print(Fore.MAGENTA + "=======================")