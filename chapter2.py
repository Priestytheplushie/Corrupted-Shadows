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

shopping = False

def chapter_2(player):
    # Clear 
    clear_screen()
    
    # Title Card
    animate_title(Fore.RED+"Chapter 2 - From the Shadows")
    time.sleep(3)
    clear_screen()

    # Chapter Structure
    the_fallen_fist(player)

    # Extras
    chapter = 2

def the_fallen_fist(player):
    global shopping
    typewriter(Fore.WHITE+"You stand before the Iron Fist, this once legendary building has")
    typewriter("seen better days. Despite the building appearing to be burning, the flames are a")
    typewriter("unnatural color. Work of the corruption you assume.")
    print("")
    time.sleep(1)
    typewriter("Near the hall is a nearby town, It might be a good idea to check it out before")
    typewriter("you run into the burning building...")
    print("")
    print("\n" + Fore.CYAN + "=" * 50)
    print(Fore.YELLOW + " What will you do?".center(50))
    print(Fore.CYAN + "=" * 50)
    print(Fore.MAGENTA + " [1] ".ljust(6) + "Enter the Guild Hall")
    print(Fore.GREEN + " [2] ".ljust(6) + "Explore the nearby town")
    print(Fore.YELLOW + " [3] ".ljust(6) + "Check Inventory")
    print(Fore.CYAN + "=" * 50)
    while True:
        choice = input(Fore.YELLOW + "> ").strip()

        if choice == "1":
            guild_halls(player)
        elif choice == "2":
            shop(player)
        elif choice == "3":
            player.inventory.use_non_combat_item(player)
            time.sleep(1)
            print("\n" + Fore.CYAN + "=" * 50)
            print(Fore.YELLOW + " What will you do?".center(50))
            print(Fore.CYAN + "=" * 50)
            print(Fore.MAGENTA + " [1] ".ljust(6) + "Enter the Guild Hall")
            print(Fore.GREEN + " [2] ".ljust(6) + "Explore the nearby town")
            print(Fore.YELLOW + " [3] ".ljust(6) + "Check Inventory")
            print(Fore.CYAN + "=" * 50)

        else:
            print(Fore.RED+"Invalid Input, Try again")

def guild_halls(player):
    pass

def shop(player):
    global shopping

    # Stock Counter
    potions_in_stock = 5
    swords_in_stock = 1
    maces_in_stock = 1

    # Create Item Objects
    iron_sword = create_item("Iron Sword")

    typewriter(Fore.WHITE+"You walk into the town and spot a nearby shop selling")
    typewriter("all kinds of supplies. You decide it might be a good idea")
    typewriter("to pick up some items before you enter the guild")
    print("")
    time.sleep(1)
    shopping = True
    while shopping:
        print(Fore.YELLOW+"The Iron Fist's Shop")
        print('')
        print(Fore.GREEN+"Balance:",player.money)
        print("")
        print(Fore.WHITE+"Items For Sale:")
        print("")
        print("[1] Health Potion ($75)",potions_in_stock,"left")
        print("[2] Iron Sword ($200)",swords_in_stock,"left")
        print("[3] Orc's Mace ($500)",maces_in_stock,"left")
        print("")
        while True:
            choice = input(Fore.YELLOW + "> ").strip()