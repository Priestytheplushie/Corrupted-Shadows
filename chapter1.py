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
from utils import *

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
    animate_title(Fore.MAGENTA+"Chapter 1 - The Corruption")
    time.sleep(3)
    clear_screen()

    # Assign Starting Equipment
    iron_sword = create_item("Iron Sword")
    potion = create_item("Health Potion")
    cleansing_flute = create_item("Cleansing Flute")

    player.inventory.add_item(iron_sword)
    player.inventory.add_item(potion)
    player.inventory.add_item(cleansing_flute)

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
    clear_screen()
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
    print(Fore.YELLOW + " [3] ".ljust(6) + "Check Inventory")
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
            battle(player, corrupted_goblin,"single")
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
                battle(player, corrupted_goblin,"single")
                break
        elif choice == "3":
            player.inventory.use_non_combat_item(player)
            time.sleep(1)
            print("\n" + Fore.CYAN + "=" * 50)
            print(Fore.YELLOW + " What will you do?".center(50))
            print(Fore.CYAN + "=" * 50)

            if player.speed > 10:
                print(Fore.GREEN + " [1] ".ljust(6) + "Protect the Village")
                print(Fore.GREEN + " [2] ".ljust(6) + "Run Away", Fore.BLUE + "(Speed: 10)")
            else:
                print(Fore.GREEN + " [1] ".ljust(6) + "Protect the Village")
                print(Fore.GREEN + " [2] ".ljust(6) + "Run Away", Fore.RED + "(Speed: 10)")
            print(Fore.YELLOW + " [3] ".ljust(6) + "Check Inventory")
            print(Fore.CYAN + "=" * 50)
            print(Fore.BLUE + "Your Speed:", player.speed)
            print(Fore.CYAN + "=" * 50)

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
            time.sleep(2)
            typewriter(Fore.WHITE+"While you were distracted, the goblins finished ravaging the once")
            typewriter("peaceful village. You feel a sense of sadness and sorrow, but")
            typewriter("you seem to be more curious about the strange goblin.")
            print("")
            time.sleep(2)
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
    corrupted_orc = CorruptedOrc(4)
    corrupted_goblin_1 = CorruptedGoblin(1)
    corrupted_goblin_2 = CorruptedGoblin(1,True)
    corrupted_goblin_3 = CorruptedGoblin(1)

    clear_screen()
    animate_title(Fore.GREEN + "Act II - The Forest")
    print("")
    time.sleep(3)
    clear_screen()
    if village_result == "fight":
        typewriter(Fore.WHITE + "As you walk through the forest, a strange sense of dread settles in...")
        typewriter("Something about this place feels very, very wrong.")
        print("")
        time.sleep(2)
        typewriter("You hear laughter — the kind you'd expect from goblins lying in wait.")
        typewriter("But the sound is colder, darker. As if even the goblins aren't quite themselves.")
        time.sleep(1)
        print("")
        typewriter("Eventually, you find yourself in a clearing... Feeling safe, you lower your guard.")
        print("")
        time.sleep(1)
        typewriter("But as you're about to sit down for a quick rest, three goblins jump from the bushes-- daggers")
        typewriter("in hand, ready for vengeance, Thier eyes glow an unnatural color, confirming your suspicion that")
        typewriter("something isn't quite right")
        print("")
        time.sleep(1)
        typewriter("The goblins sorrsurroundund you, but show no intreast in your coin, the clearing grows quiet, alll you can")
        typewriter("hear is the cold laughter of the goblins closing in on you... You've got to do something!")
        print("")
        time.sleep(2)
        enemies = [corrupted_goblin_1, corrupted_goblin_2, corrupted_goblin_3]
        battle(player, enemies,battle_mode="multi")
        typewriter(Fore.WHITE+"The three goblins lay defeated on the ground. While two are laying lifeless, one")
        typewriter("is still twitching violently, you can hear its screams of pain...You")
        typewriter("think-- that poor thing")
        print("")
        time.sleep(1)
        typewriter(Fore.WHITE+"After a well deserved rest, you leave the clearing, pushing yourself through")
        typewriter("the dense forest. You find yourself at a split-- and a choice")
        print("")
        time.sleep(2)
        heal_player(player, 30) 
    

    elif village_result == "flee":
        typewriter(Fore.WHITE+"As you rush through the forest, you lose your sense of direction.")
        typewriter("but maybe that wasn't the best idea, as you find yourself")
        typewriter("face to face with an " + Fore.RED + "Orc." + Fore.WHITE)
        print("")
        time.sleep(2)
        typewriter(Fore.WHITE+"Only... something seems wrong. The Orcs eyes glow a bright"+Fore.MAGENTA+"purple")
        typewriter("color"+Fore.WHITE+" and it's behavior seems unnatural, almost like it's acting without will")
        time.sleep(1)
        typewriter(Fore.BLUE+" Before you know it, the Orc is on top of you, ready to smash you into itty, bitty, pieces!")
        print(Fore.RESET+"")
        print("")
        battle(player,corrupted_orc,battle_mode="single",bonus_ap=2)
        typewriter(Fore.WHITE+"The Orc seems to be knocked out-- for now... Better leave before he wakes!")
        print("")
        time.sleep(2)
        typewriter(Fore.WHITE+"After walking for what you feel is eternity, you find yourself at a split path. You'll")
        typewriter("have to make a choice:")
        print("")
        time.sleep(2)
    
    print(Fore.YELLOW + "Where will you go?".center(50))
    print(Fore.CYAN + "=" * 50)
    print(Fore.GREEN + " [1] ".ljust(6) + "Head Left")
    print(Fore.GREEN + " [2] ".ljust(6) + "Head North")
    print(Fore.YELLOW +" [3]".ljust(6) + "Check Inventory")
    print(Fore.CYAN + "=" * 50)
