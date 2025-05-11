import time
import random
import os
from enemies import *
from inventory import Inventory
from items import *
from game_data import *
from player import Player
from title import animate_title
from tower.tower_items import *
from text_utils import *
from screens import death_screen, show_character_sheet
from loot_tables import loot_tables, roll_corrupted_loot,roll_loot
from tower.tower_data import tower_difficulty, floor, tower_score
from strings import (
    player_attacks_first_message,
    enemy_attacks_first_message,
    random_initiative_message,
    randomized_intro_messages,
    multi_battle_enemies_go_first,
    multi_battle_intro,
    multi_battle_player_goes_first,
    multi_battle_random_initiative
)
from discord import update_presence

turn = 1

def check_level_up(player):
    player.check_level_up()

def calculate_xp(enemy, player):
    global tower_difficulty, floor, tower_score
    base_xp = 50
    level_difference = enemy.level - player.level

    # Difficulty multipliers
    difficulty_multipliers = {
        "Easy": 0.75,
        "Normal": 1.0,
        "Hard": 1.5,
        "Hardcore": 2.0
    }

    multiplier = difficulty_multipliers.get(tower_difficulty.capitalize(), 1.0)

    # Level-based XP adjustment
    level_multiplier = (enemy.level * 2) + (level_difference * 5)
    level_multiplier = max(level_multiplier, 10)

    # Floor and score bonuses
    floor_bonus = floor * 2
    score_bonus = tower_score // 10

    total_xp = (base_xp + level_multiplier + floor_bonus + score_bonus) * multiplier
    return int(total_xp)


def battle_conclusion(player, enemies, mode):
    clear_screen()
    total_xp = 0
    killed_enemies = []

    if mode == "multi":
        for enemy in enemies:
            if enemy.hp <= 0:
                killed_enemies.append(enemy.name)
                total_xp += calculate_xp(enemy, player)

        total_xp += int(total_xp * 0.25)

        typewriter(Fore.YELLOW + player.name + " has defeated the following enemies:", delay=0.1)
        for enemy in killed_enemies:
            print(Fore.GREEN + "- " + enemy)

        enemies = [e for e in enemies if e.hp > 0]
    else:  # Single battle mode
        enemy = enemies[0]
        if enemy.hp <= 0:
            killed_enemies.append(enemy.name)
            total_xp += calculate_xp(enemy, player)

        typewriter(Fore.YELLOW + player.name + " has defeated " + enemy.name + "!", delay=0.1)

    update_presence(
        state="In Battle - Victory",
        details=f"XP {total_xp} | Enemies Defeated {len(killed_enemies)}"
    )
    time.sleep(1)
    clear_screen()
    animate_title(Fore.CYAN + "BATTLE OVER!", delay=0.05)
    time.sleep(1)

    # Show summary of battle
    print(center_text(Fore.WHITE + "Total XP: " + str(total_xp)))
    print(center_text(Fore.WHITE + "Current HP: " + str(player.hp) + "/" + str(player.max_hp)))
    print("")
    print(center_text(Fore.WHITE + "Enemies Defeated: " + ", ".join(killed_enemies)))

    print(center_text(Fore.YELLOW + "Press Enter to continue..." + Fore.RESET))

    # Award XP and check for level-up
    player.xp += total_xp
    check_level_up(player)

    input(Fore.YELLOW + "Press Enter to return to the game..." + Fore.RESET)
    clear_screen()

def calculate_ap_bonus(player_speed, enemy_speeds):
    total_enemy_speed = sum(enemy_speeds)
    if player_speed > total_enemy_speed:
        speed_difference = player_speed - total_enemy_speed
        extra_ap = min(3, speed_difference // 5) 
        return extra_ap
    return 0

def enemy_turn(player, enemies, mode):
    global turn
    print(Fore.CYAN + "-" * 40)
    typewriter(Fore.MAGENTA + "Enemy Turn - Turn " + str(turn))
    if mode == "multi":
        print(Fore.WHITE + "HP: " + str(player.hp) + " | Enemies Remaining: " + str(len([e for e in enemies if e.hp > 0])))

    else:
        print(Fore.WHITE + "HP: " + str(player.hp) + " | Enemy HP: " + str(enemies[0].hp))
    print(Fore.CYAN + "-" * 40)
    print("")

    player.process_status_effects()

    if player.is_staggered():
        print(Fore.YELLOW + player.name + " is staggered and can't act this turn!")
        print("")
        time.sleep(1)
    else:
        if mode == "multi":
            for enemy in enemies:
                if enemy.hp > 0:
                    enemy.choose_action(player)
                    time.sleep(2)
        else:
            if enemies[0].hp > 0: 
                enemies[0].choose_action(player)

def player_turn(player, enemies, mode, bonus_ap=0):
    global turn
    status_ticked = False
    if mode == "multi":
        ap = math.ceil(len(enemies) / 2)
        ap += calculate_ap_bonus(player.speed, [e.speed for e in enemies])
    else:
        ap = 1 + bonus_ap 

    while True:
        if mode == "multi":
            print(Fore.YELLOW + "You have " + str(ap) + " Action Points (AP).")
            
        if mode == "single" and ap <= 0:
            break  # Exit the loop if no AP in single mode
            
        print(Fore.CYAN + "-" * 40)
        typewriter(Fore.MAGENTA + "Your Turn - Turn " + str(turn))

        if mode == "multi":
            print(Fore.WHITE + "HP: " + str(player.hp) + " | Action Points: " + str(ap))
            alive_enemies = [e for e in enemies if e.hp > 0]  # Recalculate alive enemies
            
            for i, enemy in enumerate(alive_enemies):
                print(Fore.GREEN + str(i + 1) + ". " + enemy.name + " (" + str(enemy.hp) + "/" + str(enemy.max_hp) + " HP)")

        else:
            if bonus_ap > 0:
                print(Fore.WHITE + "HP: " + str(player.hp) + " | Action Points: " + str(ap)) 
            else:
                print(Fore.WHITE + "HP: " + str(player.hp) + " | Enemy HP: " + str(enemies[0].hp))
        
        print(Fore.CYAN + "-" * 40)
        print("")

        if not status_ticked:
            player.process_status_effects()
            status_ticked = True

        if player.is_staggered():
            print(Fore.YELLOW + player.name + " is staggered and can’t act normally!")
            print("")
            time.sleep(1)
            break

        typewriter(Fore.YELLOW + "What will you do?")
        
        if ap <= 0 and mode == "multi":
            print(Fore.BLACK + "1. Attack  [Not enough AP]")
            if isinstance(player.weapon, Weapon):
                print(Fore.BLACK + "Your weapon: " + player.weapon.name + " (equipped) | Durability: " + str(player.weapon.durability) + "/" + str(player.weapon.max_durability))
            else:
                print(Fore.BLACK + "You have no weapon equipped.")
            print(Fore.BLACK + "2. Defensive Stance  [Not enough AP]")
            if len(player.inventory.items) > 0:
                print(Fore.BLACK + "3. Use Item  [Not enough AP]")
            print(Fore.BLACK + "4. View Items  [Not enough AP]")
            print(Fore.BLACK + "5. View Character Sheet  [Not enough AP]")
            print(Fore.BLACK + "6. Identify  [Not enough AP]")
        else:
            print(Fore.GREEN + "1. Attack")
            if isinstance(player.weapon, Weapon):
                print(Fore.YELLOW + "Your weapon: " + player.weapon.name + " (equipped) | Durability: " + str(player.weapon.durability) + "/" + str(player.weapon.max_durability))
            else:
                print(Fore.RED + "You have no weapon equipped.")
            print(Fore.GREEN + "2. Defensive Stance")
            if len(player.inventory.items) > 0:
                print(Fore.GREEN + "3. Use Item")
            print(Fore.GREEN + "4. View Items")
            print(Fore.GREEN + "5. View Character Sheet")
            print(Fore.GREEN + "6. Identify")

        if mode == "multi":
            print(Fore.GREEN + "7. End Turn")

        choice = input(Fore.YELLOW + "> ").strip().lower()

        if choice == "1":
            if ap > 0:
                if mode == "multi":
                    print(Fore.YELLOW + "Choose a target to attack:")
                    
                    # Create a list of alive enemies
                    alive_enemies = [e for e in enemies if e.hp > 0]
                    
                    # Display all alive enemies
                    for i, enemy in enumerate(alive_enemies):
                        print(Fore.GREEN + str(i + 1) + ". " + enemy.name + " (" + str(enemy.hp) + "/" + str(enemy.max_hp) + " HP)")

                    try:
                        # Prompt the player to select an enemy
                        index = int(input(Fore.YELLOW + "> ")) - 1
                        
                        # Ensure the index is within bounds of the alive_enemies list
                        if 0 <= index < len(alive_enemies):
                            target = alive_enemies[index]  # Get the actual target based on selection

                            # If player has no weapon, use a punch attack
                            if player.weapon is None:
                                player.punch(target)
                            else:
                                # AOE Weapon: Attack all enemies
                                if hasattr(player.weapon, 'aoe') and player.weapon.aoe:
                                    print(Fore.YELLOW + "You unleash a powerful area-of-effect attack!")
                                    for enemy in alive_enemies:
                                        if enemy.hp > 0:  # Only attack alive enemies
                                            player.weapon.attack(player, enemy)
                                else:
                                    # Single-target weapon attack
                                    player.weapon.attack(player, target)
                            
                            ap -= 1  # Deduct AP after the attack
                        else:
                            print(Fore.RED + "Invalid selection. Please choose a valid target.")

                        print("")  # Space after the action

                    except ValueError:
                        print(Fore.RED + "Invalid input. Please enter a number.")

                else:
                    target = enemies[0]
                    if target.hp > 0:
                        if player.weapon is None:
                            player.punch(target)
                        else:
                            if hasattr(player.weapon, 'aoe') and player.weapon.aoe:
                                # AOE Weapon: Attack all enemies
                                print(Fore.YELLOW + "You unleash a powerful area-of-effect attack!")
                                print("")
                                time.sleep(2)
                                for enemy in enemies:
                                    if enemy.hp > 0:  # Only attack alive enemies
                                        player.weapon.attack(player, enemy)
                                        time.sleep(2)
                            else:
                                # Single-target weapon
                                player.weapon.attack(player, target)
                        ap -= 1
                        print("")
                        break
            else:
                if mode == "multi":
                    print(Fore.RED + "Not enough Action Points to attack.")
                    print("")
        elif choice == "2":
            if ap > 0:
                player.defend()
                ap -= 1
            else:
                if mode == "multi":
                    print(Fore.RED + "Not enough Action Points to take a defensive stance.")
                    print("")
        elif choice == "3":
            if len(player.inventory.items) > 0:
                while True:

                    if ap <= 0 and mode == "multi":
                        print(Fore.RED + "You don't have enough AP to use an item!")
                        print("")
                        break
                    elif ap <= 0:
                        break

                    print(Fore.CYAN + "-" * 40)
                    print(Fore.YELLOW + "Choose an item by number (or 'Enter' to go back):")
                    for i, item in enumerate(player.inventory.items):
                        print(Fore.GREEN + "%s. %s" % (str(i + 1), item.name))
                        for line in item.description.split("\n"):
                            print(Fore.LIGHTBLACK_EX + "   " + line)
                        if hasattr(item, "durability") and hasattr(item, "max_durability"):
                            print(Fore.LIGHTBLACK_EX + "   Durability: %s/%s" % (str(item.durability), str(item.max_durability)))
                        elif hasattr(item, "quantity"):
                            print(Fore.LIGHTBLACK_EX + "   Quantity: %s" % str(item.quantity))

                    item_choice = input(Fore.YELLOW + "> ").strip().lower()

                    if item_choice == "":
                        break

                    try:
                        index = int(item_choice) - 1
                        if 0 <= index < len(player.inventory.items):
                            item = player.inventory.items[index]
                            if isinstance(item, UseableItem):
                                if enemies:
                                    print("Choose an enemy to target for cleansing:")
                                    for i, enemy in enumerate(enemies):
                                        if enemy.corrupted:
                                            print(Fore.GREEN + str(i + 1) + ". " + enemy.name + Style.RESET_ALL)

                                    target_choice = input(Fore.YELLOW + "> ")
                                    target_choice = int(target_choice) - 1
                                    target = enemies[target_choice]

                                    item.use(player, target)
                                else:
                                    print(Fore.RED + "No enemies available to target." + Style.RESET_ALL)
                            elif isinstance(item, Weapon):
                                item.equip(player)
                                print(Fore.GREEN + item.name + " equipped!")
                            elif isinstance(item, Potion):
                                item.use(player)
                                print(Fore.GREEN + item.name + " used successfully!")
                                player.inventory.items.remove(item)  # Remove the potion from inventory after use
                            elif isinstance(item, APPotion):
                                item.use(player)
                                print(Fore.GREEN + item.name + " used successfully!")
                                player.inventory.items.remove(item)  # Remove the potion from inventory after use
                            else:
                                print(Fore.RED + "This item cannot be used here.")
                            ap -= 1 
                            if mode == "multi":
                                print("")
                                print(Fore.GREEN + item.name + " used! Remaining AP: " + str(ap))
                                print("")
                                time.sleep(1)
                        else:
                            print(Fore.RED + "Invalid item selection.")
                    except ValueError:
                        print(Fore.RED + "Invalid input.")
            else:
                print(Fore.RED + "Your inventory is empty.")
        elif choice == "4":
            for i, item in enumerate(player.inventory.items):
                print(Fore.GREEN + "%s. %s" % (str(i + 1), item.name))
                for line in item.description.split("\n"):
                    print(Fore.LIGHTBLACK_EX + "   " + line)
                if hasattr(item, "durability") and hasattr(item, "max_durability"):
                    print(Fore.LIGHTBLACK_EX + "   Durability: %s/%s" % (str(item.durability), str(item.max_durability)))
                elif hasattr(item, "quantity"):
                    print(Fore.LIGHTBLACK_EX + "   Quantity: %s" % str(item.quantity))
                time.sleep(3)

        elif choice == "5":
            show_character_sheet(player, False)
        elif choice == "6":
            if mode == "multi":
                for enemy in enemies:
                    if enemy.hp <= 0:
                        continue
                    print(Fore.CYAN + "--- Enemy: " + enemy.name)
                    print(Fore.YELLOW + "Health: " + str(enemy.hp) + "/" + str(enemy.max_hp))
                    print(Fore.YELLOW + "Level: " + str(enemy.level))
                    if enemy.corrupted:
                        enemy.reveal_identity() 

                    time.sleep(1) 
            else:
                print(Fore.CYAN + "--- Enemy: " + enemies[0].name)
                print(Fore.YELLOW + "Health: " + str(enemies[0].hp) + "/" + str(enemies[0].max_hp))
                print(Fore.YELLOW + "Level: " + str(enemies[0].level))
                if enemies[0].corrupted:
                    enemies[0].reveal_identity()

        elif choice == "7" and mode == "multi":
            break
        else:
            print(Fore.RED + "Invalid input.")
            print("")

def battle(player, enemies, battle_mode="single", bonus_ap=0):
    from discord import update_presence  # Import the update_presence function
    global turn
    turn = 1
    clear_screen()
    player_went_first = False

    if not isinstance(enemies, list):
        enemies = [enemies]

    # Update Discord Presence for the start of the battle
    update_presence(
        state="In a Battle",
        details="Preparing for Battle",
        small_image="battle",
        small_text=f"Turn {turn} | Preparing"
    )

    # Battle logic
    if battle_mode == "multi":
        typewriter(random.choice(multi_battle_intro(player, enemies)))
        print("")
        time.sleep(1)
        if all(enemy.speed < player.speed for enemy in enemies):
            typewriter(multi_battle_player_goes_first(player, enemies))
            print("")
            time.sleep(2)
            # Update Discord Presence for player's turn
            update_presence(
                state="In a Battle",
                details=f"Turn {turn} | HP: {player.hp}/{player.max_hp} | AP: {math.ceil(len(enemies) / 2)}",
                small_image="battle",
                small_text=f"Turn {turn} | {player.name}'s Turn"
            )
            player_turn(player, enemies, battle_mode, bonus_ap)
            player_went_first = True
        elif all(enemy.speed > player.speed for enemy in enemies):
            typewriter(multi_battle_enemies_go_first(player, enemies))
            print("")
            time.sleep(1)
            # Update Discord Presence for enemy's turn
            update_presence(
                state="In a Battle",
                details=f"Turn {turn} | Enemies Left: {len([e for e in enemies if e.hp > 0])} | Enemy's Turn",
                small_image="battle",
                small_text=f"Turn {turn} | Enemies' Turn"
            )
            enemy_turn(player, enemies, battle_mode)
        else:
            typewriter(multi_battle_random_initiative(player, enemies))
            print("")
            time.sleep(3)
            if random.choice([True, False]):
                # Update Discord Presence for player's turn
                update_presence(
                    state="In a Battle",
                    details=f"Turn {turn} | HP: {player.hp}/{player.max_hp} | AP: {math.ceil(len(enemies) / 2)}",
                    small_image="battle",
                    small_text=f"Turn {turn} | {player.name}'s Turn"
                )
                player_turn(player, enemies, battle_mode, bonus_ap)
                player_went_first = True
            else:
                # Update Discord Presence for enemy's turn
                update_presence(
                    state="In a Battle",
                    details=f"Turn {turn} | Enemies Left: {len([e for e in enemies if e.hp > 0])} | Enemy's Turn",
                    small_image="battle",
                    small_text=f"Turn {turn} | Enemies' Turn"
                )
                enemy_turn(player, enemies, battle_mode)
    else:
        typewriter(randomized_intro_messages(player, enemies[0]))
        print("")
        time.sleep(2)
        typewriter("Battle started!")
        print("")
        time.sleep(1)
        typewriter(f"{player.name} v.s {enemies[0].name}")
        print("")
        time.sleep(2)
        if enemies[0].speed > player.speed:
            typewriter(enemy_attacks_first_message(player, enemies[0]))
            print("")
            time.sleep(2)
            # Update Discord Presence for enemy's turn
            update_presence(
                state="In a Battle",
                details=f"Turn {turn} | Enemy HP: {enemies[0].hp}/{enemies[0].max_hp} | Enemy's Turn",
                small_image="battle",
                small_text=f"Turn {turn} | Enemies' Turn"
            )
            enemy_turn(player, enemies, battle_mode)
        elif enemies[0].speed < player.speed:
            typewriter(player_attacks_first_message(player, enemies[0]))
            print("")
            time.sleep(1)
            # Update Discord Presence for player's turn
            update_presence(
                state="In a Battle",
                details=f"Turn {turn} | HP: {player.hp}/{player.max_hp} | AP: {1 + bonus_ap}",
                small_image="battle",
                small_text=f"Turn {turn} | {player.name}'s Turn"
            )
            player_turn(player, enemies, battle_mode, bonus_ap)
            player_went_first = True
        else:
            typewriter(random_initiative_message(player, enemies[0]))
            print("")
            time.sleep(3)
            if random.randint(1, 2) == 1:
                # Update Discord Presence for player's turn
                update_presence(
                    state="In a Battle",
                    details=f"Turn {turn} | HP: {player.hp}/{player.max_hp} | AP: {1 + bonus_ap}",
                    small_image="battle",
                    small_text=f"Turn {turn} | {player.name}'s Turn"
                )
                player_turn(player, enemies, battle_mode, bonus_ap)
                player_went_first = True
            else:
                # Update Discord Presence for enemy's turn
                update_presence(
                    state="In a Battle",
                    details=f"Turn {turn} | Enemy HP: {enemies[0].hp}/{enemies[0].max_hp} | Enemy's Turn",
                    small_image="battle",
                    small_text=f"Turn {turn} | Enemies' Turn"
                )
                enemy_turn(player, enemies, battle_mode)

    # Ensure the enemy does not attack twice if they went first
    if not player_went_first and any(e.hp > 0 for e in enemies):
        player_turn(player, enemies, battle_mode, bonus_ap)

    # Main battle loop
    while player.hp > 0 and any(enemy.hp > 0 for enemy in enemies):
        turn += 1
        print("\n" + f"--- Turn {turn} ---")

        # Update Discord Presence during the battle
        if turn % 2 == 1:  # Player's turn
            if battle_mode == "single":
                update_presence(
                    state="In a Battle",
                    details=f"Turn {turn} | HP: {player.hp}/{player.max_hp} | AP: {1 + bonus_ap}",
                    small_image="battle",
                    small_text=f"Turn {turn} | {player.name}'s Turn"
                )
            else:
                update_presence(
                    state="In a Battle",
                    details=f"Turn {turn} | HP: {player.hp}/{player.max_hp} | AP: {math.ceil(len(enemies) / 2)}",
                    small_image="battle",
                    small_text=f"Turn {turn} | {player.name}'s Turn"
                )
            player_turn(player, enemies, battle_mode, bonus_ap)
        else:  # Enemy's turn
            if battle_mode == "single":
                update_presence(
                    state="In a Battle",
                    details=f"Turn {turn} | Enemy HP: {enemies[0].hp}/{enemies[0].max_hp} | Enemy's Turn",
                    small_image="battle",
                    small_text=f"Turn {turn} | Enemies' Turn"
                )
            else:
                update_presence(
                    state="In a Battle",
                    details=f"Turn {turn} | Enemies Left: {len([e for e in enemies if e.hp > 0])} | Enemy's Turn",
                    small_image="battle",
                    small_text=f"Turn {turn} | Enemies' Turn"
                )
            enemy_turn(player, enemies, battle_mode)

    if player.hp <= 0:
        return False
    else:
        battle_conclusion(player, enemies, battle_mode)
        return True