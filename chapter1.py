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
from item_factory import create_item
from game_data import *

# Color Coding

# White = Normal Text
# Yellow = Event, Important Term, Player Action
# Green = The Player
# Red = The enemy / Fail Requirement
# Purple = Special Event / Occasion

# Blue = Speed Check 
# Cyan = Intelligence Check 
# Light Red = Strength Check

def chapter_1(player):
    # Clear 
    clear_screen()
    
    # Title Card
    animate_title("Chapter 1 - The Corruption")
    time.sleep(3)
    clear_screen()

    # Assign Starting Equipment
    iron_sword = create_item("Iron Sword")
    potion = create_item("Health Potion")

    player.inventory.add_item(iron_sword)
    player.inventory.add_item(potion)

    # Chapter Structure
    intro(player)
    village_result = the_village(player)
    the_forest(player, village_result)

    # Extras
    chapter = 1

def intro(player):
    # Background
    typewriter(Fore.WHITE + "3 years after the" + Fore.MAGENTA + " Great War" + Fore.WHITE + ", the world was slowly healing")
    typewriter("from the scars of battle, but one day... everything changed.")
    print("")
    time.sleep(2)
    typewriter("Rumors spread from village to village, of" + Fore.RED + " strange occurrences")
    typewriter(Fore.WHITE + "happening throughout the land.")
    print("")
    time.sleep(1)
    typewriter(Fore.WHITE + "Whispers of a" + Fore.MAGENTA + " corruption" + Fore.WHITE + " rising from the shadows...")
    typewriter("The world, once at peace, now finds itself in chaos.")
    print("")
    time.sleep(2)
    typewriter(Fore.RED + "The world would never be the same again...")
    print("")
    time.sleep(3)
    typewriter("You awaken with a shake! The skies have turned to darkness,")
    typewriter("goblins are running rampant, but something is very wrong here...")
    print("")
    time.sleep(1)
    typewriter(Fore.WHITE + "You look out your window. The village you swore to protect")
    typewriter("is under siege! You've got to get out there and do something!")
    print("")
    time.sleep(3)

def the_village(player):
    # Create Enemies
    corrupted_goblin = CorruptedGoblin(1)

    # Story
    typewriter(Fore.WHITE + "You run outside, watching as the once peaceful village is being raided")
    typewriter("by goblins, but you notice some strange oddities about them.")
    print("")
    time.sleep(1)
    typewriter(Fore.WHITE + "As you approach, you can hear the helpless cries of the villagers and the")
    typewriter("evil laughter of the goblins. Chaos surrounds you as you are forced to make")
    typewriter("a choice...")
    print("")
    time.sleep(3)
    print("\n" + Fore.CYAN + "=" * 50)
    print(Fore.YELLOW + " What will you do?".center(50))
    print(Fore.CYAN + "=" * 50)

    if player.speed > 10:
        print(Fore.GREEN + " [1] ".ljust(6) + "Protect the Village")
        print(Fore.GREEN + " [2] ".ljust(6) + "Run Away", Fore.BLUE + "(Speed: 10)")
    else:
        print(Fore.GREEN + " [1] ".ljust(6) + "Protect the Village")
        print(Fore.GREEN + " [2] ".ljust(6) + "Run Away", Fore.RED + "(Speed: 10)")

    print(Fore.CYAN + "=" * 50)
    print(Fore.BLUE + "Your Speed:", player.speed)
    print(Fore.CYAN + "=" * 50)
    while True:
        choice = input(Fore.YELLOW + "> ").strip()
        if choice == "1":
            typewriter(Fore.BLUE + "You charge at the invading goblin, still maintaining courage")
            typewriter("after all these years of peace.")
            print("")
            time.sleep(1)
            battle(player, corrupted_goblin)
            break
        elif choice == "2":
            # Branch to "The Escape"
            if player.speed > 10:
                typewriter(Fore.WHITE + "You slowly back away, avoiding combat and slipping")
                typewriter(Fore.WHITE + "into the shadows...")
                print("")
                time.sleep(2)
                the_escape(player)
            else:
                typewriter(Fore.WHITE + "You attempt to flee, but the goblin quickly reacts, blocking")
                typewriter("your path! You're not leaving without a fight!")
                print("")
                time.sleep(1)
                battle(player, corrupted_goblin)
                break
        else:
            print(Fore.RED + "Please choose a valid option!")
            print("")

    # After Battle #1
    typewriter(Fore.GREEN + "The goblin lies defeated!" + Fore.WHITE + " But that")
    typewriter("was only one of the many invaders...")
    print("")
    time.sleep(2)
    typewriter(Fore.WHITE + "You notice the goblin shaking on the floor, bouncing between")
    typewriter("life and death in an instant.")
    print("")
    time.sleep(3)
    print(Fore.YELLOW + "What will you do?".center(50))
    print(Fore.CYAN + "=" * 50)
    print(Fore.GREEN + " [1] ".ljust(6) + "Investigate the Goblin")
    print(Fore.GREEN + " [2] ".ljust(6) + "Locate Villagers")
    print(Fore.CYAN + "=" * 50)
    while True:
        choice = input(Fore.YELLOW + "> ").strip()
        if choice == "1":
            typewriter(Fore.WHITE + "You approach the goblin and look at it. It whispers")
            typewriter('in a soft voice:' + Fore.RED + ' "The corruption will consume us all"')
            print("")
            time.sleep(1)
            typewriter(Fore.WHITE + "Before you can react, the goblin appears lifeless")
            typewriter("on the ground...")
            print("")
            break
        elif choice == "2":
            typewriter(Fore.WHITE + "As you search the village for survivors, you find")
            typewriter("none standing... This once cheerful village has fallen, and it's")
            typewriter("time to make your leave...")
            print("")
            time.sleep(3)
            break
    typewriter(Fore.WHITE + "As you leave the village you keep thinking")
    typewriter("to yourself..." + Fore.MAGENTA + " What was motivating those goblins?")
    print("")
    typewriter(Fore.WHITE + "You watched as they ignored all the gold and other")
    typewriter("valuables, and went straight for the kill.")
    print("")
    typewriter(Fore.WHITE + "But you have no time to dwell on that... As you must cross")
    typewriter("through the dense forest in order to reach" + Fore.GREEN + " The Iron Fist.")
    print("")
    time.sleep(3)
    return "fight"

def the_escape(player):
    typewriter(Fore.WHITE + "As you leave the village, you hear the helpless cries")
    typewriter("of the villagers you left behind..." + Fore.MAGENTA + "Did you make the right choice?")
    print("")
    time.sleep(3)
    typewriter(Fore.WHITE + "The village is claimed by the goblins! You run off")
    typewriter("towards the forest, leaving your" + Fore.RED + " past behind...")
    print("")
    time.sleep(2)
    typewriter(Fore.WHITE + "You look back one last time with tears in your eyes. The")
    typewriter("village you've lived in for years is gone, and now you're on your own.")
    print("")
    time.sleep(3)
    return "flee"

def the_forest(player, village_result):
    # Create Enemies
    corrupted_orc = CorruptedOrc(7)

    clear_screen()
    animate_title(Fore.GREEN + "Act II - The Forest")
    print("")
    time.sleep(3)
    clear_screen()
    if village_result == "fight":
        pass
    elif village_result == "flee":
        battle(player,corrupted_orc)
    else:
        print(Fore.RED + "Error!")
