# Priesty's Quest

# Imports
import time
import random
import cmd
import sys
import textwrap
from player import Player
from title import title_screen
from new_game import character_creation
from enemies import *
from battle import *

def main():
    clear_screen()

    animate_title(Fore.WHITE + "Chapter 1 - The Curruption")
    
    time.sleep(3)  # Pause for effect, adjust as needed
    battle(player, goblin)

player = title_screen()
goblin = Goblin(5)

main()