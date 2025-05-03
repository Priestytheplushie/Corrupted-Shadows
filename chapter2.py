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
from items import *
from item_factory import create_item
from game_data import *
from utils import *

def chapter_2(player):
    # Clear 
    clear_screen()
    
    # Title Card
    animate_title(Fore.RED+"Chapter 2 - From the Shadows")
    time.sleep(3)
    clear_screen()

    # Chapter Structure
    intro(player)
    the_fallen_fist(player)

    # Extras
    chapter = 2

def intro():
    typewriter("    ")

def the_fallen_fist(player):
    typewriter(Fore.WHITE+"You stand before the Iron Fist, this once legendary building has")
    typewriter("seen better days. Despite the building appearing to be burning, the flames are a")
    typewriter("unnatural color. Work of the corruption you assume.")
    time.sleep(1)
    typewriter("Near the hall is a nearby town, It might be a good idea to check it out before")
    typewriter("you run into the burning building...")
    print("\n" + Fore.CYAN + "=" * 50)
    print(Fore.YELLOW + " What will you do?".center(50))
    print(Fore.CYAN + "=" * 50)
    print(Fore.MAGENTA + " [1] ".ljust(6) + "Enter the Guild Hall")
    print(Fore.GREEN + " [2] ".ljust(6) + "Explore the nearby town")
    print(Fore.YELLOW + " [3] ".ljust(6) + "Check Inventory")
    print(Fore.CYAN + "=" * 50)