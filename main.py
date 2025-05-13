# Corrupted Shadows

# Imports
import time
import random
import cmd
import sys
import textwrap
import colorama
from player import Player
from title import title_screen
from game_data import tower
from enemies import *
from battle import *
from chapter1 import *
from tower.tower_main import main
from tower.tower_screens import corrupted_death_screen
from discord import connect_to_discord, update_presence, disconnect_from_discord
import os

# Dev Mode - DO NOT TOUCH

dev_mode = False
dev_title_screen = None 
player = None

try:
    if os.path.exists('dev_tools'):
        from dev_tools.dev_menu import dev_title_screen 
        dev_mode = True
except ImportError:
    dev_mode = False
    dev_title_screen = None

# Discord connection setup
try:
    connect_to_discord()
except Exception as e:
    print("Discord connection failed:", e)

def main_game_loop():
    global player  # Ensure to use the global player variable

    while True:
        if dev_mode and dev_title_screen:
            # If in dev_mode, load the dev menu for character creation
            player, mode = dev_title_screen() or (None, "dev")
        else:
            # If not in dev_mode, proceed with normal title screen
            player, mode = title_screen()

        globals()['player'] = player  # Update global player instance for dev console

        if player:
            if mode == "tower":
                # Run tower mode if selected
                main(player)
            elif mode == "gauntlet":
                # Handle gauntlet mode here
                print("Gauntlet mode selected.")  # Placeholder, needs gauntlet handling logic
            elif mode == "dev":
                # In dev mode, run some dev-specific flow
                typewriter(Fore.GREEN + "Dev flow ran successfully. Errors: None")
                time.sleep(1)
                input(Fore.YELLOW+"Press any key to continue")
            else:
                # Handle other modes
                print(Fore.RED + "Invalid mode selected. Exiting...")

            # If the player is created and is in campaign mode, start the first chapter
            chapter_1(player)

        elif player is None and mode == "dev":
            # If in dev mode but no player is created
            typewriter(Fore.YELLOW + "Dev flow ran successfully. Errors: No Player Instance")
            time.sleep(1)
            input(Fore.YELLOW+"Press any key to continue")
        
        # If character creation fails or no mode is selected
        elif not player:
            print(Fore.RED + "Character creation failed. Please try again.")

# Run the main game loop
main_game_loop()
