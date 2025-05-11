import time
import random
import os
from enemies import *
from inventory import Inventory
from items import *
from game_data import *
from player import Player
from title import animate_title
from text_utils import *
from screens import death_screen, show_character_sheet
from loot_tables import loot_tables, roll_corrupted_loot,roll_loot
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
break_loop = False

def check_level_up(player):
    player.check_level_up()

def get_loot(enemies, battle_mode='single'):
    loot = []
    
    if battle_mode == 'single' and len(enemies) == 1:
        enemy_type = enemies[0]
        loot += roll_loot(enemy_type)
    
    elif battle_mode == 'multi':
        for enemy in enemies:
            loot += roll_loot(enemy)
    
    return loot

def calculate_money(enemy, difficulty):
    base_money = 10
    level_multiplier = enemy.level * 5
    difficulty_multiplier = 1 + (difficulty / 100)
    random_bonus = random.randint(0, 20)
    money = (base_money + level_multiplier) * difficulty_multiplier + random_bonus
    return round(money)

def calculate_xp(enemy, player):
    base_xp = 50
    level_difference = enemy.level - player.level

    # If the enemy is stronger, increase XP reward
    level_multiplier = (enemy.level * 2) + (level_difference * 5)
    
    # Prevent XP rewards from becoming negative or zero if the player is much higher level than the enemy
    level_multiplier = max(level_multiplier, 10)
    
    xp = base_xp + level_multiplier
    return xp

def battle_conclusion(player, enemies, mode):
    clear_screen()
    global difficulty
    result = "Victory"
    total_xp = 0
    total_money = 0
    killed_enemies = []
    total_loot = []

    if mode == "multi":
        for enemy in enemies:
            if enemy.hp <= 0:
                killed_enemies.append(enemy.name)
                total_xp += calculate_xp(enemy, player)
                total_money += calculate_money(enemy, difficulty)

                if enemy.corrupted:
                    loot = roll_corrupted_loot(enemy.name, unstable=enemy.unstable)
                else:
                    loot = roll_loot(enemy.name)

                total_loot.append((enemy.name, loot))  # Tuple (enemy_name, loot)

        total_xp += int(total_xp * 0.25)
        total_money += int(total_money * 0.25)

        typewriter(Fore.YELLOW + player.name + " has defeated the following enemies:", delay=0.1)
        for enemy in killed_enemies:
            print(Fore.GREEN + "- " + enemy)
        typewriter(Fore.GREEN + player.name + " gains " + str(total_xp) + " XP and " + str(total_money) + " coins!", delay=0.1)

        enemies = [e for e in enemies if e.hp > 0]
    else:  # Single battle mode
        enemy = enemies[0]
        if enemy.hp <= 0:
            killed_enemies.append(enemy.name)
            total_xp += calculate_xp(enemy, player)
            total_money += calculate_money(enemy, difficulty)

            if enemy.loot_table_key != "none":
                if enemy.corrupted:
                    loot = roll_corrupted_loot(enemy.loot_table_key, unstable=enemy.unstable)
                else:
                    loot = roll_loot(enemy.loot_table_key)
                total_loot.append((enemy.name, loot))  # Attach loot to enemy name
            else:
                loot = []  # No loot if no loot table key

        typewriter(Fore.YELLOW + player.name + " has defeated " + enemy.name + "!", delay=0.1)
        typewriter(Fore.GREEN + player.name + " gains " + str(total_xp) + " XP and " + str(total_money) + " coins!", delay=0.1)

    time.sleep(1)
    clear_screen()

    # Update Discord Presence for battle conclusion
    update_presence(
        state="In Battle - Victory",
        details=f"XP {total_xp} | $ {total_money} | Lvl {player.level}"
    )

    animate_title(Fore.CYAN + "BATTLE OVER!", delay=0.05)
    time.sleep(1)

    # Show summary of battle
    print(center_text(Fore.WHITE + "Total XP: " + str(total_xp)))
    print(center_text(Fore.WHITE + "Current HP: " + str(player.hp) + "/" + str(player.max_hp)))
    print(center_text(Fore.WHITE + "Money: " + str(total_money)))
    print("")
    print(center_text(Fore.WHITE + "Enemies Defeated: " + ", ".join(killed_enemies)))

    if total_loot:  # Only print Loot if there is any
        print(center_text(Fore.YELLOW + "Loot Dropped:"))
        for enemy_name, loot in total_loot:  # Unpack the tuple (enemy_name, loot)
            for item in loot:
                if "Corrupted" in item.name:
                    print(center_text(Fore.MAGENTA + f"- {item.name} (Dropped by {enemy_name})"))
                else:
                    print(center_text(Fore.GREEN + f"- {item.name} (Dropped by {enemy_name})"))

    print(center_text(Fore.YELLOW + "Press Enter to continue..." + Fore.RESET))

    # Award XP and money
    player.xp += total_xp
    player.money += total_money

    # Check for level-up
    check_level_up(player)

    # Add loot to inventory
    for enemy_name, loot in total_loot:  # Unpack loot for adding to player inventory
        for item in loot:
            player.inventory.add_item(item)

    # Wait for the player to acknowledge the battle conclusion
    input((center_text(Fore.YELLOW + "Press Enter to return to the game..." + Fore.RESET)))
    clear_screen()

    # Ensure the function exits cleanly
    return result

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
            break  # Exit if no AP left in single mode

        print(Fore.CYAN + "-" * 40)
        typewriter(Fore.MAGENTA + "Your Turn - Turn " + str(turn))

        if mode == "multi":
            print(Fore.WHITE + "HP: " + str(player.hp) + " | Action Points: " + str(ap))

            alive_enemies = [e for e in enemies if e.hp > 0]
            for i, enemy in enumerate(alive_enemies):
                print(Fore.GREEN + str(i + 1) + ". " + enemy.name + " (" + str(enemy.hp) + "/" + str(enemy.max_hp) + " HP)")
        else:
            print(Fore.WHITE + "HP: " + str(player.hp) + " | Enemy HP: " + str(enemies[0].hp) + " | Action Points: " + str(ap))

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
            print(Fore.BLACK + "2. Defensive Stance  [Not enough AP]")
            if len(player.inventory.items) > 0:
                print(Fore.BLACK + "3. Use Item  [Not enough AP]")
            print(Fore.BLACK + "4. View Items  [Not enough AP]")
            print(Fore.BLACK + "5. View Character Sheet  [Not enough AP]")
            print(Fore.BLACK + "6. Identify  [Not enough AP]")
        else:
            print(Fore.GREEN + "1. Attack")
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
                    alive_enemies = [e for e in enemies if e.hp > 0]
                    for i, enemy in enumerate(alive_enemies):
                        print(Fore.GREEN + str(i + 1) + ". " + enemy.name + " (" + str(enemy.hp) + "/" + str(enemy.max_hp) + " HP)")
                    try:
                        index = int(input(Fore.YELLOW + "> ")) - 1
                        if 0 <= index < len(alive_enemies):
                            target = alive_enemies[index]
                            if player.weapon is None:
                                player.punch(target)
                            else:
                                if hasattr(player.weapon, 'aoe') and player.weapon.aoe:
                                    print(Fore.YELLOW + "You unleash a powerful area-of-effect attack!")
                                    for enemy in alive_enemies:
                                        if enemy.hp > 0:
                                            player.weapon.attack(player, enemy)
                                else:
                                    player.weapon.attack(player, target)
                            ap -= 1
                        else:
                            print(Fore.RED + "Invalid selection.")
                    except ValueError:
                        print(Fore.RED + "Invalid input.")
                    print("")
                else:
                    target = enemies[0]
                    if target.hp > 0:
                        if player.weapon is None:
                            player.punch(target)
                        else:
                            if hasattr(player.weapon, 'aoe') and player.weapon.aoe:
                                print(Fore.YELLOW + "You unleash a powerful area-of-effect attack!")
                                print("")
                                time.sleep(2)
                                for enemy in enemies:
                                    if enemy.hp > 0:
                                        player.weapon.attack(player, enemy)
                                        time.sleep(2)
                            else:
                                player.weapon.attack(player, target)
                        ap -= 1
                        print("")
                        if ap <= 0:
                            break
            else:
                if mode == "multi":
                    print(Fore.RED + "Not enough Action Points to attack.")

        elif choice == "2":
            if ap > 0:
                player.defend()
                ap -= 1
                if mode == "single" and ap <= 0:
                    break
            else:
                if mode == "multi":
                    print(Fore.RED + "Not enough Action Points to defend.")

        elif choice == "3":
            if len(player.inventory.items) > 0:
                while True:
                    if ap <= 0:
                        print(Fore.RED + "Not enough AP to use an item.")
                        break

                    print(Fore.CYAN + "-" * 40)
                    print(Fore.YELLOW + "Choose an item by number (or 'Enter' to go back):")
                    for i, item in enumerate(player.inventory.items):
                        print(Fore.GREEN + f"{i + 1}. {item.name}")
                        for line in item.description.split("\n"):
                            print(Fore.LIGHTBLACK_EX + "   " + line)
                        if hasattr(item, "durability") and hasattr(item, "max_durability"):
                            print(Fore.LIGHTBLACK_EX + f"   Durability: {item.durability}/{item.max_durability}")
                        elif hasattr(item, "quantity"):
                            print(Fore.LIGHTBLACK_EX + f"   Quantity: {item.quantity}")

                    item_choice = input(Fore.YELLOW + "> ").strip()
                    if item_choice == "":
                        break

                    try:
                        index = int(item_choice) - 1
                        if 0 <= index < len(player.inventory.items):
                            item = player.inventory.items[index]
                            if isinstance(item, UseableItem):
                                print("Choose an enemy to target for cleansing:")
                                for i, enemy in enumerate(enemies):
                                    if enemy.corrupted:
                                        print(Fore.GREEN + f"{i + 1}. {enemy.name}")
                                target_choice = input(Fore.YELLOW + "> ")
                                target = enemies[int(target_choice) - 1]
                                item.use(player, target)
                            elif isinstance(item, Weapon):
                                item.equip(player)
                                print(Fore.GREEN + f"{item.name} equipped!")
                            elif isinstance(item, Potion):
                                item.use(player)
                                print(Fore.GREEN + f"{item.name} used!")
                                player.inventory.items.remove(item)
                            else:
                                print(Fore.RED + "This item cannot be used.")
                            ap -= 1
                            if mode == "single" and ap <= 0:
                                break
                        else:
                            print(Fore.RED + "Invalid item selection.")
                    except ValueError:
                        print(Fore.RED + "Invalid input.")
            else:
                print(Fore.RED + "Your inventory is empty.")

        elif choice == "4":
            for i, item in enumerate(player.inventory.items):
                print(Fore.GREEN + f"{i + 1}. {item.name}")
                for line in item.description.split("\n"):
                    print(Fore.LIGHTBLACK_EX + "   " + line)
                if hasattr(item, "durability") and hasattr(item, "max_durability"):
                    print(Fore.LIGHTBLACK_EX + f"   Durability: {item.durability}/{item.max_durability}")
                elif hasattr(item, "quantity"):
                    print(Fore.LIGHTBLACK_EX + f"   Quantity: {item.quantity}")
            time.sleep(3)

        elif choice == "5":
            show_character_sheet(player, False)

        elif choice == "6":
            if mode == "multi":
                for enemy in enemies:
                    if enemy.hp > 0:
                        print(Fore.CYAN + f"--- Enemy: {enemy.name}")
                        print(Fore.YELLOW + f"Health: {enemy.hp}/{enemy.max_hp}")
                        print(Fore.YELLOW + f"Level: {enemy.level}")
                        if enemy.corrupted:
                            enemy.reveal_identity()
                        time.sleep(1)
            else:
                enemy = enemies[0]
                print(Fore.CYAN + f"--- Enemy: {enemy.name}")
                print(Fore.YELLOW + f"Health: {enemy.hp}/{enemy.max_hp}")
                print(Fore.YELLOW + f"Level: {enemy.level}")
                if enemy.corrupted:
                    enemy.reveal_identity()

        elif choice == "7" and mode == "multi":
            break

        else:
            print(Fore.RED + "Invalid input.")


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
        death_screen()
        return False
    else:
        battle_conclusion(player, enemies, battle_mode)
        return True