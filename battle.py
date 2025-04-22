import time
import random
import os
import sys
from enemies import *
from inventory import Inventory
from items import *
from player import Player
from title import animate_title
from text_utils import *
from screens import death_screen, show_character_sheet

from strings import (
    player_attacks_first_message,
    enemy_attacks_first_message,
    random_initiative_message,
    randomized_intro_messages,
)

# Global
turn = 1

def check_level_up(player):
    player.level_up()

def calculate_xp(enemy):
    base_xp = 10  # Base XP
    level_multiplier = enemy.level * 2  # Each level gives additional XP
    xp = base_xp + level_multiplier  # Add XP based on enemy level
    return xp

def battle_conclusion(player, enemy):
    clear_screen()
    result = "Victory"
    typewriter(Fore.YELLOW + player.name + " has defeated " + enemy.name + "!", delay=0.1)
    print("")
    time.sleep(1)
    xp = calculate_xp(enemy)
    player.xp += xp
    time.sleep(0.5)
    typewriter(Fore.GREEN + player.name + " gains " + str(xp) + " XP!", delay=0.1)
    time.sleep(1)
    clear_screen()
    animate_title(Fore.CYAN + "BATTLE OVER!", delay=0.05)
    time.sleep(1)
    print(center_text(Fore.WHITE + "Total XP: " + str(player.xp)))
    print(center_text(Fore.WHITE + "Current HP: " + str(player.hp) + "/" + str(player.max_hp)))
    print(center_text(Fore.WHITE + "Strength: " + str(player.strength)))
    print(center_text(Fore.WHITE + "Defense: " + str(player.defense)))
    print(center_text(Fore.WHITE + "Money: " + str(player.money)))
    print("")
    check_level_up(player)
    print("")
    print(center_text(Fore.YELLOW + "Press Enter to continue..." + Fore.RESET))
    input()
    return result


def enemy_turn(player, enemy):
    print(Fore.CYAN + "-" * 40)
    typewriter(Fore.MAGENTA + "Enemy Turn - Turn " + str(turn))
    print(Fore.WHITE + f"HP: {player.hp} | Enemy HP: {enemy.hp}")
    print(Fore.CYAN + "-" * 40)
    print("")
    time.sleep(1)
    enemy.choose_action(player)

def player_turn(player, enemy):
    print(Fore.CYAN + "-" * 40)
    typewriter(Fore.MAGENTA + "Your Turn - Turn " + str(turn))
    print(Fore.WHITE + "HP: " + str(player.hp) + " | Enemy HP: " + str(enemy.hp))
    print(Fore.CYAN + "-" * 40)
    print("")
    
    time.sleep(1)
    typewriter(Fore.YELLOW + "What will you do?")
    time.sleep(0.5)  
    print(Fore.GREEN + "1. Attack")
    
    if player.weapon:
        print(Fore.YELLOW + "Your weapon: " + player.weapon.name + " (equipped) | Durability: " + str(player.weapon.durability) + "/" + str(player.weapon.max_durability))
    else:
        print(Fore.RED + "You have no weapon equipped.")
    
    if len(player.inventory.items) > 0:
        print("2. Use Item")
    
    print("3. View Inventory")
    print("4. Check Character Sheet")
    print("b. Back")
    print(Fore.CYAN + "-" * 40)
    
    while True:
        choice = input(Fore.YELLOW + "> ").strip().lower()
        
        if choice == "1":
            if player.weapon is None:
                player.punch(enemy)
            else:
                player.attack(enemy)
            print("")
            break
        elif choice == "2":
            if len(player.inventory.items) > 0:
                print(Fore.YELLOW + "Choose an item by number to use (or b to go back):")
                for i, item in enumerate(player.inventory.items):
                    print(Fore.GREEN + str(i + 1) + ". " + item.name + " - " + item.description + " | Durability: " + str(item.durability) + "/" + str(item.max_durability))
                while True:
                    item_choice = input(Fore.YELLOW + "> ").strip().lower()
                    if item_choice == 'b':
                        break
                    try:
                        item_choice = int(item_choice) - 1
                        if 0 <= item_choice < len(player.inventory.items):
                            player.inventory.use_item(player, item_choice)
                            print("")
                            break
                        else:
                            print(Fore.RED + "Invalid index. Try again.")
                            print("")
                    except ValueError:
                        print(Fore.RED + "Please enter a valid number.")
                        print("")
            else:
                print(Fore.RED + "Your inventory is empty!")
            break
        elif choice == "3":
            print(Fore.YELLOW + "\n--- INVENTORY ---")
            print(Fore.CYAN + "-" * 40)
            if len(player.inventory.items) == 0:
                print(Fore.RED + "Your inventory is empty.")
            for i, item in enumerate(player.inventory.items):
                print(Fore.GREEN + str(i + 1) + ". " + item.name + " - " + item.description)
                print(Fore.YELLOW + "    Durability: " + str(item.durability) + "/" + str(item.max_durability))
                print(Fore.CYAN + "-" * 40)
            print("")
        elif choice == "4":
            show_character_sheet(player, False)
            typewriter(Fore.YELLOW + "What will you do?")
            time.sleep(0.5)  # Brief pause before the options
            print(Fore.GREEN + "1. Attack")
            if len(player.inventory.items) > 0:
                print("2. Use Item")
            print("3. View Inventory")
            print("4. Check Character Sheet")
            print("b. Back")
            print(Fore.CYAN + "-" * 40)
        elif choice == "b":
            break
        else:
            print(Fore.RED + "Invalid option. Try again.")

def battle(player, enemy):
    global turn
    turn = 1
    os.system('cls' if os.name == 'nt' else 'clear')
    typewriter(randomized_intro_messages(player, enemy))
    print("")
    time.sleep(1)
    # Battle Start Message
    typewriter(Fore.YELLOW + "Battle started!")
    print("")
    time.sleep(1)
    # Player vs Enemy
    typewriter(Fore.GREEN + player.name + Fore.WHITE + " v.s " + Fore.RED + enemy.name)
    print("")
    time.sleep(1)
    if enemy.speed > player.speed:
        typewriter(enemy_attacks_first_message(player, enemy))
        print("")
        enemy_turn(player, enemy)
    elif enemy.speed < player.speed:
        typewriter(player_attacks_first_message(player, enemy))
        print("")
        player_turn(player, enemy)
    else:
        typewriter(random_initiative_message(player, enemy))
        print("")
        choice = random.randint(1, 2)
        if choice == 1:
            player_turn(player, enemy)
        else:
            enemy_turn(player, enemy)
    # Battle Loop
    while player.hp > 0 and enemy.hp > 0:
        turn += 1
        print("\n--- Turn " + str(turn) + " ---")
        player_turn(player, enemy)
        if enemy.hp <= 0:
            battle_conclusion(player, enemy)
            del enemy
            break
        enemy_turn(player, enemy)
    if player.hp <= 0:
        time.sleep(3)
        death_screen()
        del enemy
