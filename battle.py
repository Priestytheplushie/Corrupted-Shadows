import time
import random
import os
import sys
from enemies import *
from inventory import Inventory
from items import *
from game_data import *
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

turn = 1

def check_level_up(player):
    player.level_up()

def calculate_money(enemy):
    base_money = 10 
    level_multiplier = enemy.level * 5
    difficulty_multiplier = 1 + (difficulty / 100) 
    random_bonus = random.randint(0, 20)
    money = (base_money + level_multiplier) * difficulty_multiplier + random_bonus
    return round(money)

def calculate_xp(enemy):
    base_xp = 10
    level_multiplier = enemy.level * 2
    xp = base_xp + level_multiplier
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
    print(Fore.WHITE + "HP: " + str(player.hp) + " | Enemy HP: " + str(enemy.hp))
    print(Fore.CYAN + "-" * 40)
    print("")

    # Process player's status effects (e.g., stagger)
    player.process_status_effects()
    
    # Handle staggered player - Skip turn if staggered
    if player.is_staggered():
        print(Fore.YELLOW + player.name + " is staggered and can't act this turn!")
        time.sleep(1)
    else:
        enemy.choose_action(player)

def player_turn(player, enemy):
    while True:
        print(Fore.CYAN + "-" * 40)
        typewriter(Fore.MAGENTA + "Your Turn - Turn " + str(turn))
        print(Fore.WHITE + "HP: " + str(player.hp) + " | Enemy HP: " + str(enemy.hp))
        print(Fore.CYAN + "-" * 40)
        print("")

        # Process status effects (e.g., stagger)
        player.process_status_effects()

        # Check if player is staggered and modify their actions accordingly
        if player.is_staggered():
            print(Fore.YELLOW + player.name + " is staggered and can’t act normally!")
            # You may want to skip the action or modify the player's turn choices here
            time.sleep(1)
            break

        # If not staggered, show normal turn options
        typewriter(Fore.YELLOW + "What will you do?")
        time.sleep(0.5)
        print(Fore.GREEN + "1. Attack")
        if isinstance(player.weapon, Weapon):
            print(Fore.YELLOW + "Your weapon: " + player.weapon.name + " (equipped) | Durability: " + str(player.weapon.durability) + "/" + str(player.weapon.max_durability))
        else:
            print(Fore.RED + "You have no weapon equipped.")
        if len(player.inventory.items) > 0:
            print(Fore.GREEN + "2. Use Item")
        print(Fore.GREEN + "3. View Inventory")
        print(Fore.GREEN + "4. Check Character Sheet")
        print(Fore.GREEN + "5. Identify (Reveal Enemy Stats)")
        print(Fore.GREEN + "b. End Turn")
        print(Fore.CYAN + "-" * 40)

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
                while True:
                    print(Fore.YELLOW + "Choose an item by number to use (or b to go back):")
                    for i, item in enumerate(player.inventory.items):
                        item_text = Fore.GREEN + str(i + 1) + ". " + item.name + " - " + item.description
                        if hasattr(item, "durability") and hasattr(item, "max_durability"):
                            item_text += Fore.YELLOW + " | Durability: " + str(item.durability) + "/" + str(item.max_durability)
                        print(item_text)
                    item_choice = input(Fore.YELLOW + "> ").strip().lower()
                    if item_choice == 'b':
                        break
                    try:
                        item_choice = int(item_choice) - 1
                        if 0 <= item_choice < len(player.inventory.items):
                            player.inventory.use_item(player, item_choice)
                            print("")
                            return  # Exit the function and end the player's turn
                        else:
                            print(Fore.RED + "Invalid index. Try again.")
                            print("")
                    except ValueError:
                        print(Fore.RED + "Please enter a valid number.")
                        print("")
            else:
                print(Fore.RED + "Your inventory is empty!")
        elif choice == "3":
            print(Fore.YELLOW + "\n--- INVENTORY ---")
            print(Fore.CYAN + "-" * 40)
            if len(player.inventory.items) == 0:
                print(Fore.RED + "Your inventory is empty.")
            for i, item in enumerate(player.inventory.items):
                print(Fore.GREEN + str(i + 1) + ". " + item.name + " - " + item.description)
                if hasattr(item, "durability") and hasattr(item, "max_durability"):
                    print(Fore.YELLOW + "    Durability: " + str(item.durability) + "/" + str(item.max_durability))
                print(Fore.CYAN + "-" * 40)
            print("")
        elif choice == "4":
            show_character_sheet(player, False)
        elif choice == "5":
            print(Fore.MAGENTA + "\nScanning enemy essence..." + Fore.WHITE)
            time.sleep(1)
            print(Fore.CYAN + "\n┌" + "─" * 38 + "┐")
            print(Fore.CYAN + "│ " + Fore.MAGENTA + "ENEMY IDENTIFIED:".ljust(37) + Fore.CYAN + "│")
            print(Fore.CYAN + "├" + "─" * 38 + "┤")
            if hasattr(enemy, 'real_name'):
                print(Fore.CYAN + "│ " + Fore.RED + "Name: " + enemy.real_name.ljust(37) + Fore.CYAN + "│")
            else:
                print(Fore.CYAN + "│ " + Fore.RED + "Name: " + enemy.name.ljust(37) + Fore.CYAN + "│")
            print(Fore.CYAN + "│ " + Fore.YELLOW + "Level: " + str(enemy.level).ljust(37) + Fore.CYAN + "│")
            print(Fore.CYAN + "│ " + Fore.RED + "HP: " + (str(enemy.hp) + "/" + str(enemy.max_hp)).ljust(37) + Fore.CYAN + "│")
            print(Fore.CYAN + "│ " + Fore.GREEN + "Strength: " + str(enemy.strength).ljust(37) + Fore.CYAN + "│")
            print(Fore.CYAN + "│ " + Fore.BLUE + "Speed: " + str(enemy.speed).ljust(37) + Fore.CYAN + "│")
            print(Fore.CYAN + "│ " + Fore.MAGENTA + "Defense: " + str(enemy.defense).ljust(37) + Fore.CYAN + "│")
            print(Fore.CYAN + "└" + "─" * 38 + "┘")
            print("")
            if hasattr(enemy, "reveal_identity"):
                enemy.reveal_identity()
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
    typewriter(Fore.YELLOW + "Battle started!")
    print("")
    time.sleep(1)
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
    while player.hp > 0 and enemy.hp > 0:
        turn += 1
        print("\n--- Turn " + str(turn) + " ---")
        player_turn(player, enemy)
        if enemy.hp > 0:
            enemy_turn(player, enemy)
    if player.hp > 0:
        battle_conclusion(player, enemy)
    else:
        death_screen(player)
